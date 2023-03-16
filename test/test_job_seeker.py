# name    :	tests/test_job_seeker.py
# version :	0.0.2
# date    :	20230317
# author  :	Michael Treadgold
# desc    :	Test job_seeker.py
import unittest
import os.path
import tempfile
from datetime import datetime as dt

import job_seeker

class TestJobSeeker(unittest.TestCase):

    def setUp(self):
        self.job_data_1 = {
            "record_number":    "1",
            "last_contact":     "20230123",
            "first_contact":    "20230201",
            "poc_name":         "Fred Smythe",
            "company":          "Some Great Place, LLC",
            "notes":            "linux, ansible, python",
            "active":           "y",
            "url":              "https://example.com/r12345",
            "title":            "Senior Automation Engineer",
        }

        self.poc_data_1 = {
            "record_number":    "1",
            "name":     "Fred Smythe",
            "phone":    "555.555.1212",
            "email":    "fred@example.com",
            "company":  "Example, Inc",
            "first_contact":    "20230123",
            "last_contact":     "20230201",
        }

        self.job_data_2 = {
            "record_number":    "2",
            "last_contact":     "20230123",
            "first_contact":    "20230201",
            "poc_name":         "Jason Jayson",
            "company":          "Can't read resume, Inc",
            "notes":            "windows server, powershell",
            "active":           "n",
            "url":              "https://whocares.com",
            "title":            "Winderz admin",
        }

        self.poc_data_2 = {
            "record_number":    "2",
            "name":     "Jason Jayson",
            "phone":    "br-549",
            "email":    "jay@whocares.com",
            "company":  "Whocares, Inc",
            "first_contact":    "20230101",
            "last_contact":     "20230101",
        }

        self.test_dir   = tempfile.TemporaryDirectory()
        self.data_file  = os.path.join(self.test_dir.name, "data.txt")
        with open(self.data_file, 'w') as f:
            f.write("\n\n\n#bogus line\ngood line\n\n\n")

    def tearDown(self):
        self.test_dir.cleanup()


    def test_convert_date(self):
        date        = dt.now()
        expected    = str(date.year)
        result      = job_seeker.convert_date(dt.now())
        self.assertTrue(result.startswith(expected))

    def test_string_to_list(self):
        my_str      = "linux;  python;  ansible      "
        expected    = ["linux", "python", "ansible"]
        result      = job_seeker.string_to_list(my_str)
        self.assertTrue(result == expected)

    def test_job_defaults(self):
        j       = job_seeker.Job()
        date    = dt.now()
        year    = str(date.year)
        self.assertTrue(j.last_contact.startswith(year))
        self.assertTrue(j.first_contact.startswith(year))
        self.assertTrue(j.active == "y")

    def test_job_data(self):
        j = job_seeker.Job(self.job_data_1)
        self.assertTrue(j.record_number == "1")
        self.assertTrue(j.last_contact  == "20230123")
        self.assertTrue(j.first_contact == "20230201")
        self.assertTrue(j.poc_name      == "Fred Smythe")
        self.assertTrue(j.company       == "Some Great Place, LLC")
        self.assertTrue(j.notes         == "linux, ansible, python")
        self.assertTrue(j.active        == "y")
        self.assertTrue(j.url           == "https://example.com/r12345")
        self.assertTrue(j.title         == "Senior Automation Engineer")

    def test_job_builder(self):
        job_line = "2; Automation Engineer; Yes; Excel, Python, Bash, VBA; sprint; sprint.com; Ulysees; 2023; 2023"
        job = job_seeker.job_builder(job_line)
        self.assertTrue(job.title == "Automation Engineer")

    def test_poc_defaults(self):
        p       = job_seeker.POC()
        date    = dt.now()
        year    = str(date.year)
        self.assertTrue(p.name  == None)
        self.assertTrue(p.email == None)
        self.assertTrue(p.phone == None)
        self.assertTrue(p.first_contact.startswith(year))
        self.assertTrue(p.last_contact.startswith(year))
    
    def test_poc_data(self):
        p   = job_seeker.POC(self.poc_data_1)
        self.assertTrue(p.record_number == "1")
        self.assertTrue(p.name          == "Fred Smythe")
        self.assertTrue(p.phone         == "555.555.1212")
        self.assertTrue(p.email         == "fred@example.com")             
        self.assertTrue(p.company       == "Example, Inc")
        self.assertTrue(p.first_contact == "20230123")
        self.assertTrue(p.last_contact  == "20230201")

    def test_poc_string(self):
        p       = job_seeker.POC(self.poc_data_1)
        results = p.__str__().split("\n")
        self.assertTrue(results[0] == "record_number: 1")
        self.assertTrue(results[1] == "name: Fred Smythe")
       
    def test_list_from_file(self):
        l = job_seeker.list_from_file(self.data_file)
        self.assertTrue(len(l) == 1)
        self.assertTrue(l[0] == "good line") 
      
    def test_parse_list(self):
        pass

    def test_create_new_job(self):
        pass

    def test_is_yes(self):
        self.assertTrue(job_seeker.is_yes("y"))
        self.assertTrue(job_seeker.is_yes("Yes"))
        self.assertFalse(job_seeker.is_yes("No"))
        self.assertFalse(job_seeker.is_yes("n"))