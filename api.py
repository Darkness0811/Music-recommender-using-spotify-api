import requests
import logging
import base64
import six
import os
import pandas as pd


class _ClientCredentialsFlow(object):
    OAUTH_TOKEN_URL = 'https://accounts.spotify.com/api/token'

    def __init__(self, client_id=None, client_secret=None):
        if not client_id:
            client_id = os.getenv('client_id')

        if not client_secret:
            client_secret = os.getenv('client_secret')

        if not client_id or not client_secret:
            raise Exception('A client ID and client secret is required.')

        self.client_id = client_id
        self.client_secret = client_secret

        self.token_info = None

    def _make_authorization_header(self):
        payload = {
            'grant_type': 'client_credentials',
            'scope': 'user-read-private user-top-read'
        }
        auth_header = base64.b64encode(six.text_type(self.client_id + ':' + self.client_secret).encode('ascii'))
        return {'Authorization': 'Basic %s' % auth_header.decode('ascii')}

    def get_access_token(self):
        payload = {'grant_type': 'client_credentials'}
        headers = self._make_authorization_header()
        response = requests.post(self.OAUTH_TOKEN_URL, data=payload, headers=headers, verify=True)
        if response.status_code != 200:
            raise Exception(response.reason)
        token_info = response.json()
        return token_info['access_token']


class Recommender(object):
    def __init__(self, client_id=None, client_secret=None):
        auth = _ClientCredentialsFlow(client_id, client_secret)
        self.token = auth.get_access_token()

        self.url = 'https://api.spotify.com/v1/'

        self._artist_ids = []
        self._track_ids = []
        self._genres = []
        self._limit = 20
        self._track_attributes = {}
        self._market = ""

        self.headers = {
            'Authorization': 'Bearer ' + self.token
        }

        self._available_genre_seeds = None

        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger("music-recommender")

    @property
    def limit(self):
        return self._limit

    @limit.setter
    def limit(self, limit):
        if limit > 100:
            self.logger.warning("Maximum target size is 100.")
        self._limit = limit

    @property
    def market(self):
        return self._market

    @market.setter
    def market(self, market):
        self._market = market

    @property
    def track_attributes(self):
        return self._track_attributes

    @track_attributes.setter
    def track_attributes(self, track_attributes):
        self._track_attributes = track_attributes

    def available_genre_seeds(self):
        return [
            
            "acoustic", "afrobeat", "alt-rock", "alternative", "ambient", "anime",
            "black-metal", "bluegrass", "blues", "bossanova", "brazil", "breakbeat",
            "british", "cantopop", "chicago-house", "children", "chill", "classical",
            "club", "comedy", "country", "dance", "dancehall", "death-metal", "deep-house",
            "detroit-techno", "disco", "disney", "drum-and-bass", "dub", "dubstep", "edm",
            "electro", "electronic", "emo", "folk", "forro", "french", "funk", "garage",
            "german", "gospel", "goth", "grindcore", "groove", "grunge", "guitar",
            "happy", "hard-rock", "hardcore", "hardstyle", "heavy-metal", "hip-hop",
            "holidays", "honky-tonk", "house", "idm", "indian", "indie", "indie-pop",
            "industrial", "iranian", "j-dance", "j-idol", "j-pop", "j-rock", "jazz",
            "k-pop", "kids", "latin", "latino", "malay", "mandopop", "metal", "metal-misc",
            "metalcore", "minimal-techno", "movies", "mpb", "new-age", "new-release",
            "opera", "pagode", "party", "philippines-opm", "piano", "pop", "pop-film",
            "post-dubstep", "power-pop", "progressive-house", "psych-rock", "punk",
            "punk-rock", "r-n-b", "rainy-day", "reggae", "reggaeton", "road-trip",
            "rock", "rock-n-roll", "rockabilly", "romance", "sad", "salsa", "samba",
            "sertanejo", "show-tunes", "singer-songwriter", "ska", "sleep", "songwriter",
            "soul", "soundtracks", "spanish", "study", "summer", "swedish", "synth-pop",
            "tango", "techno", "trance", "trip-hop", "turkish", "work-out", "world-music"
        ]



    def _is_genre_seed_available(self, genre):
        
        return genre in self.available_genre_seeds()

    @property
    def genres(self):
        return self._genres

    @genres.setter
    def genres(self, genres):
        if isinstance(genres, list):
            for genre in genres:
                genre = genre.lower()
                if self._is_genre_seed_available(genre):
                    self._genres.append(genre)
        else:
            genres = genres.lower()
            if self._is_genre_seed_available(genres):
                self._genres.append(genres)
        if not self._genres:
            return "pop"
        return self._genres
        

    @property
    def artists(self):
        return self._artist_ids

    @artists.setter
    def artists(self, artists):
        self._artist_ids = []
        if isinstance(artists, list):
            for artist in artists:
                artist = self._lookup_artist_id(artist)
                if artist:
                    self._artist_ids.append(artist)
        else:
            artist = self._lookup_artist_id(artists)
            if artist:
                self._artist_ids.append(artist)
        if not self._artist_ids:
            self.logger.warning("No matching seeds found for given artist.")

    @property
    def tracks(self):
        return self._track_ids

    @tracks.setter
    def tracks(self, tracks):
        self._track_ids = []
        if isinstance(tracks, list):
            for track in tracks:
                self._track_ids.append(self._lookup_track_id(track))
        else:
            self._track_ids.append(self._lookup_track_id(tracks))
        if not self._track_ids:
            self.logger.warning("No matching seeds found for given track.")
    
    def find_recommendations(self):
        if not self._artist_ids and not self.genres and not self.tracks:
            raise Exception("At least one artist, genre, or track seed is required.")
        
        # Updated endpoint and parameters
        params = {
            'seed_artists': ",".join(self._artist_ids),
            'seed_genres': ",".join(self.genres),
            'seed_tracks': ",".join(self.tracks),
            'limit': self.limit,
            'market': self.market  # Add market if required
        }

        # Add track attributes if any
        params.update(self.track_attributes)
        
        # Make the request to the new endpoint
        recs = self._make_request(endpoint='v1/recommendations', params=params)
        
        if not recs or 'tracks' not in recs:
            raise Exception("No recommendations received from Spotify API.")
        
        return recs

    def _lookup(self, term, lookup_type):
        params = {
            'q': term,
            'type': lookup_type
        }
        return self._make_request(endpoint='search', params=params)

    def _lookup_track_id(self, track):
        tracks = self._lookup(term=track, lookup_type='track')

        if len(tracks['tracks']['items']):
            return tracks['tracks']['items'][0]['id']
        
        self.logger.warning("No results found for: %s" % track)

    def _lookup_artist_id(self, artist_name):
        artists = self._lookup(term=artist_name, lookup_type='artist')

        if len(artists['artists']['items']):
            return artists['artists']['items'][0]['id']

        self.logger.warning("No results found for: %s" % artist_name)

    def _make_request(self, endpoint, params):
        full_url = self.url + endpoint
        #print(f"Making request to: {full_url}")  # Print full URL being called

        response = requests.get(full_url, params=params, headers=self.headers)

        # print(f"Response Status: {response.status_code}")
        # print(f"Response Text: {response.text}")  # Print full response for debugging

        if response.status_code != 200:
            print(f"API Error: {response.status_code} - {response.text}")
            raise Exception(f"Error {response.status_code}: {response.text}")

        return response.json()

