# SpotifyAnalysis

The scripts included here are used in a project for analysing Spotify data.
Once a manuscript has been published or preprinted, I'll add it here.
If you use the scripts/models before a manuscript is available, please cite/refer to this GitHub repository.

# Scripts

SM_parseAndDownloadTracks takes playlist ID's from a .csv-file, extract tracks, and downloads 30-second samples. It also retrieves audio features.
You need to create a file spotifyConstants.py that contains your client ID etc, which you can get from developer.spotify.com.

Models/SML_Network_sharing loads a pre-trained neural network that classifies Spotify tracks to different times of the day.

# Datasets

This folder contains datasets.
'combinedSpotifyFeatures.csv' is a dataset of audio features for ~475k tracks. It was created by combining publicly available datasets and scraping top playlists in various countries at various times.
'Spotify tracks from multiple popular playlists' is a smaller version of the above-mentioned dataset.

# Models

This folder contains a pre-trained neural network, and a script for testing it.
