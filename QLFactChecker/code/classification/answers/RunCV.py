import sys
sys.path.insert(0, '../../data/features/')

import csv, os, random
import string
import time
from sklearn.preprocessing import Normalizer
from sklearn.svm import *
from sklearn.naive_bayes import *
from sklearn.linear_model import *
from sklearn.model_selection import *
from sklearn.preprocessing import *
from sklearn.pipeline import *
from sklearn.ensemble import RandomForestClassifier

from sklearn.feature_selection import *
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from comment import Comment
import comment_utils
import Features
import FeatureSets
import numpy as np

# timestamp = time.strftime('%d-%m-%Y %H.%M.%S')
# We do not want to always have the timestamp, we will clear the predictions file every time instead
# This way we will not produce a huge amount of unused files and will always have the latest version.
timestamp = '' 
time_string = time.strftime('%d-%m-%Y %H.%M.%S')
EVALUATE_WITH_SCORE = True

SET_NAME = 'dev+test'
TEST_SET_NAME = 'train1'
DATA_PATH = "../../../data/input/input-"+SET_NAME+".xml"
TEST_DATA_PATH = "../../../data/input/input-"+TEST_SET_NAME+".xml"

EVAL_ON_TEST_SET = False

SCORE_PREDICTIONS_PATH = string.Template("../../../data/predictions/predicted-labels-$set-$run_id-scores.tsv")
RANKING_PREDICTIONS_PATH = string.Template("../../../data/predictions/predicted-labels-$set-$run_id-ranking.tsv")
PREDICTIONS_PATH = string.Template("../../../data/predictions/predicted-labels-$set-$run_id-$time.tsv")
RESULTS_FILE = "../../../data/results/results-answers-cross-validation-"+SET_NAME+".tsv"
CROSS_VALIDATION = True
# <0: leave-1-comment-out
# 0: leave-1-question-out
# >0: splits size
SPLIT_SETS_SIZE = 0

INCLUDE_TEXT_BASELINES = True

#ANALYSIS
ANALYSIS_PATH = string.Template("../../../data/analysis/analysis-data-$set-$run_id.tsv")

# ANALYSIS
def analysis_path(run_id, set_name=SET_NAME):
	return ANALYSIS_PATH.substitute(set=set_name, run_id=run_id[:50])

def predictions_path(run_id, set_name=SET_NAME):
    return PREDICTIONS_PATH.substitute(set=set_name, run_id=run_id[:50], time=timestamp)

def score_predictions_path(run_id, set_name=SET_NAME):
    return SCORE_PREDICTIONS_PATH.substitute(set=set_name, run_id=run_id[:50])

def ranking_predictions_path(run_id, set_name=SET_NAME):
    return RANKING_PREDICTIONS_PATH.substitute(set=set_name, run_id=run_id[:50])

def run(run_id, feat_index=''):
    clear_prediction_files(run_id)
    if SPLIT_SETS_SIZE >= 0:
        run_split_sets(run_id, SPLIT_SETS_SIZE, feat_index)
    else:
        run_leave_one_out(run_id, feat_index)
#svm-rank
def run_rank(run_id, feat_index=''):
    clear_prediction_files(run_id)
    if SPLIT_SETS_SIZE >= 0:
        test_set, train_set, dev_features, train_features, dev_predicted, train_labels = run_split_sets_rank(run_id, SPLIT_SETS_SIZE, feat_index)
        
    # else:
    #     test_set, train_set, dev_features, train_features, dev_predicted = run_leave_one_out_rank(run_id, feat_index)
        

    return test_set, train_set, dev_features, train_features, dev_predicted,train_labels

def clear_prediction_files(run_id):
    if EVALUATE_WITH_SCORE:
        # clear the predictions file to overwrite it with the latest result
        if os.path.exists(score_predictions_path(run_id)):
            os.remove(score_predictions_path(run_id))
        if os.path.exists(ranking_predictions_path(run_id)):
            os.remove(ranking_predictions_path(run_id))
        if EVAL_ON_TEST_SET:
            if os.path.exists(score_predictions_path(run_id, TEST_SET_NAME)):
                os.remove(score_predictions_path(run_id, TEST_SET_NAME))
            if os.path.exists(ranking_predictions_path(run_id, TEST_SET_NAME)):
                os.remove(ranking_predictions_path(run_id, TEST_SET_NAME))
    if os.path.exists(predictions_path(run_id)):
        os.remove(predictions_path(run_id))
    if EVAL_ON_TEST_SET:
        if os.path.exists(predictions_path(run_id, TEST_SET_NAME)):
            os.remove(predictions_path(run_id, TEST_SET_NAME))

def run_leave_one_out(run_id, feat_index=''):
    print('--RUN_ID: ', run_id)
    ensure_required_directories_exist()
   
    full_set = comment_utils.read_comments(DATA_PATH)
   
    if not os.path.exists(RESULTS_FILE):
        # If the results file does not exist - calcualte the baselines
        write_to_csv_file(['RUN-ID', 'Time', 'Params', 'Optimized for', 'SET', 'Accuracy', 'Precision', 'Recall', 'F1', 'MAP', 'Predictions', '', ''], RESULTS_FILE)
        calculate_baseline(full_set, 0, 'all-negative', RESULTS_FILE)
        calculate_baseline(full_set, 1, 'all-positive', RESULTS_FILE)

    best_params, scoring = run_experiment(full_set, full_set, run_id, feat_index, True)

    for i in range(0,len(full_set)):
        print('running experiments for split', i)
        train_set = list(full_set)
        test_set = []
        test_set.append(full_set[i])
        train_set.remove(full_set[i])
        print('LEAVE ONE OUT', len(test_set), len(train_set))
        params, scoring = run_experiment(train_set, test_set, run_id, feat_index, False, best_params)

    evaluate_test_sets(RESULTS_FILE, run_id, params, scoring)

