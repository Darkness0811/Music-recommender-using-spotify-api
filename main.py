from fastapi import FastAPI
import uvicorn
from music import Music_Recommender
from models import recommendation_schema, music, P_music
import ms
app = FastAPI()

@app.post("/recommend")
async def recommend(values:recommendation_schema):
    recommend=Music_Recommender(values)
    recommendations:list[music]=recommend()
    return{"recommendation":recommendations}

@app.post("/home")
async def home(values:P_music):
    recommend=ms.Popular_recommend(values)
    recommendations:list[P_music]=recommend
    return {"recommendation":recommendations}


@app.get("/")
async def index():
    return {"message": "Hello World"}       

if __name__=="__main__":
    uvicorn.run(app)