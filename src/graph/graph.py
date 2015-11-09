
"""
The data structures used in this class are adopted from STINGER, an open source framework for temporal graph analysis
http://cass-mt.pnnl.gov/docs/pubs/pnnlgeorgiatechsandiastinger-u.pdf

We could have linked our implementation to STINGER's Python interface (albeit still experimental),
but then decided to implement the STINGER's base data structures in Python to gain a better understanding of its implementation.

There are 3 main data structures:
1. vertex_degree -- This keeps track of the degrees of the source vertex.  This implemented as a Dictionary {source_vertex1: # of degree, source_vertex2: # of degree, ..}
2. vertex_edgeblock -- Each source vertex points to an edgeblock.  An edgeblock contains a list of the end vertices and its corresponding timestamp.
This is implemented as a Dictionary of Dictionary where {source_vertex: {end_vertex1:time, end_vertex2:time, ....}}
3. edge_time -- This contains edges and the lastest time when the edge was added {edgeA~edgeB:11:01PM, edgeC~edgeD:11:02PM}

The Stinger C++ implementation uses Arrays and Pointers to the related data structures (edgeblocks, etc).  It also has preallocated array sizes and blocks, reuses array blocks
and uses holes or negative values to connote a deleted edge.  This Python implementation uses Dictionaries.

Updates using the STINGER framework is fast since only the affected edge/vertex is updated through either increment/decrement or and insert/delete in the Dictionary class
Lookups, insertions and deletions in Python dictionaries are O(1) average case and O(n) worst case.  There are a couple of instances where we needed to maintain
a copy of the original dictionary which increases memory and is O(n).  This might be a place for optimization. 

DEVLOG 8 -- STINGER literature


Created on Fri Nov 7 06:25:17 2015
@author: Loryfel T. Nunez
"""
from __future__ import division
from job import Job
import collections
from datetime import datetime, timedelta  


class GraphController:

    def __init__(self):

        self.start_time = ''
        self.end_time = ''
        self.vertex_edgeblock = {}
        self.vertex_degree = {}
        self.edge_time = {}
        self.vertex_avg = "0.00"

    def update(self, job):
        """ Update the 3 data structures and checks the time interval """
        self.insert(job)
        self.checkpoint(job)
        self.get_results()

  
    def get_results(self):
        """ Populates self.vertex_avg, which is the running average of all 
        the active vertices at that point in time """
        count = 0
        sum_value = 0
        if len(self.vertex_degree) == 0:
            self.vertex_avg = "0.00" # string for printing
            return
        for key, value in (self.vertex_degree).iteritems():
            sum_value += value
            count += 1
        ave = sum_value / count
        self.vertex_avg = "{0:.2f}".format(sum_value / count)
        

    def ageoff(self, remove_from):
        """ Removes edges and their corresponding vertices if it is <= time window of the latest tweet """
        edge_time = (self.edge_time).copy()
        for key, value in edge_time.iteritems():
            if value <= remove_from:
                edges = key.split('~')
                source_vertex  = edges[0]
                end_vertex = edges[1]
                self.delete(source_vertex, end_vertex, remove_from)

    def insert(self, job):
        """ Add to the data structures """

        # Do not insert if there are less than 2 hashtags, but still use the Tweet's time
        # for the purpose of checkpointing the time window
        if len(job.hash_tags) < 2:
            return

        # n^2 here to create a complete graph for the hashtags
        for h in job.hash_tags:
            other_tags = (job.hash_tags).copy()
            other_tags.remove(h)
            
            for o in other_tags:
                edge_key = h + '~' + o
                # update edgeblock where h is the source_vertex and o is the end_vertex
                if h in self.vertex_edgeblock:
                    od = self.vertex_edgeblock[h]
                    od[o] = job.date
                    self.vertex_edgeblock[h] = od
                else:
                    # possible optimization, DEVLOG 9
                    od = collections.OrderedDict()
                    od[o] = job.date
                    self.vertex_edgeblock[h] = od

                # update edge list, with the latest time
                self.edge_time[edge_key] = job.date
            
            # update vertex_degree, for h (source_vertex) -- its degree is just the size of the edgeblock     
            v = len(self.vertex_edgeblock[h])
            self.vertex_degree[h] = v


    def checkpoint(self, job):
        """ Check if current job's timestamp >= the max window """
        if job.date >= self.end_time:
            removetime = job.date - timedelta(seconds=60)
            # removetime is relative to the current job time
            self.ageoff(removetime)

            # Reset start and end time
            self.start_time = job.date
            self.end_time = self.start_time + timedelta(seconds=60)
           
        
    def delete(self, source_vertex, end_vertex, remove_from):
        """ Checks the timestamp of the candidate vertices and edges
        and deletes them if its time <= current job time - window """

        od = self.vertex_edgeblock[source_vertex]
        if od[end_vertex] <= remove_from:       
            # delete from edgeblock
            del od[end_vertex]
            # update vertex_edgeblock with new od
            self.vertex_edgeblock[source_vertex] = od
            # update degrees
            self.vertex_degree[source_vertex] = len(od)
        key = source_vertex + '~' + end_vertex
        if self.edge_time[key] <= remove_from:
            del self.edge_time[key]
        
      