#svm-rank
def run_leave_one_out_rank(run_id, feat_index=''):
    print('--RUN_ID: ', run_id)
    ensure_required_directories_exist()
   
    full_set = comment_utils.read_comments(DATA_PATH)
   
    if not os.path.exists(RESULTS_FILE):
        # If the results file does not exist - calcualte the baselines
        write_to_csv_file(['RUN-ID', 'Time', 'Params', 'Optimized for', 'SET', 'Accuracy', 'Precision', 'Recall', 'F1', 'MAP', 'Predictions', '', ''], RESULTS_FILE)
        calculate_baseline(full_set, 0, 'all-negative', RESULTS_FILE)
        calculate_baseline(full_set, 1, 'all-positive', RESULTS_FILE)

    best_params, scoring, train_features, dev_features, dev_predicted = run_experiment_rank(full_set, full_set, run_id, feat_index, True)

    for i in range(0,len(full_set)):
        print('running experiments for split', i)
        train_set = list(full_set)
        test_set = []
        test_set.append(full_set[i])
        train_set.remove(full_set[i])
        print('LEAVE ONE OUT', len(test_set), len(train_set))
        params, scoring, train_features, dev_features, dev_predicted  = run_experiment_rank(train_set, test_set, run_id, feat_index, False, best_params)

    evaluate_test_sets(RESULTS_FILE, run_id, params, scoring)
    return test_set, train_set, dev_features, train_features, dev_predicted

def run_split_sets(run_id, splits, feat_index=''):
    print('--RUN_ID: ', run_id)
    ensure_required_directories_exist()

    set_parts = []

    if splits == 0:
        set_parts = comment_utils.split_set_in_parts_leave_1_question_out(DATA_PATH)
    else:
        set_parts = comment_utils.split_set_in_consecutive_parts(DATA_PATH, splits)

    full_set = []
    for i in range(0,len(set_parts)):
        full_set.extend(set_parts[i])

    test_set = comment_utils.read_comments(TEST_DATA_PATH)

    # for comment in test_set:
    #     print(comment.comment_id, comment.label)

    if not os.path.exists(RESULTS_FILE):
        # If the results file does not exist - calcualte the baselines
        write_to_csv_file(['RUN-ID', 'Time', 'Params', 'Optimized for', 'SET', 'Accuracy', 'Precision', 'Recall', 'F1', 'MAP', 'Predictions', '', ''], RESULTS_FILE)
        calculate_baseline(full_set, 0, 'classification-baseline-all-negative', RESULTS_FILE)
        calculate_baseline(full_set, 1, 'classification-baseline-all-positive', RESULTS_FILE)
        if EVALUATE_WITH_SCORE:
            # If the results file does not exist - calcualte the baselines
            calculate_baseline_with_score(full_set, 'ranking-baseline-default-comment-order', RESULTS_FILE)
            calculate_baseline_with_score_oracle(full_set, 'ranking-baseline-oracle', RESULTS_FILE)
            calculate_baseline_with_score_random(full_set, 'ranking-baseline-random', RESULTS_FILE)

        if EVAL_ON_TEST_SET:
            # calculate baselines for test set
            calculate_baseline(test_set, 0, 'classification-baseline-all-negative', RESULTS_FILE, TEST_SET_NAME, TEST_DATA_PATH)
            calculate_baseline(test_set, 1, 'classification-baseline-all-positive', RESULTS_FILE, TEST_SET_NAME, TEST_DATA_PATH)
            if EVALUATE_WITH_SCORE:
                # If the results file does not exist - calcualte the baselines
                calculate_baseline_with_score(test_set, 'ranking-baseline-default-comment-order', RESULTS_FILE, TEST_SET_NAME, TEST_DATA_PATH)
                calculate_baseline_with_score_oracle(test_set, 'ranking-baseline-oracle', RESULTS_FILE, TEST_SET_NAME, TEST_DATA_PATH)
                calculate_baseline_with_score_random(test_set, 'ranking-baseline-random', RESULTS_FILE, TEST_SET_NAME, TEST_DATA_PATH)

        if INCLUDE_TEXT_BASELINES:
            calculate_baseline_bag_of_words(set_parts, 'baseline-bag-of-words', 1, 1, False, RESULTS_FILE)
            calculate_baseline_bag_of_words(set_parts, 'baseline-word-ngrams-2', 2, 2, False, RESULTS_FILE)
            calculate_baseline_bag_of_words(set_parts, 'baseline-word-ngrams-3', 3, 3, False, RESULTS_FILE)
            calculate_baseline_bag_of_words(set_parts, 'baseline-word-ngrams-4', 4, 4, False, RESULTS_FILE)
            # calculate_baseline_bag_of_words(set_parts, 'baseline-word-ngrams-1-2', 1, 2, False, RESULTS_FILE)
            # calculate_baseline_bag_of_words(set_parts, 'baseline-word-ngrams-1-3', 1, 3, False, RESULTS_FILE)
            # calculate_baseline_bag_of_words(set_parts, 'baseline-word-ngrams-2-3', 2, 3, False, RESULTS_FILE)
            # calculate_baseline_bag_of_words(set_parts, 'baseline-word-ngrams-1-4', 1, 4, False, RESULTS_FILE)
            # calculate_baseline_bag_of_words(set_parts, 'baseline-word-ngrams-2-4', 2, 4, False, RESULTS_FILE)
            # calculate_baseline_bag_of_words(set_parts, 'baseline-bag-of-words-tfidf', 1, 1, True, RESULTS_FILE)
            # calculate_baseline_bag_of_words(set_parts, 'baseline-word-ngrams-tfidf-2', 2, 2, True, RESULTS_FILE)
            # calculate_baseline_bag_of_words(set_parts, 'baseline-word-ngrams-tfidf-3', 3, 3, True, RESULTS_FILE)
            # calculate_baseline_bag_of_words(set_parts, 'baseline-word-ngrams-tfidf-4', 4, 4, True, RESULTS_FILE)
            # calculate_baseline_bag_of_words(set_parts, 'baseline-word-ngrams-tfidf-1-2', 1, 2, True, RESULTS_FILE)
            # calculate_baseline_bag_of_words(set_parts, 'baseline-word-ngrams-tfidf-1-3', 1, 3, True, RESULTS_FILE)
            # calculate_baseline_bag_of_words(set_parts, 'baseline-word-ngrams-tfidf-2-3', 2, 3, True, RESULTS_FILE)
            # calculate_baseline_bag_of_words(set_parts, 'baseline-word-ngrams-tfidf-1-4', 1, 4, True, RESULTS_FILE)
            # calculate_baseline_bag_of_words(set_parts, 'baseline-word-ngrams-tfidf-2-4', 2, 4, True, RESULTS_FILE)
            
    best_params, scoring = run_experiment(full_set, full_set, run_id, feat_index, True)

    for i in range(0,len(set_parts)):
        print('running experiments for split', i)
        train_set = list(full_set)
        dev_set = set_parts[i]
        for c in dev_set:
            train_set.remove(c)
        params, scoring = run_experiment(train_set, dev_set, run_id, feat_index, False, best_params)

    evaluate_test_sets(RESULTS_FILE, run_id, params, scoring)

    # predict and evaluate the test set    
    if EVAL_ON_TEST_SET:
        params, scoring = run_experiment(full_set, test_set, run_id, feat_index, False, best_params, TEST_SET_NAME)
        evaluate_test_sets(RESULTS_FILE, run_id, params, scoring, TEST_SET_NAME, TEST_DATA_PATH)

