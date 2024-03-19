import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import joblib
import re
# import ipywidgets as widgets
# from IPython.display import display

vector = joblib.load('vectorizer.pkl')
vec_metric = joblib.load('vec_metric.pkl')
movie = pd.read_csv('clean_movie.csv')
ratings = pd.read_csv('ratings.csv')

def clean_title(title):
    return re.sub('[^a-zA-Z0-9 ]','',title) 


def search_movieId(title):
    title = clean_title(title)
    query_vec= vector.transform([title])
    similarity = cosine_similarity(query_vec,vec_metric).flatten() # flatten is used get 1D array
    indices = np.argpartition(similarity,-5)[-1]# most similar listed first
    Id  = movie.iloc[indices][0]
    return Id

def recommendation(movieId):
    # finding similar users and their recommendation  greater than 10%
    similar_user = ratings[(ratings['movieId']==movieId) &(ratings['rating']>4) ]['userId'].unique()
    similar_user_rec = ratings[(ratings['rating'] >4 ) & (ratings['userId'].isin(similar_user))]['movieId']
    similar_user_rec = similar_user_rec.value_counts()/len(similar_user) 
    similar_user_rec = similar_user_rec[similar_user_rec >0.2]
    
    
    all_user = ratings[(ratings['movieId'].isin(similar_user_rec.index)) &(ratings['rating']>4)] #list of users like the above movie
    all_user['movieId'].value_counts() # counting how many user rated a single movie
    all_user_rec = all_user['movieId'].value_counts()/len(all_user['userId'].unique())
    
    rec_percent = pd.concat([similar_user_rec,all_user_rec],axis = 1)
    rec_percent.columns = ['similar','all']
    
    rec_percent['score'] = rec_percent['similar']/rec_percent['all']
    rec_percent.sort_values(ascending=False,by ='score')
    
    #returning only top ten movie with three attributes ['score','title','genres']
    return rec_percent.head(11).merge(movie,left_index=True,right_on='movieId')['clean_title']
    




