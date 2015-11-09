#!/usr/bin/env python
import os
import filecmp
import time

# Unit tests -- run it from main
os.chdir( ".." )
os.system("python -m tests.unit_tests")
os.chdir( "src/" )

# Scalability/Timing Tests

start_time = time.time()
os.system("python tweets_cleaned.py ../tweet_input/big_tweets.txt ../tweet_output/ft1_bigtweets.txt")
end_time = time.time()
print("Elapsed time for FEATURE 1 for 9993 tweets was %g seconds" % (end_time - start_time))
start_time = time.time()
os.system("python  average_degree.py ../tweet_input/big_tweets.txt ../tweet_output/ft2_bigtweets.txt")
end_time = time.time()
print("Elapsed time for FEATURE 2 for 9993 tweets was %g seconds" % (end_time - start_time))
 

# Acceptance tests for Feature 1

print (" START ACCEPTANCE/INTEGRATION TESTS ")
os.system("python tweets_cleaned.py ../tweet_input/small_tweets1.txt ../tweet_output/ft1_test.txt")
if filecmp.cmp('../tweet_output/ft1_test.txt', '../tweet_output/ft1_expected.txt'):
    print 'Feature 1 Acceptance Test (1) -- PASSED'
else:
    print 'Feature 1 Acceptance Test (1) -- FAILED, compare ../tweet_output/ft1_test.txt and ../tweet_output/ft1_expected.txt '
if filecmp.cmp('../tweet_output/tweets_cleaned.log', '../src/tweets_cleaned.log'):
    print 'Logging -- PASSED'
else: 
    print 'Problems with logging'

# Acceptance tests for Feature 2
os.system("python average_degree.py ../tweet_input/small_tweets1.txt ../tweet_output/ft2_test_1.txt")
if filecmp.cmp('../tweet_output/ft2_test_1.txt', '../tweet_output/ft2_expected_1.txt'):
    print 'Feature 2 Acceptance Test (1) -- PASSED'
else:
    print 'Feature 2 Acceptance Test (1) -- FAILED, compare ../tweet_output/ft2_test_1.txt and ../tweet_output/ft2_expected_1.txt '

os.system("python ../src/average_degree.py ../tweet_input/small_tweets2.txt ../tweet_output/ft2_test_2.txt")
if filecmp.cmp('../tweet_output/ft2_test_2.txt', '../tweet_output/ft2_expected_2.txt'):
    print 'Feature 2 Acceptance Test (2) -- PASSED'
else:
    print 'Feature 2 Acceptance Test (2) -- FAILED, compare ../tweet_output/ft2_test_2.txt and ../tweet_output/ft2_expected_2.txt '
print (" END ACCEPTANCE/INTEGRATION TESTS ")

 