#svm-rank
def run_split_sets_rank(run_id, splits, feat_index=''):
    print('--RUN_ID: ', run_id)
    ensure_required_directories_exist()

    set_parts = []

    if splits == 0:
        set_parts = comment_utils.split_set_in_parts_leave_1_question_out(DATA_PATH)
    else:
        set_parts = comment_utils.split_set_in_consecutive_parts(DATA_PATH, splits)

    full_set = []
    for i in range(0,len(set_parts)):
        full_set.extend(set_parts[i])

    test_set = comment_utils.read_comments(TEST_DATA_PATH)

    dev_features = []
    train_features = []
    # for comment in test_set:
    #     print(comment.comment_id, comment.label)

    if not os.path.exists(RESULTS_FILE):
        # If the results file does not exist - calcualte the baselines
        write_to_csv_file(['RUN-ID', 'Time', 'Params', 'Optimized for', 'SET', 'Accuracy', 'Precision', 'Recall', 'F1', 'MAP', 'Predictions', '', ''], RESULTS_FILE)
        calculate_baseline(full_set, 0, 'classification-baseline-all-negative', RESULTS_FILE)
        calculate_baseline(full_set, 1, 'classification-baseline-all-positive', RESULTS_FILE)
        if EVALUATE_WITH_SCORE:
            # If the results file does not exist - calcualte the baselines
            calculate_baseline_with_score(full_set, 'ranking-baseline-default-comment-order', RESULTS_FILE)
            calculate_baseline_with_score_oracle(full_set, 'ranking-baseline-oracle', RESULTS_FILE)
            calculate_baseline_with_score_random(full_set, 'ranking-baseline-random', RESULTS_FILE)

        if EVAL_ON_TEST_SET:
            # calculate baselines for test set
            calculate_baseline(test_set, 0, 'classification-baseline-all-negative', RESULTS_FILE, TEST_SET_NAME, TEST_DATA_PATH)
            calculate_baseline(test_set, 1, 'classification-baseline-all-positive', RESULTS_FILE, TEST_SET_NAME, TEST_DATA_PATH)
            if EVALUATE_WITH_SCORE:
                # If the results file does not exist - calcualte the baselines
                calculate_baseline_with_score(test_set, 'ranking-baseline-default-comment-order', RESULTS_FILE, TEST_SET_NAME, TEST_DATA_PATH)
                calculate_baseline_with_score_oracle(test_set, 'ranking-baseline-oracle', RESULTS_FILE, TEST_SET_NAME, TEST_DATA_PATH)
                calculate_baseline_with_score_random(test_set, 'ranking-baseline-random', RESULTS_FILE, TEST_SET_NAME, TEST_DATA_PATH)

        if INCLUDE_TEXT_BASELINES:
            calculate_baseline_bag_of_words(set_parts, 'baseline-bag-of-words', 1, 1, False, RESULTS_FILE)
            calculate_baseline_bag_of_words(set_parts, 'baseline-word-ngrams-2', 2, 2, False, RESULTS_FILE)
            calculate_baseline_bag_of_words(set_parts, 'baseline-word-ngrams-3', 3, 3, False, RESULTS_FILE)
            calculate_baseline_bag_of_words(set_parts, 'baseline-word-ngrams-4', 4, 4, False, RESULTS_FILE)
            # calculate_baseline_bag_of_words(set_parts, 'baseline-word-ngrams-1-2', 1, 2, False, RESULTS_FILE)
            # calculate_baseline_bag_of_words(set_parts, 'baseline-word-ngrams-1-3', 1, 3, False, RESULTS_FILE)
            # calculate_baseline_bag_of_words(set_parts, 'baseline-word-ngrams-2-3', 2, 3, False, RESULTS_FILE)
            # calculate_baseline_bag_of_words(set_parts, 'baseline-word-ngrams-1-4', 1, 4, False, RESULTS_FILE)
            # calculate_baseline_bag_of_words(set_parts, 'baseline-word-ngrams-2-4', 2, 4, False, RESULTS_FILE)
            # calculate_baseline_bag_of_words(set_parts, 'baseline-bag-of-words-tfidf', 1, 1, True, RESULTS_FILE)
            # calculate_baseline_bag_of_words(set_parts, 'baseline-word-ngrams-tfidf-2', 2, 2, True, RESULTS_FILE)
            # calculate_baseline_bag_of_words(set_parts, 'baseline-word-ngrams-tfidf-3', 3, 3, True, RESULTS_FILE)
            # calculate_baseline_bag_of_words(set_parts, 'baseline-word-ngrams-tfidf-4', 4, 4, True, RESULTS_FILE)
            # calculate_baseline_bag_of_words(set_parts, 'baseline-word-ngrams-tfidf-1-2', 1, 2, True, RESULTS_FILE)
            # calculate_baseline_bag_of_words(set_parts, 'baseline-word-ngrams-tfidf-1-3', 1, 3, True, RESULTS_FILE)
            # calculate_baseline_bag_of_words(set_parts, 'baseline-word-ngrams-tfidf-2-3', 2, 3, True, RESULTS_FILE)
            # calculate_baseline_bag_of_words(set_parts, 'baseline-word-ngrams-tfidf-1-4', 1, 4, True, RESULTS_FILE)
            # calculate_baseline_bag_of_words(set_parts, 'baseline-word-ngrams-tfidf-2-4', 2, 4, True, RESULTS_FILE)
            
    best_params, scoring, train_features, dev_features, dev_predicted, train_labels  = run_experiment_rank(full_set, full_set, run_id, feat_index, True)

    # for i in range(0,len(set_parts)):
    #     print('running experiments for split', i)
    #     train_set = list(full_set)
    #     dev_set = set_parts[i]
    #     for c in dev_set:
    #         train_set.remove(c)
    train_set = list(full_set)
    dev_set = []
    for i in range(83):
        dev_set.append(full_set[i])
        train_set.remove(full_set[i])
    params, scoring, train_features, dev_features, dev_predicted, train_labels  = run_experiment_rank(train_set, dev_set, run_id, feat_index, False, best_params)

    evaluate_test_sets(RESULTS_FILE, run_id, params, scoring)

    # predict and evaluate the test set    
    if EVAL_ON_TEST_SET:
        params, scoring = run_experiment(full_set, test_set, run_id, feat_index, False, best_params, TEST_SET_NAME)
        evaluate_test_sets(RESULTS_FILE, run_id, params, scoring, TEST_SET_NAME, TEST_DATA_PATH)

    return dev_set, train_set, dev_features, train_features, dev_predicted, train_labels

