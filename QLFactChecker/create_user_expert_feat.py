import csv
import string
import xml.etree.ElementTree as ET
import math

import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.translate.bleu_score import sentence_bleu
import gensim.summarization

user_feature_map = dict()
user_categories = dict()
user_answers=dict()
user_ques=dict()
user_num_answers_to_ques=dict()

nist_overlap=dict()

SET_NAME = 'dev+test'
XML_FILE = 'data/input/input-'+SET_NAME+'.xml'

# Parse XML File to get strucured data
def get_user_features(xml_file):    
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    threads_count = 0
    for thread in root:
        threads_count += 1
    
    for thread in root:
        question_tag = thread[0]
        
        asker = question_tag.attrib['RELQ_USERID']
        question_category = question_tag.attrib['RELQ_CATEGORY']
        question_fact_label=question_tag.attrib['RELQ_FACT_LABEL']
        
        if asker in user_ques:
            user_ques[asker]+=1
        else:
            user_ques[asker]=1
        
        num_of_answers=len(thread.findall('RelComment'))
        
        if question_fact_label == 'Single Question - Factual':
            for index, comment_tag in enumerate(thread):
                if index>0:
                    comment_user = comment_tag.attrib['RELC_USERID']
            
                    if comment_user in user_answers:
                        user_answers[comment_user]+=1
                    else:
                        user_answers[comment_user]=1
                    
                    if comment_user in user_categories:
                        user_categories[comment_user].add(question_category)
                    else:
                        user_categories[comment_user]={question_category}
                    
                    if comment_user in user_num_answers_to_ques:
                        user_num_answers_to_ques[comment_user].append(num_of_answers)
                    else:
                        user_num_answers_to_ques[comment_user] = [num_of_answers]

# Function to calculate z-score for a particular user
def calculate_z_score(user_id):
    if(user_id in user_answers) and (user_id in user_ques):
        z_score = (user_answers[user_id]- user_ques[user_id])/math.sqrt(user_answers[user_id]+user_ques[user_id])
        return z_score
    else:
        z_score = (user_answers[user_id])/math.sqrt(user_answers[user_id])
        return z_score

# Function to calculate category-expertise for a particular user
def calc_category_expertise(user_id):
    if(user_id in user_answers) and (user_id in user_categories):
        num_cat = len(user_categories[user_id])
        return (user_answers[user_id]/num_cat)
    else:
        return 0

# Functoin to calculate BM25 Score for Q-A thread, used for SVM-RANK
def get_bm25_score(question, comments, comment_ids):
    print(comment_ids)
    file="bm25_scores.csv"
    user_exp = open(file, "a",  encoding="utf8")
    feat_writer = csv.writer(user_exp, delimiter="\t")
    corpus = []
    for comment in comments:
        if question is not None and comment is not None:
         answer = comment.split()
         # print(answer)
         corpus.append(answer)
    
    if(len(corpus)>0):
        bm25_obj = gensim.summarization.bm25.BM25(corpus)
        #bm25_obj.initialize()
        average_idf = sum(map(lambda k: float(bm25_obj.idf[k]), bm25_obj.idf.keys())) / len(bm25_obj.idf.keys())

        for (i,comment) in enumerate(comments):
            if question is not None and comment is not None:
                row = []
                score = bm25_obj.get_score(question, i, average_idf)
                row.append(comment_ids[i])
                row.append(score)
                print(row)
                feat_writer.writerow(row)

# Function to calculate the difficulty of answers that user answers
def user_answer_difficulty(user_id):
    file="user_answer_diff.csv"
    user_diff = open(file, "a",  encoding="utf8")
    feat_writer = csv.writer(user_diff, delimiter="\t")
    row = []
    row.append(user_id)
    if(user_id in user_answers) and (user_id in user_num_answers_to_ques):
        sum_frac = 0.0
        for num in user_num_answers_to_ques[user_id]:
            sum_frac += 1.0/num
        sum_frac = sum_frac/user_answers[user_id]
        row.append(sum_frac)
        feat_writer.writerow(row)
        return sum_frac
    else:
        row.append(0)
        feat_writer.writerow(row)
        return 0

# Function to calculate N-Gram Overlap for a Q-A pair
# NOTE: This is not used in final feature sets anymore due to poor performance
def calculate_n_gram_overlap(question, answer, comment_id):
    #file="n_gram_overlap.csv"
    n_gram = open(file, "a",  encoding="utf8")
    feat_writer = csv.writer(n_gram, delimiter="\t")

    stop = stopwords.words('english')
    row = []
    row.append(comment_id)
    if question is not None and answer is not None:
        # print("Question  : ", question)
        # print("Answer : ", answer)

        q_tokens=question.split()
        a_tokens=answer.split()


        question_tokens = []
        comment_tokens = []

        for token in q_tokens:
            token = token.strip()
            if token not in stop:
                question_tokens.append(token)

        for token in a_tokens:
            token = token.strip()
            if token not in stop:
                comment_tokens.append(token)

        # print("Question Tokens : ", question_tokens)
        # print("Answer : ", comment_tokens)
        references = [question_tokens]
        candidates = comment_tokens

        score = sentence_bleu(references, candidates, weights=(1, 0, 0, 0))
        row.append(score)

        feat_writer.writerow(row)
        # print("Score : ", score)
        # print("\n")
        

# Creating the feature file to be used    
def create_user_feature_file():
    file="user_expertise.csv"
    user_exp = open(file, "w",  encoding="utf8")
    feat_writer = csv.writer(user_exp, delimiter="\t")

    tree = ET.parse(XML_FILE)
    root = tree.getroot()
    for thread in root:
        question_tag = thread[0]
        question_fact_label=question_tag.attrib['RELQ_FACT_LABEL']
        question_text = question_tag[1].text
        answer_row = []
        comment_ids = []
        if question_fact_label == 'Single Question - Factual':
            for index, comment_tag in enumerate(thread):
                if index>0:
                    row = []
                    comment_user = comment_tag.attrib['RELC_USERID']
                    comment_id = comment_tag.attrib['RELC_ID']
                    comment_text = comment_tag[0].text
                    row.append(comment_id)
                    row.append(calculate_z_score(comment_user))
                    row.append(calc_category_expertise(comment_user))
                    row.append(user_answer_difficulty(comment_user))
                    answer_row.append(comment_text)
                    comment_ids.append(comment_id)
                    feat_writer.writerow(row)
                    calculate_n_gram_overlap(question_text, comment_text, comment_ids)
                    row=[]
            get_bm25_score(question_text, answer_row, comment_ids)


    user_exp.close()

get_user_features(XML_FILE)
create_user_feature_file()