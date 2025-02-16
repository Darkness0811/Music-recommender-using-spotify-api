from pydantic import BaseModel
from dataclasses import dataclass

class recommendation_schema(BaseModel):
    artist_name: str
    genres: list[str] 
    attrs: dict
    limit:int =20
    
@dataclass
class music:
    song_name:str
    song_id:int
    artist_name:str
    artist_id:int
    play_link:str
    link:str
    image:str
    release_date:int
    popularity:int

@dataclass
class P_music:
    song_name:str
    artist_name:str
    link:str
    