def calculate_baseline(data_set, baseline_label, baseline_name, results_file, set_name=SET_NAME, data_path=DATA_PATH):
    print('calculating baseline:', baseline_name, set_name)
    baseline_prediction_file = PREDICTIONS_PATH.substitute(set=set_name, run_id=baseline_name, time=timestamp)
    if os.path.exists(baseline_prediction_file):
        os.remove(baseline_prediction_file)
    for comment in data_set:        
        write_to_csv_file([comment.comment_id, baseline_label], baseline_prediction_file)
    baseline_eval = evaluate(data_path, baseline_prediction_file, results_file, baseline_name, set_name, data_path)
    result_line = [baseline_name, time_string, 'n/a', 'n/a']
    result_line.extend(baseline_eval)
    write_to_csv_file(result_line, results_file)

def calculate_baseline_with_score(data_set, baseline_name, results_file, set_name=SET_NAME, data_path=DATA_PATH):
    print('calculating baseline:', baseline_name, set_name)
    baseline_prediction_file = score_predictions_path(baseline_name, set_name)
    if os.path.exists(baseline_prediction_file):
        os.remove(baseline_prediction_file)
    for comment in data_set:
        write_to_csv_file([comment.comment_id, 1/cid_to_int_extracted(comment.comment_id)], baseline_prediction_file)
    baseline_eval = evaluate(data_path, baseline_prediction_file, results_file, baseline_name, set_name, data_path)
    result_line = [baseline_name, time_string, 'n/a', 'n/a']
    result_line.extend(baseline_eval)
    write_to_csv_file(result_line, results_file)

