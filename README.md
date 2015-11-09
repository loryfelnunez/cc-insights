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
4. tweet_output folder contains output files from the test suite and expected output files to be used in the Acceptance tests. As per the Coding challenge -- f1.txt and f2.txt are the standard output, feel free to overwrite these files.
5. For code review, comments may have some DEVLOG entries.  You can refer to devlog.md in the topmost directory to reference the DEVLOG entry number.

## Description

This is an OOP approach to 

### Feature 1

Clean and extract the text from the raw JSON tweets that come from the Twitter Streaming API, and track the number of tweets that contain unicode.

### Details



## Feature 2

Calculate the average degree of a vertex in a Twitter hashtag graph for the last 60 seconds, and update this each time a new tweet appears.

### Details

The data structures used are adopted from STINGER, an open source framework for temporal graph analysis
http://cass-mt.pnnl.gov/docs/pubs/pnnlgeorgiatechsandiastinger-u.pdf

We could have linked our implementation to STINGER's Python interface (albeit still experimental),
but then decided to implement the STINGER's base data structures in Python to gain a better understanding of its implementation.

There are 3 main data structures:
1. vertex_degree -- This keeps track of the degrees of the source vertex.  This implemented as a Dictionary {source_vertex1: # of degree, source_vertex2: # of degree, ..}
2. vertex_edgeblock -- Each source vertex points to an edgeblock.  An edgeblock contains a list of the end vertices and its corresponding timestamp.
This is implemented as a Dictionary of Dictionary where {source_vertex: {end_vertex1:time, end_vertex2:time, ....}}
3. edge_time -- This contains edges and the lastest time when the edge was added {edgeA~edgeB:11:01PM, edgeC~edgeD:11:02PM}

The Stinger C++ implementation uses Arrays and Pointers to the related data structures (edgeblocks, etc).  It also has preallocated array sizes and blocks, reuses array blocks and uses holes or negative values to connote a deleted edge.  This Python implementation uses Dictionaries.

Updates using the STINGER framework is fast since only the affected edge/vertex is updated through either increment/decrement and/or  insert/delete in the Dictionary class. Lookups, insertions and deletions in Python dictionaries are O(1) average case and O(n) worst case.  There are a couple of instances where we needed to maintain a copy of the original dictionary which increases memory and is O(n).  This might be a place for optimization. 

 
