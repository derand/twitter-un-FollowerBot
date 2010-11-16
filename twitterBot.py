#!/usr/bin/env python
# -*- coding: utf-8 -*-

from oauth import oauth
from oauthtwitter import OAuthApi
import sys
import os

twitter = None
consumerKey = ''
consumerSecret = ''

def auth():
	authToken = None
	authSecret = None
	if os.path.exists('/tmp/twitter.tmp'):
		f = open('/tmp/twitter.tmp', 'r')
		authToken = f.readline().strip()
		authSecret = f.readline().strip()
		print "oauth_token: " + authToken
		print "oauth_token_secret: " + authSecret
		f.close()
	needAuth = True
	if authToken!=None and authSecret!=None:
		twitter = OAuthApi(consumerKey, consumerSecret, authToken, authSecret)
		if twitter.autorized():
			needAuth = False

	if needAuth:
		twitter = OAuthApi(consumerKey, consumerSecret)

		temp_credentials = twitter.getRequestToken()
		print temp_credentials

		print twitter.getAuthorizationURL(temp_credentials)

		oauth_verifier = raw_input('What is the PIN? ')
		access_token = twitter.getAccessToken(temp_credentials, oauth_verifier)
		print access_token

		print("oauth_token: " + access_token['oauth_token'])
		print("oauth_token_secret: " + access_token['oauth_token_secret'])

		f = open('/tmp/twitter.tmp', 'w')
		f.write('%s\n%s'%(access_token['oauth_token'], access_token['oauth_token_secret']))
		f.close()

		twitter = OAuthApi(consumerKey, consumerSecret, access_token['oauth_token'], access_token['oauth_token_secret'])
	return twitter


def unfollow():
	friends = twitter.GetFriendsIDs()
	for i in range(min(len(friends),30)):
		twitter.UnfollowUser(friends[i])


def follow(query):
	users = twitter.searchByQuery(query)
	count = min(30, len(users))
	for user in users:
		print user['id']
		twitter.FollowUser(user['id'])


if __name__=='__main__':
	if len(sys.argv)<2:
		print "Usage: %s <mode>"%sys.argv[0]
		print "Mode:"
		print "  follow   - find and follow by twitter users"
		print "  unfollow - unfollow twitter users"
		print ""
		sys.exit(0)

	if sys.argv[1]=='unfollow':
		twitter = auth()
		unfollow()
	elif sys.argv[1]=='follow':
		twitter = auth()
		follow('twitter')
	