def calculate_baseline_with_score_random(data_set, baseline_name, results_file, set_name=SET_NAME, data_path=DATA_PATH):
    print('calculating baseline:', baseline_name, set_name)
    baseline_prediction_file = score_predictions_path(baseline_name, set_name)
    if os.path.exists(baseline_prediction_file):
        os.remove(baseline_prediction_file)
    for comment in data_set:
        write_to_csv_file([comment.comment_id, random.random()], baseline_prediction_file)
    baseline_eval = evaluate(data_path, baseline_prediction_file, results_file, baseline_name, set_name, data_path)
    result_line = [baseline_name, time_string, 'n/a', 'n/a']
    result_line.extend(baseline_eval)
    write_to_csv_file(result_line, results_file)

def calculate_baseline_with_score_oracle(data_set, baseline_name, results_file, set_name=SET_NAME, data_path=DATA_PATH):
    print('calculating baseline:', baseline_name, set_name)
    baseline_prediction_file = score_predictions_path(baseline_name, set_name)
    if os.path.exists(baseline_prediction_file):
        os.remove(baseline_prediction_file)
    for comment in data_set:
        #write_to_csv_file([comment.comment_id, comment.label], baseline_prediction_file)
        score = 0
        if comment.label == 1.0:
            score = 1+ 0.01*1/cid_to_int_extracted(comment.comment_id)
        else:
            score = 0.001*1/cid_to_int_extracted(comment.comment_id)
        #print('===SCORE===', score)
        write_to_csv_file([comment.comment_id, score], baseline_prediction_file)
    baseline_eval = evaluate(data_path, baseline_prediction_file, results_file, baseline_name, set_name, data_path)
    result_line = [baseline_name, time_string, 'n/a', 'n/a']
    result_line.extend(baseline_eval)
    write_to_csv_file(result_line, results_file)


def calculate_baseline_bag_of_words(set_parts, baseline_name, ngram_range_from, ngram_range_to, tfidf, results_file, set_name=SET_NAME, data_path=DATA_PATH):
    # Go through all the cross validation splits, build model and evaluate
    print('CALCULATING BASELINE', baseline_name)
    full_set_flat = [comment for sublist in set_parts for comment in sublist]
    full_set = [comment.text for sublist in set_parts for comment in sublist]
    full_set_labels = [comment.label for sublist in set_parts for comment in sublist]

    if tfidf:
        vectorizer = TfidfVectorizer(ngram_range=(ngram_range_from, ngram_range_to))
    else:
        vectorizer = CountVectorizer(ngram_range=(ngram_range_from, ngram_range_to))
    full_set_features = vectorizer.fit_transform(full_set)
    
    model, best_params, scoring = build_model(full_set_features, full_set_labels)

    for i in range(0,len(set_parts)):
        print('running experiments for split', i)
        train_set = list(full_set_flat)
        dev_set = set_parts[i]
        for c in dev_set:
            train_set.remove(c)
        params, scoring = run_experiment_word_baselines(train_set, dev_set, baseline_name, ngram_range_from, ngram_range_to, tfidf, False, best_params)

    # Evaluate the results from the written prediction file and save them in the results file
    evaluate_test_sets(RESULTS_FILE, baseline_name, best_params, scoring)



def ensure_required_directories_exist():
    ensure_directory_exists('../../../data/predictions')
    ensure_directory_exists('../../../data/results')
    ensure_directory_exists('../../../data/analysis')  # ANALYSIS

def ensure_directory_exists(f):
    if not os.path.exists(f):
        os.makedirs(f)   

def run_experiment(train_data, dev_data, run_id, feat_index='', full_set=False, params=None, set_name=SET_NAME):
    # Read the features
    train_features, train_labels = read_features(train_data, SET_NAME, feat_index)
    dev_features, dev_labels = read_features(dev_data, set_name, feat_index)
    #test_features, test_labels = read_features(test_data, TEST_SET_NAME, feat_index)

    # Scale the features
    min_max_scaler = MinMaxScaler()
    train_features = min_max_scaler.fit_transform(train_features)
    dev_features = min_max_scaler.transform(dev_features)

    # If the full set is passed, we want to just return the best params.
    # If a subset is passed, the passed params are used

    if full_set:
        model, best_params, scoring = build_model(train_features, train_labels)
    else:
        model, best_params, scoring = build_model(train_features, train_labels, params)
        # Predict the dev and train data        
        dev_predicted = model.predict(dev_features)
        if EVALUATE_WITH_SCORE:
            dev_predicted_scores = model.predict_proba(dev_features)

        print(dev_predicted)

        for (i,comment) in enumerate(dev_data):
            comment.predicted_label = dev_predicted[i]
            if EVALUATE_WITH_SCORE:
                add_ranking = 1/cid_to_int_extracted(comment.comment_id)*0.0000000001
                comment.predicted_score = dev_predicted_scores[i][1]+add_ranking
                


        # Write the predicted labels to file
        write_predictions_to_file(dev_data, predictions_path(run_id, set_name))
        if EVALUATE_WITH_SCORE:
            write_score_predictions_to_file(dev_data, score_predictions_path(run_id, set_name))
            # comment_utils.convert_scores_to_ranking_file_and_return_ranking_map(score_predictions_path(run_id, set_name), ranking_predictions_path(run_id, set_name))
            

    # evaluate and save the result
    return best_params, scoring

