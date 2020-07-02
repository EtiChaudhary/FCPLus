setwd("//home//ksravindrababu//IR_proj")
d = read.csv("Comments_with_pos.tsv",header=FALSE,stringsAsFactors = FALSE,sep = '\t')
newdat=data.frame()
#Lexical density
pp=d$V9
p1=c("N","V","A","R")
G=strsplit(pp, " ")
lev=p1
G1 = do.call(rbind,lapply(G,function(x,lev)
{ table(factor(x,levels = lev,
               ordered = TRUE))},
lev = lev))
library(stringr)
tot = str_count(pp, '\\s+')+1
o=G1/tot
G2=rowSums(o)
newdat=cbind(d$V2,G2)


#Counts of each pos tag

p=c("N","O","S","^","Z","V","A","R","!","D","P","&","T","X","#","@","~","U","E","$",",","G","L","M","Y")
lev=p
G1 = do.call(rbind,lapply(G,function(x,lev)
{ table(factor(x,levels = lev,
               ordered = TRUE))},
lev = lev))

tot = str_count(pp, '\\s+')+1 
o=G1/tot
o=as.data.frame(o)
newdat=cbind(newdat,o)

#Grammatical errors

comm_text=str_replace(gsub("\\s+", " ", str_trim(d$V6)), "B", "b")
#next_word_your=str_extract(comm_text, '(?<=your\\s)\\w+')
next_word_its=str_extract(comm_text, '(?<=its\\s)\\w+')

write.csv(next_word_its,"its_col.csv",row.names = F)

#Add the tag### 

dat_its_tag=read.csv("its_col.csv",header=F,stringsAsFactors = F,sep='\t')
its_data = within(dat_its_tag, {
  new_its = ifelse(V2 == "V"|V2=="R"|V2=="D", 1, 0)
})

newdat=cbind(newdat,its_data$new_its)
#Dictionary words for checking typos
dic = read.csv("removed_prop_nouns_comm.csv",header=FALSE,stringsAsFactors = FALSE)
library(qdapDictionaries)
dic$V2=tolower(dic$V2)
p=strsplit(dic$V2," ")
p=lapply(p, function(x) unique(x)) 
set=as.vector(GradyAugmented)
s=lapply(p, function(x) set %in% x)
#p1=lapply(s, function(x) sum(x))
p2=do.call(rbind,lapply(s,function(x) sum(x)))

total=lapply(p, function(x) length(x)) 
total=unlist(total)
dict_words=p2/total

newdat=cbind(newdat,dict_words)

######Counting no. of words and no. of distinct words###
library(tm)
dd = read.csv("comments_cleaned.csv",header=FALSE,stringsAsFactors = FALSE,sep=',')
dd$V1<-removePunctuation(dd$V1)
tot1 = str_count(dd$V1, '\\s+')+1 
p=strsplit(dd$V1," ")
p=lapply(p, function(x) unique(x)) 
distinct = lapply(p, function(x) length(x))
distinct = unlist(distinct)
ratio = distinct/tot1

newdat=cbind(newdat,ratio)
len_comment = tot1/max(tot1)
newdat=cbind(newdat,len_comment)
newdat=cbind(newdat,distinct)
newdat=newdat[,-c(18,19,26,27)]

#######Questions quality######
comm=read.csv("Comments.tsv",header=FALSE,stringsAsFactors = FALSE,sep = '\t')
d = read.csv("new_pos_tags_ques.csv",header=FALSE,stringsAsFactors = FALSE,sep = '\t')
d = d[-250,]
newdatq=data.frame()
#Lexical density
pp=d$V2
p1=c("N","^","V","A","R")
G=strsplit(pp, " ")
lev=p1
G1 = do.call(rbind,lapply(G,function(x,lev)
{ table(factor(x,levels = lev,
               ordered = TRUE))},
lev = lev))
library(stringr)
tot = str_count(pp, '\\s+')+1
o=G1/tot
G2=rowSums(o)
newdatq=cbind(comm$V2,G2)


#Counts of each pos tag
#get the counts by running the tweetNLP POS tagger
#./runTagger.sh --no-confidence examples/input.txt > output.tsv
p=c("N","O","S","^","Z","V","A","R","!","D","P","&","T","X","#","@","~","U","E","$",",","G","L","M","Y")
lev=p
G1 = do.call(rbind,lapply(G,function(x,lev)
{ table(factor(x,levels = lev,
               ordered = TRUE))},
lev = lev))

tot = str_count(pp, '\\s+')+1 
o=G1/tot
o=as.data.frame(o)
newdatq=cbind(newdatq,o)

#Grammatical errors...do later

ques_text=str_replace(gsub("\\s+", " ", str_trim(comm$V5)), "B", "b")
#next_word_your=str_extract(comm_text, '(?<=your\\s)\\w+')
next_word_its=str_extract(ques_text, '(?<=its\\s)\\w+')

write.csv(next_word_its,"its_colq.csv",row.names = F)

#Add the tag### 

