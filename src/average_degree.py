"""
Calculate the average degree of a vertex in a Twitter hashtag graph for the last 60 seconds, 
and update this each time a new tweet appears.


Created on Fri Nov 6 05:03:17 2015
@author: Loryfel T. Nunez
"""

import argparse
from job import Job, JobGraph
from manager import Manager, ManagerGraph


if __name__=="__main__":
    
    # command line args
    parser = argparse.ArgumentParser(description="Get the Vertex Average")    
    parser.add_argument("infile", help="Tweet Input file (JSON)")
    parser.add_argument("outfile", help="Output file with the vertex degrees")
    args = parser.parse_args()

    # Instantiate a class manages processes and resources
    # ManagerGraph inherits from Manager and takes in a time Window in Seconds
    # where Window is the time when we refresh the graph
    # DEVLOG No. 3, 4

    manager = ManagerGraph(60)

    with open(args.infile) as input_fp, open(args.outfile, 'w') as output_fp:

        lines = input_fp.readlines()

        # each line is a JSON formatted tweet  
        has_started = False  
        for line in lines:        
            # specify job id, job data and job type
            job = JobGraph(line)  
            if job.date == "":
                continue
            if has_started == False:
                manager.start(job.date)
                has_started = True
            manager.put(job)
            manager.update_graph(job)
            output_fp.write(manager.get_results())
                