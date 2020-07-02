import sys
import operator
import numpy as np
sys.path.insert(0, '../../data/features/')

import csv, os, random, operator
import string
import time

from comment import Comment
import comment_utils
import Features
import FeatureSets

import RunCV
from gensim.summarization.bm25 import get_bm25_weights

# This is the index of the column of the result we are comparing in the results file.
ACCURACY_INDEX = 5
MAP_INDEX = 9

# To change whether runs should be sorted by accuracy or MAP, change the values below:
RESULT_SCORE_INDEX = ACCURACY_INDEX
RUN_PREFIX = 'TOP_'

SET_NAME = 'dev+test'
RESULTS_FILE = "../../../data/results/results-answers-cross-validation-"+SET_NAME+".tsv"

TOP_N_FROM = 2
TOP_N_TO = 40

test_comment_order_list=[]

# The main function called to prduce SMV-Rank Results
def read_results_overall():
    best_results = read_best_results()
    max_index = min(TOP_N_TO, len(best_results))
    
    groups_names = []
    groups_names_str = ''
    for i in range(0, max_index):
        n = i+1
        index_name = RUN_PREFIX+str(n)
        groups_names.append(best_results[i][0])
        if groups_names_str != '':
            groups_names_str += ', '    
        groups_names_str += best_results[i][0]

        #Running for Top-N Feature Sets
        if n >= TOP_N_FROM:
            run_id = index_name + ' ('+groups_names_str + ')'
            print('!!! Running...', run_id)
            test_set, train_set, dev_features, train_features, dev_predicted, train_labels = RunCV.run_rank(run_id, groups_names)
            
            # Function to create train_input for svm-rakn
            create_svm_rank_input(test_set, train_set, dev_features, train_features, dev_predicted, train_labels,run_id)
            # Function to creat test_input for svm-rank
            create_svm_rank_test(test_set, train_set, dev_features, train_features, dev_predicted, run_id)
            # Run SVM-Rank
            run_svm_rank(run_id)
            # Parse SVM-Rank Output and produce statistics
            parse_svm_rank_output(run_id)
            # Output the question-answer threads, with answers ranked according to
            # SVM-Rank
            create_ranked_commments(run_id, test_set)

# Helper Function to display train-data set
def display_dev_features(dev_features):
	np.savetxt('dev.out',dev_features,delimiter=',')
	

#  Helper Function to create test-data set
def display_test_set(test_set):
	file='display_test'
	file_open=open(file,"w")
	for (i,item) in enumerate(test_set):
		file_open.write(str(item.question_id))
		file_open.write("         ")
		file_open.write(str(item.comment_id))
		file_open.write("\n")
	file_open.close()

# Function to read best category-wise results
def read_best_results():
    group_scores = {}
    with open(RESULTS_FILE,encoding="utf8") as csvfile:
        csvreader = csv.reader(csvfile, delimiter='\t')
        for row in csvreader:
            group = row[0]
            score = row[RESULT_SCORE_INDEX]
            if (group.endswith('-incl')):
                group_scores[group] = score
                
    sorted_group_scores = sorted(group_scores.items(), key=operator.itemgetter(1), reverse=True)
    return sorted_group_scores

# Function to return bm25 scores
def get_bm25_score(comment_id):
	with open("../../../bm25_scores.csv",encoding="utf8") as csvfile:
		csvreader = csv.reader(csvfile, delimiter='\t')
		for row in csvreader:
			if(row[0] == comment_id):
				return row[1]

		return 0

# Function to create input file for SVM-Rank, for train-set
def create_svm_rank_input(test_set, train_set, dev_features, train_features, dev_predicted, train_labels, run_id):
	#Create SVM-Rank input for train set
	file="../../../svm_rank/train_set_"+str.rstrip(str(run_id)[:6])+".dat"
	train_set_svm_rank = open(file, "w")

	question_number=1
	train_writer = csv.writer(train_set_svm_rank, delimiter=' ')
	curr_qid = ''
	#prev_qid = ''
	ground_truth_rank=1
	row = []
	for (i,item) in enumerate(train_set):
		if(train_labels[i] == 1):
			if(curr_qid == ''):
				curr_qid = item.question_id
			if(curr_qid != item.question_id):
				curr_qid = item.question_id
				ground_truth_rank=1
				question_number+=1
			
			row.append(get_bm25_score(item.comment_id))
			ground_truth_rank = ground_truth_rank + 1
			row.append("qid:"+str(question_number))
			feat_num = 1 ;
			#for key,value in train_features.items():
			for feat_value in range(len(train_features[i])):
				feature = str(feat_num) + ":" + str(train_features[i][feat_value])
				feat_num += 1
				row.append(feature)
			train_writer.writerow(row)
			row=[]
	train_set_svm_rank.close()

