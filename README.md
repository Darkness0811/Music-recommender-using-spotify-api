# Music-recommender-using-spotify-api

**1. Introduction**
The Music Recommendation System is designed to provide users with personalized music suggestions based on their preferences. It leverages the Spotify API to fetch recommendations using user-defined parameters such as artist name, genres, and track attributes.

**2. Project Components**
- **Backend (FastAPI):** Handles API requests and processes user inputs.
- **Recommendation Engine:** Uses the Spotify API to generate recommendations.
- **Frontend (Streamlit):** Provides a user-friendly interface for input and displaying recommendations.

**3. Steps of Implementation**

**Step 1: Setting Up API Authentication**
- Implemented OAuth 2.0 authentication to access the Spotify API.
- Stored API credentials securely using environment variables.

**Step 2: Developing the Recommendation Engine**
- Created a `_ClientCredentialsFlow` class in `api.py` to authenticate API requests.
- Developed a `Recommender` class to interact with Spotify's recommendation API.
- Implemented methods to fetch artist IDs, track IDs, and genre-based recommendations.

**Step 3: Defining Data Models**
- Used `pydantic` and `dataclasses` in `models.py` to define `recommendation_schema`, `music`, and `P_music` models.

**Step 4: Creating the Backend API**
- Developed FastAPI endpoints in `main.py` to handle recommendation requests.
- Implemented `/recommend` endpoint to return music recommendations based on user preferences.

**Step 5: Building the Recommendation Service**
- Implemented `Music_Recommender` class in `music.py` to process requests and retrieve recommendations.
- Converted API responses into structured data using `pandas`.
- Stored recommended songs in a CSV file for further analysis.

**Step 6: Developing the Frontend Interface**
- Built a Streamlit application in `app.py`.
- Provided input fields for artist names and genre selection.
- Integrated API requests to fetch recommendations dynamically.
- Displayed song details including images, play links, and artist information.

**Step 7: Testing and Deployment**
- Performed unit testing to ensure API responses were accurate.
- Deployed the FastAPI backend and Streamlit frontend on a local server.
- Verified the correctness of recommendations and UI functionality.

**4. Conclusion**
This project successfully integrates the Spotify API with a recommendation system, allowing users to receive music suggestions based on their preferences. Future improvements include expanding filtering options and enhancing model accuracy through machine learning.

