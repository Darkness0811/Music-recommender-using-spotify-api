import pandas as pd
import numpy as np
import Recommenders as Recommenders
from models import P_music
from data import song_df,user



def Popular_recommend(user_id):
    result = []
    pr = Recommenders.popularity_recommender_py()
    pr.create(song_df, 'user_id', 'song')

    recommendations = pr.recommend(user_id)  
    for rec in recommendations['song']:
        # Fetch additional details for each recommended song
        song_details = song_df[song_df['song'] == rec]
        song_name = song_details.iloc[0]['name']
        artist_name = song_details.iloc[0]['artist']
        link = song_details.iloc[0]['spotify_preview_url']
        
        # Create P_music instance with song details and append to result list
        result.append(P_music(song_name=song_name, link=link, artist_name=artist_name))
    return result



# def popular_playlist(song):
#     result=[]
#     pr=Recommenders.item_similarity_recommender_py()
#     recommendations = pr.get_similar_items(song)  # Recommend for a specific user
#     for rec in recommendations:
#         # Fetch additional details for each recommended song
#         song_details = song_df[song_df['song'] == rec].iloc[0]
#         song_name = song_details['name']
#         artist_name = song_details['artist']
#         link = song_details['spotify_preview_url']
        
#         # Create P_music instance with song details and append to result list
#         result.append(P_music(song_name=song_name, link=link, artist_name=artist_name))
#     return result





