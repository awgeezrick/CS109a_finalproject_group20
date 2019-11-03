# spotify_api
# Author - Mark McDonald - 2019
# Handles Spotify authorization and api requests

# You will need to setup a Spotify API developer account and store your credentials in local environment variables for these functions to work.
# SPOTIFY_CLIENT_ID
# SPOTIFY_CLIENT_SECRET
# SPOTIFY_REDIRECT_URI
#
# template bash profile lines:
# export SPOTIFY_CLIENT_ID={your info here}
# export SPOTIFY_CLIENT_SECRET={your info here}
# export SPOTIFY_REDIRECT_URI=cs109arecommender://callback


#v1: Initial Release
#v2: Added support for audio_features

import os
import sys
import json
import time
from time import sleep
import spotify_utils_v1

import requests
from requests.auth import AuthBase
import base64

# Create a token authentication class to help create access token
class TokenAuth(AuthBase):
    """Implements a custom authentication scheme."""

    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        """Attach an API token to a custom auth header."""
        r.headers['Authorization'] = f'{self.token}'  # Python 3.6+
        return r


# Convert string into base64 encryption
def base64_conv(data):
    # Standard Base64 Encoding
    encodedBytes = base64.b64encode(data.encode("utf-8"))
    encodedString = str(encodedBytes, "utf-8")

    return encodedString


# setup spotify credenatial in your bash profile
# you get these by applying for developer credentials at spotify API site
def credentials():
    """
    Stores necessary credential variables.
    Must be initialized but only needs to be initalized once by calling credentials().
    Subsequenty, credentials are retrieved via:
        credentials.client_id
        credentials.client_secret
        credentials.redirect_uri

    """
    # test to see if we need to set variables
    try:
        if credentials.client_id or credentials.client_secret or credentials.redirect_uri:
            pass
    except:
        # they aren't set
        print("Setting credentials")
        try:
            client_id = os.environ['SPOTIFY_CLIENT_ID']
            setattr(credentials, "client_id", client_id)
        except:
            print("ERROR: You must have a SPOTIFY_CLIENT_ID variable setup in your bash profile")
        try:
            client_secret = os.environ['SPOTIFY_CLIENT_SECRET']
            setattr(credentials, "client_secret", client_secret)
        except:
            print("ERROR: You must have a SPOTIFY_CLIENT_SECRET variable setup in your bash profile")
        try:
            redirect_uri = os.environ['SPOTIFY_REDIRECT_URI']
            setattr(credentials, "redirect_uri", redirect_uri)
        except:
            print("ERROR: You must have a SPOTIFY_REDIRECT_URI variable setup in your bash profile")

        # base64 credentials
        encodedCredentials = base64_conv(credentials.client_id + ":" + credentials.client_secret)
        setattr(credentials, "credentials", encodedCredentials)


def token(force: bool = False) -> str:
    """
    Returns a new token if the current token is expired.
    parameters:
        force - default=False.  Will force a new token even if current token isn't expired
    attributes:
        expiration - time in epoch of the current token's expiration
        token - string value of the current token
    returns:
        string value of the current token

    """

    # Ensure that credentials are set
    credentials()

    url = "https://accounts.spotify.com/api/token"

    # check current token
    # -------------------
    # If token has been set and is valid, return current token
    try:
        if (not force) and (time.time() < token.expiration) and (token.token != None):
            return token.token
    except:
        # token attributes have not been set
        print("token():INFO:   Getting initial token")

    # No token exists or token is not valid
    # refresh token
    # -------------
    auth = TokenAuth('Basic ' + credentials.credentials)
    data = {"grant_type": "client_credentials"}
    tok_response = requests.post(url, auth=auth, data=data)
    stat = tok_response.status_code

    if stat != 200:
        print("Error getting token: {}".format(stat))
        return False

    # parse token from response
    token_duration = tok_response.json().get('expires_in')
    token_exp_time = time.time() + token_duration - 10  # 10 second padding
    new_token = tok_response.json().get('access_token')

    print("token():INFO:   Token refreshed")

    # set static attribute for function
    # use: token.expiration  returns: exp time in epoch
    # use: token.token  returns: token string
    setattr(token, 'expiration', token_exp_time)
    setattr(token, 'token', new_token)

    return new_token


def parse_spotify_url(spotify_url) -> str:
    """
    Returns the spotify id and url type from a url value from the database
    Example valid url: "spotify:track:0HLWvLKQWpFdPhgk6ym58n"
    """

    if ':' not in spotify_url:
        print("parse_spotify_url(): Not a valid spotify url: {}".format(spotify_url))
        return False

    split_string = spotify_url.split(":")

    # get last item
    length = len(split_string)

    parsed_id = split_string[length - 1]
    parsed_type = split_string[length - 2]

    return parsed_type, parsed_id


def get_spotify_url(db_uri: str) -> str:
    """
    returns the supplied db uri into a Spotify url
    """
    # get type and id
    url_type, url_id = parse_spotify_url(db_uri)

    # convery to spotify URL
    spotify_url = "https://api.spotify.com/v1/"
    if url_type == "track":
        spotify_url += "tracks/"
    elif url_type == "artist":
        spotify_url += "artists/"
    elif url_type == "album":
        spotify_url += "albums/"

    spotify_url += url_id

    return spotify_url