dat_its_tag=read.csv("its_colq.csv",header=F,stringsAsFactors = F,sep='\t')
its_data = within(dat_its_tag, {
  new_its = ifelse(V2 == "V"|V2=="R"|V2=="D", 1, 0)
})

newdat=cbind(newdat,its_data$new_its)

#Dictionary
dic = read.csv("removed_prop_nounsq_final.csv",header=FALSE,stringsAsFactors = FALSE,sep='\t')
library(qdapDictionaries)
dic$V2=tolower(dic$V2)
p=strsplit(dic$V2," ")
p=lapply(p, function(x) unique(x)) 
set=as.vector(GradyAugmented)
s=lapply(p, function(x) set %in% x)
#p1=lapply(s, function(x) sum(x))
p2=do.call(rbind,lapply(s,function(x) sum(x)))

total=lapply(p, function(x) length(x)) 
total=unlist(total)
dict_words=p2/total

#newdat=cbind(newdat,dict_words)

######Counting no. of words and no. of distinct words###
dd = read.csv("pre_questions.csv",header=FALSE,stringsAsFactors = FALSE,sep='\t')
tot1 = str_count(dd$V2, '\\s+')+1 

p=strsplit(dd$V2," ")
p=lapply(p, function(x) unique(x)) 
distinct = lapply(p, function(x) length(x))
distinct = unlist(distinct)
ratio = distinct/tot1

len_question = tot1/max(tot1)
#newdat=cbind(newdat,ratio)

f1_q=len_question
f2_q=dict_words

eti = read.csv("user_answer_diff.csv",header=FALSE,stringsAsFactors = FALSE,sep='\t')
d = read.csv("Comments_with_pos.tsv",header=FALSE,stringsAsFactors = FALSE,sep = '\t')
dc = read.csv("comments_cleaned.csv",header=FALSE,stringsAsFactors = FALSE,sep = '\t') 
dc$V1<-removePunctuation(dc$V1)
d$V6=dc$V1
agg_d = aggregate(d$V6, list(d$V7), paste, collapse=" ")
agg_d$x=str_replace(gsub("\\s+", " ", str_trim(agg_d$x)), "B", "b")
target=unique(eti$V1)
agg_d1=agg_d[match(target, agg_d$Group.1),]
#write.csv(agg_d,"agg_comm.csv",row.names = FALSE)

agg_pos = read.csv("agg_comm_pos_tags.csv",header=FALSE,stringsAsFactors = FALSE,sep = '\t')
agg_pos = agg_pos[-176,]
pp=agg_pos$V2
p1=c("N","^","V","A","R")
G=strsplit(pp, " ")
lev=p1
G1 = do.call(rbind,lapply(G,function(x,lev)
{ table(factor(x,levels = lev,
               ordered = TRUE))},
lev = lev))
library(stringr)
tot = str_count(pp, '\\s+')+1
o=G1/tot
G2=rowSums(o)

user_lex = as.data.frame(cbind(target,G2))
user_lex$G2=as.character(user_lex$G2)

for(i in 1:nrow(user_lex))
{
  ind = which(eti$V1 %in% user_lex$target[i])
  eti[ind,3]=user_lex[i,2]
}

eti1 = cbind(d$V2,eti)
eti1 = cbind(sl,eti1)
eti1 = eti1[,c(1,2,5)]
write.csv(eti1,"eti_lexical_features.csv",row.names = FALSE)

####Question_quality

ques = as.data.frame(cbind(d$V1,eti))
colnames(ques)[1]="uid"
ques1=ques[,c(1,4)]
ques1$V3=as.numeric(ques1$V3)

agg_q= aggregate(V3~uid, ques1, function(x) sum(x>=0.6)/length(x))

targetq=unique(d$V1)
agg_q1=agg_q[match(targetq, agg_q$uid),]
ques_quality_data = as.data.frame(d$V1)
colnames(ques_quality_data)[1]="qid"
for(i in 1:nrow(agg_q1))
{
  ind = which(ques_quality_data$qid %in% agg_q1$uid[i])
  ques_quality_data[ind,2]=agg_q1[i,2]
}
f3_a = newdat$G2
f3_a = as.character(f3_a)
f3_a = as.numeric(f3_a)

f3_q = ques_quality_data$V2
f3_q = as.character(f3_q)
f3_q = as.numeric(f3_q)

f1_q = len_question
f2_q = dict_words

f1_a = newdat$len_comment
f1_a = as.character(f1_a)
f1_a = as.numeric(f1_a)

f2_a = newdat$dict_words
f2_a = as.character(f2_a)
f2_a = as.numeric(f2_a)

answer_score = 0.2*(f1_a) + 0.4*(f2_a) + 0.4*(f3_a)
ques_score = 0.2*(f1_q) + 0.4*(f2_q) + 0.4*(f3_q) 

f1_score  = (2*answer_score*ques_score)/(answer_score+ques_score)

newdat = cbind(newdat,f1_score)
write.csv(newdat,"ans_quality.csv",row.names = FALSE)