#svm-rank
def run_experiment_rank(train_data, dev_data, run_id, feat_index='', full_set=False, params=None, set_name=SET_NAME):
    # Read the features
    train_features, train_labels = read_features(train_data, SET_NAME, feat_index)
    dev_features, dev_labels = read_features(dev_data, set_name, feat_index)
    #test_features, test_labels = read_features(test_data, TEST_SET_NAME, feat_index)

    # Scale the features
    min_max_scaler = MinMaxScaler()
    train_features = min_max_scaler.fit_transform(train_features)
    dev_features = min_max_scaler.transform(dev_features)
    dev_predicted = []
    # If the full set is passed, we want to just return the best params.
    # If a subset is passed, the passed params are used

    if full_set:
        model, best_params, scoring = build_model(train_features, train_labels)
    else:
        model, best_params, scoring = build_model(train_features, train_labels, params)
        # Predict the dev and train data        
        dev_predicted = model.predict(dev_features)
        if EVALUATE_WITH_SCORE:
            dev_predicted_scores = model.predict_proba(dev_features)

        #print(dev_predicted)

        for (i,comment) in enumerate(dev_data):
            comment.predicted_label = dev_predicted[i]
            if EVALUATE_WITH_SCORE:
                add_ranking = 1/cid_to_int_extracted(comment.comment_id)*0.0000000001
                comment.predicted_score = dev_predicted_scores[i][1]+add_ranking
                


        # Write the predicted labels to file
        write_predictions_to_file(dev_data, predictions_path(run_id, set_name))
        if EVALUATE_WITH_SCORE:
            write_score_predictions_to_file(dev_data, score_predictions_path(run_id, set_name))
            # comment_utils.convert_scores_to_ranking_file_and_return_ranking_map(score_predictions_path(run_id, set_name), ranking_predictions_path(run_id, set_name))
            

    # evaluate and save the result
    return best_params, scoring, train_features, dev_features, dev_predicted, train_labels

def run_experiment_word_baselines(train_data, dev_data, run_id, ngram_range_from=1, ngram_range_to=1, tfidf = False, full_set=False, params=None, set_name=SET_NAME):
    # Get the numerical features from words in the comments
    train_features = []
    train_labels = []
    train_corpus = []
    for comment in train_data:
        train_corpus.append(comment.text)
        train_labels.append(comment.label)

    # if ngram_range_from == ngram_range_to and ngram_range_to == 1:
    #     vectorizer = CountVectorizer()
    #     print('v1')
    # else:
    if tfidf:
        vectorizer = TfidfVectorizer(ngram_range=(ngram_range_from, ngram_range_to))
    else:
        vectorizer = CountVectorizer(ngram_range=(ngram_range_from, ngram_range_to))
    train_features = vectorizer.fit_transform(train_corpus)

    # dev features
    dev_features = []
    dev_labels = []
    dev_corpus = []
    for comment in train_data:
        dev_corpus.append(comment.text)
        dev_labels.append(comment.label)

    dev_features = vectorizer.transform(dev_corpus)

    # Scale the features
    """
    NOT SCALING THE BAG-OF-WORDS FEATURES - TODO!!!
    """
    # min_max_scaler = MinMaxScaler()
    # train_features = min_max_scaler.fit_transform(train_features)
    # dev_features = min_max_scaler.transform(dev_features)

    # If the full set is passed, we want to just return the best params.
    # If a subset is passed, the passed params are used

    model, best_params, scoring = build_model(train_features, train_labels, params)
    # Predict the dev and train data        
    dev_predicted = model.predict(dev_features)
    if EVALUATE_WITH_SCORE:
        dev_predicted_scores = model.predict_proba(dev_features)

    print(dev_predicted)

    for (i,comment) in enumerate(dev_data):
        comment.predicted_label = dev_predicted[i]
        if EVALUATE_WITH_SCORE:
            add_ranking = 1/cid_to_int_extracted(comment.comment_id)*0.0000000001
            comment.predicted_score = dev_predicted_scores[i][1]+add_ranking
    
        # Write the predicted labels to file
        write_predictions_to_file(dev_data, predictions_path(run_id, set_name))
        if EVALUATE_WITH_SCORE:
            write_score_predictions_to_file(dev_data, score_predictions_path(run_id, set_name))
            # comment_utils.convert_scores_to_ranking_file_and_return_ranking_map(score_predictions_path(run_id, set_name), ranking_predictions_path(run_id, set_name))
            
    # evaluate and save the result
    return best_params, scoring


def write_predictions_to_file(data, file):
    for comment in data:
        write_to_csv_file([comment.comment_id, comment.predicted_label], file)

def write_score_predictions_to_file(data, file):
    for comment in data:
        write_to_csv_file([comment.comment_id, comment.predicted_score], file)

def evaluate_test_sets(results_file, run_id, best_params, scoring, set_name=SET_NAME, data_path=DATA_PATH):
    # write header:
    if not os.path.exists(results_file):
        write_to_csv_file(['RUN-ID', 'Time', 'Params', 'Optimized for', 'SET', 'Accuracy', 'Precision', 'Recall', 'F1', 'MAP', 'Predictions', '', ''], results_file)

    result_line = [run_id, time_string, best_params, scoring]

    dev_eval = evaluate(data_path, predictions_path(run_id, set_name), results_file, run_id, set_name, data_path)

    result_line.extend(dev_eval)

    write_to_csv_file(result_line, results_file)