def get_spotify_data(db_uri: str, key: str = None):
    """
    Returns single item from spotify url via API call.
    Provided URI can be a track,, artist or album.
    if key value is set, returns value for that key.
    If key is not valid, False is returned.
    See 'get_spotify_list' for retrieving a list of items.
    parameters:
        db_uri: - database uri value
        key: (optional) - key for which value should be returned.  If None, return entire json dictionary
    returns:
        value of key supplied or entire json dictionart if key=None.
    """

    # build spotify url from db uri
    url = get_spotify_url(db_uri)

    token()  # ensure token is valid
    response = requests.get(url, auth=TokenAuth('Bearer ' + token.token))

    # v2: Added delay when too many API requests
    if response.status_code == 429: # too many requests
        retry_value = response.headers.get('Retry-After')
        print("API limit.  Waiting {} seconds".format(retry_value))
        sleep(retry_value+1)

        # resend request
        token()  # ensure token is valid
        response = requests.get(url, auth=TokenAuth('Bearer ' + token.token))

    if response.status_code != 200:
        print("ERR: Unable to access Spotify data:  ERR:{}   URI:{}".format(response.status_code, db_uri))
        return False

    if key == None:
        return response.json()
    else:
        if key not in response.json().keys():
            print("'{}' not in keys: \n\t{}".format(key, response.json().keys()))
            return False
        return response.json().get(key)


def build_id_string(uri_list:list) -> str:
    """
    Buils list or ids used for API REST call.
    """
    rv_str = ''

    for u in uri_list:
        t_type, t_id = parse_spotify_url(u)

        if rv_str == '':
            rv_str += t_id
        else:
            rv_str += ',' + t_id

    return rv_str


def get_spotify_list(spotify_url:str, uri_list:list):
    """
    Returns a list of objects from a list of provided
    URI's and spotify URL.  Can be used for tracks, audio audio_features
    and artists.  Need only to supply proper spotify_url base for each.
    Items returned are in same order as list.
    Arguments:
        spotify_url:str - spotify API URL that is base of call.
        uri_list:list - ordered list of spotify item uris
    Returns:
        list of item dictionaries in order of uri list supplied
    """

    # build dictionary for rest call parameters
    r_dict = {'ids': build_id_string(uri_list)}

    token()  # ensure token is valid
    response = requests.get(spotify_url,
                            auth=TokenAuth('Bearer ' + token.token),
                            params=r_dict)

    if response.status_code == 429: # too many requests
        retry_value = response.headers.get('Retry-After')
        print("API limit.  Waiting {} seconds".format(retry_value))
        for s in tqdm(range(retry_value+1)):
            sleep(1)

        # resend request
        token()  # ensure token is valid
        response = requests.get(spotify_url,
                            auth=TokenAuth('Bearer ' + token.token),
                            params=r_dict)


    if response.status_code == 503: # service unavailable
        count_limit = 10
        count = 0
        while response.status_code == 503:
            retry_value = response.headers.get('Retry-After')
            if retry_value is None or retry_value==0:
                retry_value = 3
            print("{} Service Unavailable.  Waiting {} seconds".format(count_limit-count, retry_value))
            for s in tqdm(range(retry_value+1)):
                sleep(1)

            # resend request
            token()  # ensure token is valid
            response = requests.get(spotify_url,
                                auth=TokenAuth('Bearer ' + token.token),
                                params=r_dict)
            count += 1
            if count == count_limit:
                print("Tried {} times.  Done trying.".format(count_limit))
                return False


    if response.status_code != 200:
        print("ERR: Unable to access Spotify data:  ERR:{}".format(response.status_code, spotify_url))
        return False

    return response


def get_artists(uri_list:list) -> list:
    """
    Returns a list of artists from a list of provided
    artist URL's.
    Artis returned are in same order as list.
    Arguments:
        artist_uri_list:list - ordered list of spotify artist uris
    Returns:
        list of arist dictionaries in order of uri list supplied
    """
    max_batch = 50
    if len(uri_list)>max_batch:
        print("ERR: List too large.  Max allowed is {}.  Provided list size={}".format(max_batch, len(uri_list)))
        return False
    spotify_url = "https://api.spotify.com/v1/artists/"
    response = get_spotify_list(spotify_url, uri_list)
    return response.json().get('artists')


def get_tracks(uri_list:list) -> list:
    """
    Returns a list of tracks from a list of provided
    track URL's.
    Tracks returned are in same order as list.
    Arguments:
        uri_list:list - ordered list of spotify track uris
    Returns:
        list of track dictionaries in order of uri list supplied
    """
    max_batch = 50
    if len(uri_list)>max_batch:
        print("ERR: List too large.  Max allowed is {}.  Provided list size={}".format(max_batch, len(uri_list)))
        return False
    spotify_url = "https://api.spotify.com/v1/tracks/"
    response = get_spotify_list(spotify_url, uri_list)
    return response.json().get('tracks')


def get_audiofeatures(uri_list:list) -> list:
    """
    Returns a list of audio features from a list of provided
    track URI's.
    Tracks returned are in same order as list.
    Arguments:
        uri_list:list - ordered list of spotify track uris
    Returns:
        list of track dictionaries in order of uri list supplied
    """
    max_batch = 100
    if len(uri_list)>max_batch:
        print("ERR: List too large.  Max allowed is {}.  Provided list size={}".format(max_batch, len(uri_list)))
        return False
    spotify_url = "https://api.spotify.com/v1/audio-features/"
    response = get_spotify_list(spotify_url, uri_list)
    return response.json().get('audio_features')
