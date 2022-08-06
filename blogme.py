# -*- coding: utf-8 -*-
"""
Created on Thu Aug  4 00:02:00 2022

@author: ahadi
"""

import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

#reading excel or xlsx files
data = pd.read_excel('articles.xlsx')

#Summary of the data
data.describe()

#Summary of the columns
data.info()

#Counting the number of articles per source
#format of groupby: df.groupby(['column_to_group'] )['column_to_count'].count()
#count of articles by different publisher
data.groupby(['source_id'])['article_id'].count()

#data['title'][3181] (to extract the title of 3181th row)

#number of reactions by publisher
data.groupby(['source_id'])['engagement_reaction_count'].sum()

#dropping a column
data = data.drop('engagement_comment_plugin_count' , axis=1)  #axis=1 is just referring to dropping a column

#Creating a keyword flag

# keyword = 'crash'

# keyword_flag = []
# #lets create a for loop to isolate each title
# length = len(data)
# for x in range(0,length):
#     heading = data['title'][x] #This will fetch title index wise i.e. if x=0 then first title will be fetched.
#     if keyword in heading: #This will check if the keywoord is present in the header i.e. if crash is in the title.
#         flag = 1
#     else:
#         flag = 0
    
#     keyword_flag.append(flag)

#creating a function for the above code
def keywordflag(keyword):
    length =len(data)
    keyword_flag=[]
    for x in range(0,length):
        heading = data['title'][x] #This will fetch title index wise i.e. if x=0 then first title will be fetched.
        try:  #Try and find keyword in every heading
            if keyword in heading: #This will check if the keywoord is present in the header i.e. if crash is in the title.
                flag = 1
            else:
                flag = 0
        except: # But if its not there / or heading doesn't exist(nan) the make the flag = 0
            flag = 0     
        keyword_flag.append(flag)
    return keyword_flag

keywordflag = keywordflag('crash') 

data['keyword_flag'] = pd.Series(keywordflag)

#SentimentIntensityAnalyzer

sent_int = SentimentIntensityAnalyzer() #initializing the class

text = data['title'][16]
sent = sent_int.polarity_scores(text) #A compound is just a sum of neg,pos and neu and is normalised. A compound which is closer to -1 is negative and a compund which is closer to 1 is positive.

neg = sent['neg']    
pos = sent['pos']
neu = sent['neu']
    
    
#Adding a for loop to extract sentiment per title
title_neg_sentiment = []
title_pos_sentiment = [] 
title_neu_sentiment = []    

length = len(data)
for x in range (0,length):
   try:
        text = data['title'][x]
        sent_int = SentimentIntensityAnalyzer() #initializing the class 
        sent = sent_int.polarity_scores(text) #A compound is just a sum of neg,pos and neu and is normalised. A compound which is closer to -1 is negative and a compund which is closer to 1 is positive.
        neg = sent['neg']    
        pos = sent['pos']
        neu = sent['neu']
   except:
        neg = 0
        pos = 0
        neu = 0
        
   title_neg_sentiment.append(neg)
   title_pos_sentiment.append(pos)
   title_neu_sentiment.append(neu)         

data['title_neg_sentiment']  = pd.Series(title_neg_sentiment) 
data['title_pos_sentiment']  = pd.Series(title_pos_sentiment) 
data['title_neu_sentiment']  = pd.Series(title_neu_sentiment)

#Writing the data

data.to_excel('blogme_cleaned.xlsx', sheet_name='blogemedata', index = False)