# Function to create input file for SVM-Rank, for test-set
def create_svm_rank_test(test_set, train_set, dev_features, train_features, dev_predicted,run_id):
	
	#Create SVM-Rank input for test set
	file="../../../svm_rank/test_set_"+str.rstrip(str(run_id)[:6])+".dat"
	test_set_svm_rank = open(file, "w")
	test_writer = csv.writer(test_set_svm_rank, delimiter=' ')
	curr_qid = ''
	#prev_qid = ''
	question_number=1
	ground_truth_rank=1
	row = []
	for (j,item) in enumerate(test_set):
		if(item.predicted_label == 1):
			if(curr_qid == ''):
					curr_qid = item.question_id
			if(curr_qid != item.question_id):
				curr_qid = item.question_id
				ground_truth_rank=1
				question_number+=1
			
			row.append(get_bm25_score(item.comment_id))
			ground_truth_rank = ground_truth_rank + 1
			row.append("qid:"+str(question_number))
			feat_num = 1 ;
			print(dev_features.shape)
			for feat_value in range(len(dev_features[j])):
				feature = str(feat_num) + ":" + str(dev_features[j][feat_value])
				feat_num += 1
				row.append(feature)
			test_writer.writerow(row)
			test_comment_order_list.append(item.comment_id)
			row=[]
	test_set_svm_rank.close()
	# print(test_comment_order_list)

# Actually, run SVM Rank and Save Logs
def run_svm_rank(run_id):
	#Command to train
	input_file = "../../../svm_rank/train_set_"+str.rstrip(str(run_id)[:6])+".dat"
	model_file = "../../../svm_rank/model_"+str.rstrip(str(run_id)[:6])
	param_c = 20
	train_cmnd = "../../../svm_rank/svm_rank_learn -c "+str(param_c)+" "+input_file+" "+model_file

	os.system(train_cmnd)

	#Command to test
	test_file="../../../svm_rank/test_set_"+str.rstrip(str(run_id)[:6])+".dat"
	prediction="../../../svm_rank/predictions/prediction_"+str.rstrip(str(run_id)[:6])
	
	out_temp="../../../svm_rank/stats/stats_"+str.rstrip(str(run_id)[:6])+".txt"
	test_cmnd="../../../svm_rank/svm_rank_classify "+test_file+" "+model_file+" "+prediction+" >"+out_temp
	os.system(test_cmnd)

# Produce Statistics file for SVM-Rank Results
def parse_svm_rank_output(run_id):
	
	stat_file = open("../../../svm_rank/stats/stats_"+str.rstrip(str(run_id)[:6])+".txt", "r")
	content = stat_file.readlines()

	out_file = open("../../../svm-rank_results"+".csv", "a")
	out_writer = csv.writer(out_file, delimiter="\t")

	row = ["Run_ID", "Average Loss", "Zero/one-Error", "Total Num Swapped Pairs", "Avg Swapped Pairs %"]
	out_writer.writerow(row)
	row = []
	line = content[4]
	index = line.find(':')
	value =''

	row.append(run_id)
	if(index!=-1):
		value=line[index+1:]
	else:
		value="NA"
	row.append(value)	

	line=content[5]
	index = -1
	index = line.find(':')
	value =''
	if(index!=-1):
		value=line[index+1:]
	else:
		value="NA"
	row.append(value)
		
	line=content[9]
	index = -1
	index = line.find(':')
	value =''
	if(index!=-1):
		value=line[index+1:]
	else:
		value="NA"
	row.append(value)
		
	line=content[10]
	index = -1
	index = line.find(':')
	value =''
	if(index!=-1):
		value=line[index+1:]
	else:
		value="NA"
	row.append(value)

	out_writer.writerow(row)
	out_file.close()

# Produce Output file Question-Answer Threads ranked according to SVM-Rank Results
def create_ranked_commments(run_id, test_data):

	prediction="../../../svm_rank/predictions/prediction_"+str.rstrip(str(run_id)[:6])
	comment_score = dict()
	id_list = []
	out_file = open(prediction, "r")
	reader = csv.reader(out_file, delimiter="\t")

	ranked_output  = open("../../../svm_rank_output/svm_ranked_comments_"+str.rstrip(str(run_id)[:6])+".txt", "a")

	i = 0
	parts = []
	qtext = ''
	prev_qtext = ''
	for val in reader:
		if(qtext == ''):
			qtext = test_data[i].question_id
			prev_qtext = qtext

		qtext = test_data[i].question_id

		if(prev_qtext != qtext):
			parts.append(comment_score)
			comment_score = {}
			prev_qtext = qtext
		
		comment_score[test_data[i].comment_id] = val[0]
		i+=1

	for dictionary in parts:
		sorted_d = sorted(dictionary.items(), key=operator.itemgetter(1))
		first = 0
		for key,val in sorted_d:	
			for (i,comment) in enumerate(test_data):
				if(comment.comment_id == key):
					if(first==0):
						ranked_output.write("QUESTION: "+comment.qbody+"\n")
						first+=1
					ranked_output.write("\t COMMENT : "+comment.text+"\n")
					break;
		ranked_output.write("\n *******************\n")	

read_results_overall()
