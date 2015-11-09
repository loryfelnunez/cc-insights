import unittest
from datetime import datetime, timedelta 
from src.text import clean
from src.job import Job, JobGraph
# hack to find the job module used in the import graph statement below
import sys
sys.path.append("./src")
from src.graph import graph


class TestClean(unittest.TestCase):
    
    def test_is_only_punct(self):
        test_string = "?!....."
        self.assertEqual(clean.is_only_punct(test_string), True)

    def test_replace_escape_chars(self):
        test_string_1 = "Listening to liveband at Full Tank \\m\/ (at @KilangBateri in Johor Bahru, Johor) https:\/\/t.co\/5mYqnqW7yG"
        expected_output_1 = "Listening to liveband at Full Tank \m/ (at @KilangBateri in Johor Bahru, Johor) https://t.co/5mYqnqW7yG"
        self.assertEqual(clean.replace_escape_chars(test_string_1), expected_output_1)


    def test_strip_non_ascii(self):
        test_string_1 = u"I knew my old ford couldn't run her down, she probly didn't like me anyhow\ud83c\udfb6\ud83c\udfb5\ud83d\udd0a"
        expected_output_1 = "I knew my old ford couldn't run her down, she probly didn't like me anyhow"
        self.assertEqual(clean.strip_non_ascii(test_string_1), expected_output_1)
        test_string_2 = u"\ud83d\ude14"
        expected_output_2 = ""
        self.assertEqual(clean.strip_non_ascii(test_string_2), expected_output_2)



class TestJob(unittest.TestCase):
    """ Fixture for the Job class """
    def setUp(self):
        text = u"{\"created_at\":\"Fri Oct 30 15:29:45 +0000 2015\",\"id\":659789756637822976,\"id_str\":\"659789756637822976\",\"text\":\"@IKEA complain https:\/\/t.co\/GzyHJC6jMI\"}"
        self.job = Job(text)
        self.job.clean_data()

    def tearDown(self):
        self.job = None

    def test_print_job(self):
        """ Correct format ensures proper object consistency """
        expected_output = "@IKEA complain https://t.co/GzyHJC6jMI (timestamp: Fri Oct 30 15:29:45 +0000 2015)\n"
        str_job = str(self.job)
        self.assertEqual(str_job, expected_output)

    def test_validity(self):
        """ Check if validity flags for text are set """
        self.assertEqual(self.job.has_nonascii, False)
        self.assertEqual(self.job.is_valid, True)

            
class TestGraph(unittest.TestCase):
    """ Fixture for the Graph Class """
    def setUp(self):
        self.graph = graph.GraphController()
        text1 = u"{\"created_at\":\"Fri Oct 30 15:29:30 +0000 2015\",\"id\":1,\"id_str\":\"1\",\"text\":\"#Spark and #hadoop are in\"}"
        self.job1 = JobGraph(text1)
        self.graph.start_time =  self.job1.date
        self.graph.end_time = self.job1.date + timedelta(seconds=60)
        text2 = u"{\"created_at\":\"Fri Oct 30 15:29:31 +0000 2015\",\"id\":2,\"id_str\":\"2\",\"text\":\"#Cloudera and #HADOOP are in\"}"
        self.job2 = JobGraph(text2)
        text3 = u"{\"created_at\":\"Fri Oct 30 15:30:30 +0000 2015\",\"id\":3,\"id_str\":\"3\",\"text\":\"#Python and #C++ are in\"}"
        self.job3 = JobGraph(text3)
        self.graph.update(self.job1)
        self.graph.update(self.job2)
        self.graph.update(self.job3)


    def tearDown(self):
        self.job = None

    def test_insert(self):
        ok = False
        if "#CLOUDERA~#HADOOP" in self.graph.edge_time and "#CLOUDERA" in self.graph.vertex_degree and "#CLOUDERA" in self.graph.vertex_edgeblock:
            ok = True
        self.assertEqual(ok, True)


    def test_ageoff(self):
        in_edge_list = False
        if "#SPARK~#HADOOP" in self.graph.edge_time:
            in_edge_list = True
        self.assertEqual(in_edge_list, False)


suite = unittest.TestLoader().loadTestsFromTestCase(TestClean)
testResult = unittest.TextTestRunner(verbosity=2).run(suite)

suite = unittest.TestLoader().loadTestsFromTestCase(TestJob)
testResult = unittest.TextTestRunner(verbosity=2).run(suite)

suite = unittest.TestLoader().loadTestsFromTestCase(TestGraph)
testResult = unittest.TextTestRunner(verbosity=2).run(suite)


   