def calculate_map(p, gold_labels_file, score_predictions_file):
    gold_labels = comment_utils.read_comment_labels_from_xml(gold_labels_file)
    predicted_scores = comment_utils.read_comment_scores_from_tsv(score_predictions_file)

    # print(gold_labels)
    # print(predicted_scores)

    map_value = 0
    scores = {}

    counter = 0

    # Put all values in a map for each query
    for comment_id, predicted_score in predicted_scores.items():
        qid = qid_from_cid(comment_id)
        gold_label = gold_labels[comment_id]
        add_ranking = 1/cid_to_int_extracted(comment_id)*0.0000000001
        if not qid in scores.keys():
            scores[qid] = {}
        scores[qid][predicted_score+add_ranking] = gold_label

    for query, score_label_mapping in scores.items():
        # print(score_label_mapping.values())
        if 1 in score_label_mapping.values() and sum(score_label_mapping.values()) < len(score_label_mapping.values()):
            counter += 1
            # print(query, score_label_mapping)
            sorted_scores = sorted(score_label_mapping.keys(), reverse=True)
            average_precision = 0
            limit = min(p, len(sorted_scores))

            count_positive_labels = 0
            for i in range(0,limit):
                score = sorted_scores[i]
                label = score_label_mapping[score]
                #print(score, label)
                if label == 1:
                    count_positive_labels += 1
                    average_precision += count_positive_labels/(i+1)
            # print(count_positive_labels, i+1)
            map_value += average_precision / count_positive_labels
            # print('ap, limit, map=', average_precision, limit, map_value)
        # else:
        #     print('exclude', score_label_mapping )

    # print(map_value, len(scores.items()), counter)

    map_value /= counter

    # print(map_value)
    # print(counter)

    return map_value


def evaluate(gold_labels_file, prediction_file, results_file, run_id, set_name, data_path=DATA_PATH):
    gold_labels = comment_utils.read_comment_labels_from_xml(gold_labels_file)
    predicted_labels = comment_utils.read_comment_labels_from_tsv(prediction_file)

    # ANALYSIS
    analysis_file = analysis_path(run_id, set_name)
    row_arr = ['Comment ID', 'Predicted Label', 'Gold Label']
    write_to_csv_file(row_arr, analysis_file)

    true_positives = 0
    false_positives = 0
    true_negatives = 0
    false_negatives = 0

    print('evaluate...')

    for comment_id, predicted_label in predicted_labels.items():
        gold_label = gold_labels[comment_id]

        row_arr = [comment_id, predicted_label, gold_label]
        write_to_csv_file(row_arr, analysis_file)
        
        if gold_label == 1 and predicted_label == 1:
            true_positives += 1
        elif gold_label == 1 and predicted_label == 0:
            false_negatives += 1
        elif gold_label == 0 and predicted_label == 0:
            true_negatives += 1
        elif gold_label == 0 and predicted_label == 1:
            false_positives += 1

    confusion_matrix = 'TP=' + str(true_positives) + ', FP=' + str(false_positives) + ', TN=' + str(true_negatives) + ', FN=' + str(false_negatives) 
    confusion_matrix2 = 'PredictedYES='+str((true_positives+false_positives))+', ActualYES='+str((true_positives+false_negatives))
    confusion_matrix3 = 'PredictedNO='+str((true_negatives+false_negatives))+', ActualNO='+str((true_negatives+false_positives))

    print(true_positives, false_positives, true_negatives, false_negatives)

    accuracy = (true_positives + true_negatives)/(true_positives+true_negatives+false_positives+false_negatives)
    if true_positives+false_positives > 0:
        precision = true_positives/(true_positives+false_positives)
    else:
        precision = 'n/a'

    recall = true_positives/(true_positives+false_negatives)

    f1 = 2*true_positives/(2*true_positives + false_negatives + false_positives)

    map_value = 'n/a'
    if EVALUATE_WITH_SCORE:
        # first try to calculate the map on ranking
        if os.path.exists(ranking_predictions_path(run_id, set_name)):
            path = ranking_predictions_path(run_id, set_name)
            map_value = calculate_map(20, data_path, path)
        elif os.path.exists(score_predictions_path(run_id, set_name)):
            path = score_predictions_path(run_id, set_name)
            map_value = calculate_map(20, data_path, path)
        elif os.path.exists(predictions_path(run_id, set_name)):
            path = predictions_path(run_id, set_name)
            map_value = calculate_map(20, data_path, path)

    return [set_name, accuracy, precision, recall, f1, map_value, confusion_matrix, confusion_matrix2, confusion_matrix3]

def read_features_from_index(data, set_name, feat_index):
    #set_name = 'dev+test'
    print('---Reading features from index for ' + set_name, feat_index) 
    X = []
    y = []
    if isinstance(feat_index, list):
        features_map = FeatureSets.read_feature_sets(set_name, feat_index)
    else:
        features_map = FeatureSets.read_feature_set(set_name, feat_index)
    for comment in data:
        # Set the features for each
        if comment.comment_id in features_map.keys():
            pair_x = features_map[comment.comment_id]
            X.append(pair_x)
            y.append(comment.label)

    return X, y    


def read_features(data, set_name, feat_index):
    if len(feat_index) > 0:
        return read_features_from_index(data, set_name, feat_index)

    print('Reading features for set: ' + set_name)    
    X = []
    y = []
    features_map = {}

    features_map = Features.add_features(features_map, Features.read_question_word_presence_features(set_name))

    # TODO: Read more features

    for question in data:
        # Set the features for each
        question_x = features_map[question.qid]
        X.append(question_x)
        y.append(question.label)

    return X, y

    
