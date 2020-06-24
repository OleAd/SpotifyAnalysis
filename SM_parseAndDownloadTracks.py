# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 19:38:57 2020

@author: olehe

This script takes a csv with Spotify Playlist IDs
Then gets all tracks from those playlists
Then gets audio features for those tracks
Then downloads a 30-second preview mp3.

"""



#%% Do imports
import spotipy
import spotipy.util as util
import pandas as pd
import time
import random
import requests

import spotifyConstants
# this import contains client ID, Secret, and redirect URL
# for the script to work, you need to make one yourself using the Spotify Developer system

#%% Initiate spotipy
# This initiates a token, for my user and for my app
token=util.prompt_for_user_token(spotifyConstants.myUser, scope=None,
						   client_id=spotifyConstants.myClientID,
						   client_secret=spotifyConstants.myClientSecret,
						   redirect_uri=spotifyConstants.myRedirect)
sp = spotipy.Spotify(auth=token)

#%% Dataframe to hold all tracks

column_names = ['TrackName', 'TrackID', 'SampleURL', 'danceability', 'energy', 
				'loudness', 'speechiness', 'acousticness', 'instrumentalness',
				'liveness', 'valence', 'tempo']
sampleDataFrame = pd.DataFrame(columns = column_names)


#%% Read csv-file
# The csv-file should contain the Spotify ID of the playlists you want to scrape

toDownloadPlaylist = pd.read_csv('Links recreational music - Spotify.csv', low_memory=False)

# This section may need reformatting depending on the csv-file you are using

# listsID holds all the playlist IDs
listsId=[];

for ind in toDownloadPlaylist.index:
	thisEntry = toDownloadPlaylist.iloc[ind]
	thisID = thisEntry['Spotify-ID']
	isPlaylist = thisEntry['Playlist? ']
	
	if isPlaylist=='yes':
		locStartString = thisID.find('/playlist/')
		#format the playlist id, get just the actual ID
		thisIDclean = thisID[locStartString+10:locStartString+10+22]
		listsId.append(thisIDclean)
	
# Now get tracks out of the playlists

completedPlaylists=[]
thisTime = time.time()
totalTracks = 0


#remaininglist=[x for x in listsId if x not in completedPlaylists]

for thisList in listsId:
	# Sleep a little bit to not piss of Spotify
	thisSleep = random.randint(0,10) * 0.05
	time.sleep(thisSleep)
	theseTracks = sp.playlist_tracks(thisList, limit=None, fields='items.track.id, items.track.name, items.track.preview_url')
	theseTracks = sp.playlist_tracks(thisList, limit=None)
	nowTime = time.time()
	if (nowTime - thisTime) > 1800:
		# Refresh token occasionally
		print('Getting new token')
		token=util.prompt_for_user_token(spotifyConstants.myUser, scope=None,
						   client_id=spotifyConstants.myClientID,
						   client_secret=spotifyConstants.myClientSecret,
						   redirect_uri=spotifyConstants.myRedirect)
		sp = spotipy.Spotify(auth=token)
		time.sleep(5)
		thisTime = time.time()
	
	# adding something here to expand the number of tracks, as we missed some due to spotipy only returning the first 100
	# stackoverflow to the rescue
	tracks = theseTracks['items']
	while theseTracks['next']:
		theseTracks = sp.next(theseTracks)
		tracks.extend(theseTracks['items'])
	
	for track in tracks:
		if track['track']==None:
			continue
		thisId=track['track']['id']
		if thisId == None:
			continue
		thisName=track['track']['name']
		print(thisName)
		print()
		thisUrl=track['track']['preview_url']
		# Sleep a little bit to avoid rate limiting
		thisSleep = random.randint(0,10)*0.05
		time.sleep(thisSleep)
		# Get audio features for the track
		thisFeature=sp.audio_features(tracks=thisId)
		
		# Create a dataframe entry
		if thisFeature[0]!=None:
			thisDict = [{'TrackName':thisName,
				 'TrackID':thisId,
				 'SampleURL':thisUrl,
				 'danceability':thisFeature[0]['danceability'],
				 'energy':thisFeature[0]['energy'],
				 'loudness':thisFeature[0]['loudness'],
				 'speechiness':thisFeature[0]['speechiness'],
				 'acousticness':thisFeature[0]['acousticness'],
				 'instrumentalness':thisFeature[0]['instrumentalness'],
				 'liveness':thisFeature[0]['liveness'],
				 'valence':thisFeature[0]['valence'],
				 'tempo':thisFeature[0]['tempo']
				 }]
			thisDf = pd.DataFrame(thisDict)
			sampleDataFrame = sampleDataFrame.append(thisDf, ignore_index=True)
			totalTracks += 1
	# Keep track over which playlists we've completed
	completedPlaylists.append(thisList)


#%% Save the tracks to disk
	
sampleDataFrame.drop_duplicates(inplace=True)
	
sampleDataFrame.to_csv('firstPlaylistScrape.csv', encoding='utf-8')

#%% Create a dataframe that will hold the tracks we successfully download

chosenTracks = pd.DataFrame(columns=['TrackName', 'TrackID', 'SampleURL',
									 'danceability', 'energy', 'loudness',
									 'speechiness', 'acousticness', 'instrumentalness', 'acousticness', 'instrumentalness',
									 'liveness', 'valence', 'tempo'])





#%% Download tracks

countTracks=0
sampleDataFrame.reset_index(inplace=True, drop=True)


for ind in sampleDataFrame.index:
	track = sampleDataFrame.iloc[ind]
	thisFolder = 'firstPlaylistScrape'
	thisID = track['TrackID']
	thisUrl = track['SampleURL']
	thisName = track['TrackName']
	
	if thisUrl != None:
		# sleep a bit to not piss of server
		# not sure if sleep is necessary here though
		time.sleep(random.randrange(0,42)/100)
		# Download the 30-second preview
		thisSample = requests.get(thisUrl)
		if len(thisSample.content) > 0:
			countTracks += 1
			# Clean up filename
			thisName = thisName.replace('/', '')
			thisName = thisName.replace('\\', '')
			thisName = thisName.replace('.', '')
			saveName = thisFolder + '/' + thisName + '_ID_' + thisID + '.mp3'
			saveName = saveName.replace(":", "")
			saveName = saveName.replace("!", "")
			saveName = saveName.replace('"', '')
			saveName = saveName.replace(":", "")
			saveName = saveName.replace("!", "")
			saveName = saveName.replace('"', '')
			saveName = saveName.replace('?', '')
			saveName = saveName.replace('<', '')
			saveName = saveName.replace('>', '')
			saveName = saveName.replace('\\', '')
			saveName = saveName.replace('*', '')
			saveName = saveName.replace('|', '')
			
			open(saveName, 'wb').write(thisSample.content)
			# add to database
			chosenTracks = chosenTracks.append(track, ignore_index=True)
		else:
			print('One did not download successfully')
	else:
		print('Skipped one due to no sample available')


# And now save csv with the included tracks
		
chosenTracks.to_csv('includedTracks.csv', encoding='utf-8')





































