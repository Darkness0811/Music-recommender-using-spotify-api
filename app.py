import streamlit as st
import requests
from models import recommendation_schema

# Define your FastAPI server URL
API_URL = "http://localhost:8000"

# Function to make a recommendation request to FastAPI backend
def get_recommendation(values):
    url = f"{API_URL}/recommend"
    response = requests.post(url, json=values.dict())
    return response.json()

# Streamlit UI
def main():
    st.title("Music Recommender")

    # Input fields for user to specify recommendation criteria
    artist_name = st.text_input("Enter Artist Name:", value="", key="artist_name_input", type="default")

    # Display checkboxes for genres
    st.subheader("Select Genres:")
    selected_genres = st.multiselect("Genres:", options=["Pop", "Rock", "Hip Hop", "Jazz", "Classical", "Electronic", "Country"])

    # Button to trigger recommendation
    if st.button("Get Recommendations"):
        # Create recommendation schema object
        values = recommendation_schema(artist_name=artist_name, genres=selected_genres, attrs={})

        # Call the backend API
        recommendations = get_recommendation(values)

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
                                st.image(rec['image'], caption=f"Song: {rec['song_name']}, Artist: {rec['artist_name']}", use_column_width=True, width=150)
                                st.write("Link:", rec['link'])
                                st.audio(rec['play_link'], format='audio/mp3')
                                st.write("-----------")

# Run the Streamlit app
if __name__ == "__main__":
    main()
