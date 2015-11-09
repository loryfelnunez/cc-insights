Submission to Insight Data Engineering - Coding Challenge 
===========================================================

The solution is implemented in Python 2.7 

## How to run
1. Populate tweet_input/tweets.txt with JSON formatted tweets
2. Run ./run.sh in the topmost directory.  
	Feature 1 This will run tweets_cleaned.py with the output in tweet_output/ft1.txt
	Feature 2 This will run average_degree.py with the output in tweet_output/ft2.txt
3. For testing, go to the tests/ folder and run run_tests.sh in that folder.  This will run the following:
	Unit Test
	Scalability and Timing Tests
	Acceptance/Integration Test
   Test input are in tweet_input.  big_tweets.txt is the output of the data-gen module.
   Tests output will be shown in stdout.

## Description

# Feature 1

Clean and extract the text from the raw JSON tweets that come from the Twitter Streaming API, and track the number of tweets that contain unicode.

# Feature 2

Calculate the average degree of a vertex in a Twitter hashtag graph for the last 60 seconds, and update this each time a new tweet appears.

 
