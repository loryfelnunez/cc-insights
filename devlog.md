Devlog

1. Job Class - can convert to a Simple Factory class for each of the feature by using @classmethod to create different job type
or since we are just extending do via inheritance

2. logging - limit 
Rotating log file



3. Dictionary not as global 

4. python 2.7 - new laptop clean install of anaconda python 2.7
dateutile version

5. again the module relative import brain freeze

7. data -gen for testing

8. modularize Manager and Job using inheritance

9.  how many tweets per minute
need to process a minute of tweets in less than a minute

10. maybe use hashtags to speed up since we are parsing the json anyway
11. hand calculate to 

12.Optimization: used generators

------

1. Use of Python 2.7.  I was torn with using Python 3x vs 2.7 

2. This implementation can support tweets that do not come in datetime order using a PriorityQueue.  In a bigger  system, we can have a 
process/machine as the Tweet Ingester where its only mission in life is to get Tweets from Twitter and our Tweet Analyzer programs will just
get from the Tweet Ingester. This implementation tries to emulate it by using the Tweet Date is the priority for the Tweet Priority Queue.  We added an overhead
here of O(n log n) for the Priority Queue.

3. Additional feature to allow user to specify time window in seconds

4. ManagerGraph inherits from Manager class to extend Manager class to call graph module

5. We assume a JSON input, but to make code extensible, we can OOP this line (self.json_text = json.loads(self.text)) and make it into a Generic Converter class
that can take in other formats (XML, txt, etc) and it will just return to us the necessary info for the Job class.  

6. Getting the Twitter ID is not part of the coding challenge, but having a unique ID is very helpful to cross reference data.

7. Filtering tweets with punctuation only is not part of the challenge. 

8. Related Literature for Stringer

9. Use of OrderedDict to possibly optimize removal of aged-off items.  Maybe even use an LRU cache?  Need to think more about it.

  


         
