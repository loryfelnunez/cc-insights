#!/usr/bin/env python
import Queue
from graph import graph
from datetime import datetime, timedelta  

class Manager:
    """
    Manager class for Job management
    This is a wrapper for the PriorityQueue class ordered by date
        - stores Jobs
        - prioritizes jobs (based on time)
        - updates and maintains output formats for specific job types
         

    Created on Fri Nov 6 05:03:17 2015
    @author: Loryfel T. Nunez
    """

    def __init__(self):
        self.q = Queue.PriorityQueue()
        self.total_unicode = 0
        
        
    def put(self, job):
        """ Puts the processed Job in the Queue while maintaining a running count 
            of tweets with non_ascii """
        if job.has_nonascii:
           self.total_unicode += 1 
    	self.q.put(job)

    def get(self):
     	return self.q.get()

    def unicode_output(self):
        return ''.join([str(self.total_unicode), " has unicode\n"])

 
class ManagerGraph(Manager):

    def __init__(self, interval):
        Manager.__init__(self)
        self.graph_controller = graph.GraphController()
        self.interval = interval

    def start(self, initial_time):
        self.graph_controller.start_time = initial_time
        self.graph_controller.end_time = initial_time + timedelta(seconds=self.interval)
       
    def update_graph(self, job):
        self.graph_controller.update(job)

    def get_results(self):
        to_print = self.graph_controller.vertex_avg + "\n"
        return to_print
      

