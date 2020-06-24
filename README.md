# SpotifyAnalysis
Scripts for analysing a Spotify dataset

SM_parseAndDownloadTracks takes playlist ID's from a .csv-file, extract tracks, and downloads 30-second samples. It also retrieves audio features.
You need to create a file spotifyConstants.py that contains your client ID etc, which you can get from developer.spotify.com.

# Datasets
This folder contains datasets.
'combinedSpotifyFeatures.csv' is a dataset of audio features for ~475k tracks. It was created by combining publicly available datasets and scraping top playlists in various countries at various times.
