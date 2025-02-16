from models import music,recommendation_schema
import os
import pandas as pd

client_id = os.environ.get("client_id")
client_secret = os.environ.get("client_secret")

from api import Recommender

class Music_Recommender:
    def __init__(self,value:recommendation_schema):
        self.recommender = Recommender(client_id, client_secret)
        self.recommender.artists = value.artist_name
        self.recommender.genres = value.genres
        self.recommender.track_attributes = value.attrs
        self.recommender.limit = value.limit
    
    def __call__(self) -> list[music]:
        recommendations = self.recommender.find_recommendations()
        
        result = []
        
        for recommendation in recommendations['tracks']:
            print(recommendation)
            result.append(music(recommendation['name'],recommendation['id'],
                                recommendation['artists'][0]['name'],recommendation['artists'][0]['id'],
                                recommendation['preview_url'],recommendation['external_urls']['spotify'],
                                recommendation['album']['images'][0]['url'],
                                recommendation['album']['release_date'],recommendation['popularity']))
    
        #     data.append(music(recommendation['name'],recommendation['artists'][0]['name'],
        #                         recommendation['artists'][0]['id'],
        #                         recommendation['external_urls']['spotify'], recommendation['album']['images'][0]['url'],
        #                         recommendation['album']['release_date'],recommendation['popularity'],recommendation['is_local'],
        #                         recommendation['disc_number'],recommendation['duration_ms'],recommendation['explicit']))
        
        df = pd.DataFrame(result)

        # Save as CSV
        df.to_csv('spotify_data.csv', index=False)

        # df = pd.DataFrame(json)

        # # Save DataFrame as JSON file
        # df.to_json("spotify.json", index=False)
        return result