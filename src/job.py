#!/usr/bin/env python
import logging
from text import clean
import json
#from src.graph import graph

class Job:
    """
        Constructs each Tweet to be processed as a Job.
        This class does the basic methods that extract and clean required information from 
        the Tweet to make to ready for further processing
        Required params:
            text - string representation of the Tweet JSON 
                  
    """

    def __init__(self, text):  

        # Initialize with default vals.  If vals are still default even after object
        # creation, then that will help us flag the object for errors
        self.date = ""
        self.clean_text = ""
        self.text_date = ""

        # A valid Job instance must have a JSON text with tweet content and time
        self.text = text
        self.json_text = json.loads(self.text) # DEVLOG 5 - This can be modularized for bigger systems
        self.get_time()

        # DEVLOG 6 - Not necessary (commented out), but having unique ID is helpful
        # self.tweet_id = self.get_id()

        # DEVLOG 2 - for the priority queue, not really necessary since we assume the tweets are in order
        # used in __comp__
        self.priority = self.date
         
        # update object's internal state
        self.has_nonascii = False
        self.is_valid = True

        
    def __str__(self):
        """ String represenation of Job, application specific"""
        # output this to ft1.txt
        return self.clean_text + " (timestamp: " + self.text_date + ")\n"

    def __cmp__(self, other):
        """ Sorts the Job according to timestamp using a Priority Queue """
        return cmp(self.priority, other.priority)

    # Additional feature, DEVLOG 6
    # def get_id(self):
    #    if 'id_str' in self.json_text:
    #        self.tweet_id = self.json_text['id_str']
    
    def clean_data(self):
        """ Updates:
                self.clean_text and 
                self.has_nonascii
            - remove escape chars 
            - remove non ASCII string
        """    
        if 'text' in self.json_text:
            text_utf8 = (self.json_text['text']).encode('utf8')
            text_escaped = clean.replace_escape_chars(text_utf8)
            try:
                self.clean_text = text_escaped.decode('ascii').strip()
            except UnicodeDecodeError:
                self.has_nonascii = True
                # remove the non ASCII string
                self.clean_text = clean.strip_non_ascii(text_escaped).strip()


    def get_time(self):
        """ Updates:
            self.text_date - text representation of the date of the tweet
            self.date - date object representation, to be used for sorting 
        """
        if 'created_at' in self.json_text: 
            self.text_date = self.json_text['created_at'] 
            self.date = clean.convert_to_date(self.text_date)
    

    def validate(self):    
        """ Tweet is valid if text and date are valid, if invalid, log"""
        # write first 80 chars to log, Job obj flags the job is NOT valid if there is no text  
        # not account for Tweets that start with {"limit":
        if not self.clean_text:   
            self.is_valid = False
            logging.warning("Invalid text content. JSON entry: %s ..... ", (self.text)[0:80] )
        elif not self.text_date:     
            self.is_valid = False
            logging.warning("Invalid date content. JSON entry: %s ..... ", (self.text)[0:80] )
        # DEVLOG 7, cleaning up punctuation
        # elif clean.is_only_punct(self.clean_text):   
        #    self.is_valid = False
        #    logging.warning("Content only has punctuation. JSON entry: %s ..... ", (self.text)[0:50] )



class JobGraph(Job):
    """ Subclass of Job Class 
            Extends Job by adding Graph functionality
    """

    def __init__(self, line):

        Job.__init__(self, line)
        # use the hashtags attribute, or reuse feature 1 functions, chose latter
        self.clean_data()
        self.hash_tags = clean.get_hash_tags(self.clean_text)
        self.validate_hashtags()

    def validate_hashtags(self):
        if len(self.hash_tags) <= 1:
                self.is_valid = False
        
