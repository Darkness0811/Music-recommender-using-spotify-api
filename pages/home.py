import streamlit as st
import pandas as pd
from models import P_music
from data import user
import requests
from dataclasses import asdict  # Add this import\

# Streamlit UI
st.title("Music Recommendation")

# Define your FastAPI server URL
API_URL = "http://localhost:8000"
def get_recommendation(values):
    url = f"{API_URL}/home"
    response = requests.post(url, values)
    return response.json()



# Display popular tracks
# Call the backend API
id = st.text_input(f"{range(0,len(user))}")# Populate appropriately
recommendations = get_recommendation(user.iloc[id])


# Display recommendations in columns
if 'recommendation' in recommendations:
            col_count = 3  # Number of columns
            rec_count = len(recommendations['recommendation'])
            rows = rec_count // col_count + (1 if rec_count % col_count else 0)
            for row in range(rows):
                cols = st.columns(col_count)
                for col_idx in range(col_count):
                    rec_idx = row * col_count + col_idx
                    if rec_idx < rec_count:
                        rec = recommendations['recommendation'][rec_idx]
                        with cols[col_idx]:
                            st.write(f"Recommendation {rec_idx + 1}:")
                            # Wrap the image in an <a> tag to open the link on click
                            with st.container():
                                st.image(rec['fox.png'], caption=f"Song: {rec['song_name']}, Artist: {rec['artist_name']}", use_column_width=True, width=150)
                                st.write("Link:", rec['link'])
                                st.write("-----------")