def build_model(X, y, params = None, scoring='accuracy'):
    
    print('Building model...', params)
    # clf = LinearSVC(C=4)
    # clf.fit(X, y)

    # If params are given, use them for the classifier
    # Otherwise - perform grid search to find the best params
    if params:
        print('Training with predefined params...')
        clf = SVC(**params)
    else:
        print('Perform grid search for finding the best params...')
        param_grid = [
            {'C': [0.025, 0.25, 0.5, 1, 2, 4, 8, 16, 32, 64, 100, 128, 256, 500, 1000], 'kernel': ['linear'], 'probability': [True]},
            {'C': [0.025, 0.25, 0.5, 1, 2, 4, 8, 16, 32, 64, 100, 128, 256, 500, 1000], 'gamma': [2, 1, 0.5, 0.3, 0.2, 0.1, 0.01, 0.001, 0.0001], 'kernel': ['rbf'], 'probability': [True]},
        ]
        svr = SVC()
        k=StratifiedKFold(n_splits=5, shuffle=False)
        clf = GridSearchCV(svr, param_grid, scoring=scoring, cv=k)

    #clf = SVC(C=2, gamma=0.2)
    clf.fit(X, y)

    if isinstance(clf, GridSearchCV):
        print("best params: ", clf.best_params_)
        print("best score: ", clf.best_score_)
        print("best estimator: ",  clf.best_estimator_)

        return clf, clf.best_params_, scoring
    else:
        return clf, clf.get_params(False), scoring

#Use these models instead of build_model method in case of checking with Naive Bayes,Logistic Regression or Random Forest
# ANALYSIS FOR NAIVE BAYES
def build_model_guassian(X, y, params = None, scoring='accuracy'):
    
    print('Building Model Gaussian Naive Bayes ...')
    clf = GaussianNB()
    clf.fit(X, y)

    return clf, clf.get_params(False), scoring

#ANALYSIS FOR LOGISTIC REGRESSION
def build_model_logistic(X, y, params = None, scoring = 'accuracy'):
    print('Using Logistic Regression')

    print('Perform grid search for finding the best params...')
    param_grid = {'C': [0.025, 0.25, 0.5, 1, 2, 4, 8, 16, 32, 64, 100, 128, 256, 500, 1000]}
    clf = LogisticRegression(solver = 'liblinear')
    clf = GridSearchCV(clf, param_grid, scoring=scoring)    
    clf.fit(X,y)
    if isinstance(clf, GridSearchCV):
        print("best params: ", clf.best_params_)
        print("best score: ", clf.best_score_)
        print("best estimator: ",  clf.best_estimator_)

        return clf, clf.best_params_, scoring
    else:
        return clf, clf.get_params(False), scoring


#ANALYSIS FOR RANDOM FOREST
def build_model_random(X, y, params = None, scoring='accuracy'):
    
    print('Building Model Random Forest ...')   
    param_grid = {
    'max_depth': [3,5,6],
    'max_features': ['auto'],
    'n_estimators': [5,15,20]
    }
    rndf = RandomForestClassifier(random_state = random.seed(1234))
    #Remove this line in case of testing with Stratified K-Fold
    clf = GridSearchCV(rndf, param_grid, scoring=scoring,cv=5)
    #add these lines in case of testing with Stratified K-Fold
    #k=StratifiedKFold(n_splits=5, shuffle=False)
    #clf = GridSearchCV(rndf, param_grid, scoring=scoring,cv=k)
    clf.fit(X, y)

    if isinstance(clf, GridSearchCV):
        print("all possible combinations:",clf.cv_results_)
        print("best params: ", clf.best_params_)
        print("best score: ", clf.best_score_)
        print("best estimator: ",  clf.best_estimator_)

        return clf, clf.best_params_, scoring
    else:
        return clf, clf.get_params(False), scoring

    
def write_output(pairs, set_name, run_id):
    # output for svmrank
    file = '../output/svmrank/min2/'+run_id+'-'+set_name+'.out'
    result = {}
    for pair in pairs:
        qid_int = qid_to_int(pair.question_id)
        cid_int = cid_to_int(pair.comment_id)
        if not qid_int in result.keys():
            result[qid_int] = {}
        result[qid_int][cid_int] = [pair.question_id, pair.comment_id, pair.probability, pair.predicted_label]

    for qid in sorted(result):
        comments = result[qid]
        for cid in sorted(comments):
            label = 'true' if comments[cid][3] == 1 else 'false'
            arr = [comments[cid][0], comments[cid][1], 0, comments[cid][2], label]
            write_to_csv_file(arr, file)

def qid_to_int(qid):
    part1q = qid[qid.find('Q')+1:qid.find('_R')]
    part2q = qid[qid.find('_R')+2:]
    resq = int(part1q)*10000000 + int(part2q)*1000
    return resq

def qid_from_cid(cid):
    return cid[cid.find('Q'):cid.find('_C')]

def cid_to_int(cid):
    part1c = cid[cid.find('Q')+1:cid.find('_R')]
    part2c = cid[cid.find('_R')+2:cid.find('_C')]
    part3c = cid[cid.find('_C')+2:]
    resc = int(part1c)*10000000 + int(part2c)*1000 + int(part3c)
    return resc

def cid_to_int_extracted(cid):
    return int(cid[cid.find('_C')+2:])
    

def write_to_csv_file(array, file_path):
    with open(file_path, 'a+', newline='') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter='\t', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(array)

