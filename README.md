# FCPLus
Fact Checking in CQA Forums
This project is based on the work done in: [Fact Checking in Community Forums](https://arxiv.org/pdf/1803.03178.pdf)

## **Intructions for Reproducing Results**

### Running Category-Wise Experiments
From the present working directory, follow the commands:
```
cd QLFactChecker/code/classification/answers
python3 RunMultiply.py 
```
Once the run is complete:
- Results file will be created in QLFactChecker/data/results
- The result file contains category-wise results (including our proposed feature-categories)

### Running Combined-Feature Results
- For running combined, feature results, first obtain the above category-wise results
- Once, complete, follow the instructions as bellow:
- For first method:
```
cd QLFactChecker/code/classification/answers
python3 combine_best_feature_groups.py 
```

- For second method:
```
cd QLFactChecker/code/classification/answers
python3 combine_best_feature_groups_feedforward.py
```
**NOTE** : By running the above commands, the combined-category results produced will be the ones that will include our proposed-feature sets by default.
To get the original set of results, comment line 37 in combine_best_feature_groups.py and uncomment line 36.

### To Run other classifiers
- To run the Naive Bayes Classifier, replace the "build_model" by "build_model_guassian" in QLFactChecker/code/classification/answers/RunCV.py file.
- To run the Random Forest Classifier, replace the "build_model" by "build_model_random" in QLFactChecker/code/classification/answers/RunCV.py file.
- To run the Logistic Regression Classifier, replace the "build_model" by "build_model_logistic" in QLFactChecker/code/classification/answers/RunCV.py file.

### Running SVM-Rank
Delete the csv file under QLFactChecker/data/results and issue the following commands:
```
cd QLFactChecker/code/classification/answers
python3 RunMultiply.py 
python3 RunSVMRank.py
```
After the run is complete:
- Statistics for SVM-Rank results will be present in QLFactChecker/svm_rank_results.csv
- Ordered comments, as per SVM-Rank Ranking will be found in svm_ranked_comments/*
- The bm25 scores can be found in QLFactChecker/bm25_scores.csv that is used as ground truth rankings.

### Creating Proposed Feature Files
- Prerequisite:
  -Install TweetNLP. Please follow the following link to install it.
    
    https://code.google.com/archive/p/ark-tweet-nlp/downloads
  
- Our result files for the Combined feature set runs with proposed features can be found in QLFactChecker/Proposed_Features_Combined_Results/*
- Feature files for the proposed feature set can be found under QLFactChecker/data/features, by the name:
  - semeval2016-dev+test-with-annotations-clear-true-false-only.xml.tab_format.readability
  - semeval2016-dev+test-with-annotations-clear-true-false-only.xml.tab_format.user_expertise
  - semeval2016-dev+test-with-annotations-clear-true-false-only.xml.tab_format.answer_quality
- In order to reproduce the feature file for USER_EXPERTISE CATEGORY, run
```
cd QLFactChecker
python3 create_user_expert_feat.py
```
Results will be created in present directory with the file name as 'user_expertise.csv'

### Summarizing Answer (Extension)
- Prerequisite:
  - Install 'vader'.
    ```
    pip install vaderSentiment
    ```
- To run the code:
```
cd Answer_Summarizer
python3 summarize.py

```