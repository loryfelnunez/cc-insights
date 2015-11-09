"""
Clean and extract the text from the raw JSON tweets that come from the Twitter Streaming API
and track the number of tweets that contain unicode.

Requirements for a "clean" Tweet 
    - all of the escape characters are replaced 
    - unicode have been removed.
    - do not process empty tweets or tweets with an empty timestamp

Assumptions
    - each tweet is JSON formatted
    - each tweet is sorted by datetime, earlier tweets come in first
   
Created on Fri Nov 6 05:03:17 2015
@author: Loryfel T. Nunez
"""

import argparse
import logging
from job import Job
from manager import Manager


if __name__=="__main__":
    
    # command line args
    parser = argparse.ArgumentParser(description="Cleaning Tweets")    
    parser.add_argument("infile", help="Tweet Input file (JSON)")
    parser.add_argument("outfile", help="Cleaned Tweets output file")
    args = parser.parse_args()

    logging.basicConfig(filename='tweets_cleaned.log', filemode='w', level=logging.DEBUG)

    # Instantiate a class that manages processes and resources
    manager = Manager()

    # use a+ so we can add the total number of tweets with unicode after  the tweet-by-tweet processing
    with open(args.infile) as input_fp, open(args.outfile, 'a+') as output_fp:

        lines = input_fp.readlines()

        # make sure output file is empty
        output_fp.truncate()

        # each line is a JSON formatted tweet    
        for line in lines:        

            # specify job id, job data and job type
            job = Job(line)    
            job.clean_data()
            job.validate()

            if job.is_valid:
                manager.put(job)
                output_fp.write(str(manager.get()))
        
        output_fp.write(manager.unicode_output())  
