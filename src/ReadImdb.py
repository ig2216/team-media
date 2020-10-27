'''
Created on Oct 23, 2020

@author: haishan
'''
import requests
import json


def getMoviebyYear(movieyear):
		
	result = []
		
	omdb_api_key = '2dcdc723'
	endpoint = 'http://www.omdbapi.com/?'
	parameters = {

        't': 'm*',    
		'y': movieyear,
		'apiKey' : omdb_api_key

	}
	
	resp = requests.get(endpoint, params=parameters)
 
	data = resp.json()
	 
	return data	

		
def getMovie(movieid):
 
	result = []
 
	omdb_api_key = '2dcdc723'
	endpoint = 'http://www.omdbapi.com/?'
	parameters = {
 
		'i': movieid,
		'apiKey' : omdb_api_key,

	}
 
	resp = requests.get(endpoint, params=parameters)
 
	data = resp.json()
	 
	return data
	 

print(getMoviebyYear('2020'))	 
print(getMovie('tt3896198'))
