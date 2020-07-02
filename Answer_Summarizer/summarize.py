import re
import csv
import nltk
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyser = SentimentIntensityAnalyzer()

def sentiment_analyzer_scores(sentence):
    score = analyser.polarity_scores(sentence)
    val = list(score.values())
    return(val[3])
    #print("{:-<40} {}".format(sentence, str(score)))



with open('where.csv', 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    features = []
    for row in reader:
        sen = re.split('[,;.]',row[5])
        sentences = []
        for i in range(len(sen)):
            sen_score = sentiment_analyzer_scores(sen[i])
            if(sen_score > -0.05):
                sentences.append(str(sen[i]))
        if(len(sentences)!=0):
            feat = [row[0],row[1],sentences]
            features.append(feat)   
    #print(features)
    for i in range(len(features)):
        list_sentence=features[i][2]
        print(list_sentence)
        extracted=[]
        for k in range(len(list_sentence)):
            sent=list_sentence[k]
            tokens=nltk.word_tokenize(sent)
            pos_list=nltk.pos_tag(tokens)
            if(len(sent)<=5):
                #print(len(sent))
                j=0
                while j < len(pos_list):
                    if pos_list[j][1]=='NNP':
                        extracted.append(pos_list[j][1])
                        j=j+1
                    elif pos_list[j][1]=='IN':
                        j=j+1
                        if j<len(pos_list):
                            l=j+1
                            if(l < len(pos_list)):
                                while pos_list[l][1] !='IN' or l<len(pos_list):
                                    if j<len(pos_list):
                                        if((pos_list[j][1]=='NN' and pos_list[j][0][0].isupper()=='True') or (pos_list[j][1]=='NNP')):
                                            extracted.append(pos_list[j][0])
                                            l=l+1
                                            j=j+1
                                        else:
                                            j=j+1
                                            l=l+1
                        j=j+1
                    elif pos_list[j][0][0].isupper()=='True':
                        extracted.append(pos_list[n][0])
                        j=j+1
                    else:
                        j=j+1
            else:

                n=0
                while n < len(pos_list):

                    if pos_list[n][1]=='IN':
                        n=n+1
                        if n<len(pos_list):
                            k=n+1
                            if(k < len(pos_list)):
                                while k < len(pos_list) and pos_list[k][1] !='IN':
                                    if n<len(pos_list):
                                        if (pos_list[n][1] == 'NN' and pos_list[n][0][0].isupper()=='True') or pos_list[n][1] == 'NNP':
                                            extracted.append(pos_list[n][0])
                                            n=n+1
                                            k=k+1
                                        else:
                                            n=n+1
                                            k=k+1
                        n=n+1
                    elif pos_list[n][0][0].isupper()=='True':
                        extracted.append(pos_list[n][0])
                        n=n+1
                    else:
                        n=n+1

        print(extracted)
   

