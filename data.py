# Load data
import pandas as pd


song_df_1 = pd.read_csv('archive/User Listening History.csv')
song_df_2 = pd.read_csv("archive/Music Info.csv")

song_df = pd.merge(song_df_1, song_df_2.drop_duplicates(['track_id']), on='track_id', how='left')


song_df['song'] = song_df['name']+' - '+song_df['artist']

user=song_df["user_id"].drop_duplicates()

user.index = range(1, 1 + len(user))



