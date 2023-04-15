# name    :	tests/test_job_seeker.py
# version :	0.0.2
# date    :	20230317
# author  :	Michael Treadgold
# desc    :	Test job_seeker.py
import unittest
from unittest.mock import patch
import os.path
import tempfile
from datetime import datetime as dt

import job_seeker

JOB_FIELDS = [
    "record_number",
    "title",
    "active",
    "notes",
    "company",
    "url",
    "poc_name",
    "last_contact",
    "first_contact"
]

POC_FIELDS = [
    "record_number",
    "name",
    "company",
    "phone",
    "email",
    "first_contact",
    "last_contact"
]

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
            f.write("\n\n\n#bogus line\ngood line\n\n\nBrian; 555-555-5555\n")
            
        self.test_list_from_file = ["2; Automation Engineer; Yes; Excel, Python, Bash, VBA; sprint; sprint.com; Ulysees; 2023; 2023", "3; Junior Developer; Yes; PYthon, Javascript, Kubernetes, Docker; localcompany; local.comp.com; James Battersey; 2023; 2023"]
        self.test_line_job = "9; Junior Developer; Yes; PYthon, Javascript, Kubernetes, Docker; localcompany; local.comp.com; James Battersey; 2023; 2023"
        self.test_line_poc = "12; Killian; Run Fast; 8666544646; kill@run.com; 2023; 2023"
        
        self.job_record_file = os.path.join(self.test_dir.name, "jobs.txt")
        with open(self.job_record_file, 'w') as f:
            f.write("\n2; Automation Engineer; Yes; Excel, Python, Bash, VBA; sprint; sprint.com; Ulysees; 2023; 2023\n")
            f.write("3; Junior Developer; Yes; PYthon, Javascript, Kubernetes, Docker; localcompany; local.comp.com; James Battersey; 2023; 2023")
            f.write("4; Linux Server Admin; Yes; Arch, Redhat, NGIX, docker; Company number 7; comp7.com; Martin Freeman; 20230314; 20230112\n")
            f.write("5; LEad Deve; Yes; Python; Happy Cow Dev Ltd; HCDL; Julian Bishop; 2023; 2023\n")
            f.write("6; Mister-Programmer-guy; Yes; Just the business; DolphinExperience; DE.com; Haley; 20230321; 20230321\n")
            
        self.poc_record_file = os.path.join(self.test_dir.name, "pocs.txt")
        with open(self.poc_record_file, 'w') as f:
            f.write("\n1; Frank Green Zappa; United Music Federation; 0225 666 444; zappa@UMF.com; 2023; 2023\n")
            f.write("\n2; Killian; Run Fast; 8666544646; kill@run.com; 2023; 2023\n")
            f.write("\n3; Shannon Docherty; JustInTime; 545488844; shannon@JIT.com; 2023; 2023\n")
            f.write("\n4; Jason Bourne; Blackrock; 555-898-9944; jason@blackrock.quiet.com; 20070305; 20220118\n")

        
        

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

    def test_builder(self):
        job_line = "2; Automation Engineer; Yes; Excel, Python, Bash, VBA; sprint; sprint.com; Ulysees; 2023; 2023"
        job = job_seeker.builder(job_line, "job")
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
        self.assertTrue(len(l) == 2)
        self.assertTrue(l[0] == "good line") 
        self.assertTrue(l[1] == "Brian; 555-555-5555")
        
      
    def test_parse_list(self):
        _list = job_seeker.parse_list(self.test_list_from_file, "poc", "Sprint")
        self.assertTrue(len(_list) == 1, msg = {len(_list)})
        self.assertTrue(_list[0].__str__() == 'record_number: 2\nname: Automation Engineer\ncompany: Yes\nphone: Excel, Python, Bash, VBA\nemail: sprint\nfirst_contact: sprint.com\nlast_contact: Ulysees')
        pass

    def test_insert_new_item(self):
        data = { 
                "record_number": 27,
                "title": "fred",
                "active": "y",
                "notes": "y", 
                "company": "y",
                "url": "y",
                "poc_name": "y",
                "last_contact": 20230413,
                "first_contact": 20230413,
                }
        job_seeker.insert_new_item(data, self.job_record_file, "job")
        with open(self.job_record_file) as f:
            lines = f.readlines()
            self.assertTrue(lines[-1] == "27; fred; y; y; y; y; y; 20230413; 20230413\n")
        
    def test_get_next_record_number(self):
        next_record_number = job_seeker.get_next_record_number(self.job_record_file)
        self.assertTrue(next_record_number == 7)

    def test_is_yes(self):
        self.assertTrue(job_seeker.is_yes("y"))
        self.assertTrue(job_seeker.is_yes("Yes"))
        self.assertFalse(job_seeker.is_yes("No"))
        self.assertFalse(job_seeker.is_yes("n"))
        
    def test_get_user_data(self):
        input_values = ['input_1',
                        'input_2',
                        'input_3',
                        "input_4",
                        "input_5",
                        "input_6",
                        "20230413",
                        "20230413",
                        ]
        fields = [  7,
                    "title",
                    "active",
                    "notes",
                    "company",
                    "url",
                    "poc_name",
                    "last_contact",
                    "first_contact"
                    ]
        correct_output = {  'record_number' : 7,
                            'title'         : 'input_1',
                            'active'        : 'input_2',
                            'notes'         : 'input_3',
                            'company'       : 'input_4',
                            'url'           : 'input_5',
                            'poc_name'      : 'input_6',
                            'last_contact'  : '20230413',
                            'first_contact' : '20230413',
                            }
        
        with patch('builtins.input', side_effect=input_values):
            self.maxDiff = None
            self.assertEqual(job_seeker.get_user_data(fields), correct_output)
        
    
    def test_insert_new_item(self):
        _inputs = ["y"]
        with patch('builtins.input', side_effect=_inputs):
            job_seeker.insert_new_item(self.test_line_job, self.job_record_file, "job")
        with open (self.job_record_file) as f:
            lines = f.readlines()
            self.assertTrue(lines[-1] == self.test_line_job + "\n")
        
        with patch('builtins.input', side_effect=_inputs):
            job_seeker.insert_new_item(self.test_line_poc, self.poc_record_file, "poc")
        with open (self.poc_record_file) as f:
            lines = f.readlines()
            self.assertTrue(lines[-1] == self.test_line_poc + "\n")
        
    def test_update_record(self):
        _input = ["Harry Potter",
                  "company five",
                  "555-865865",
                  "harry_potter@five.com",
                  "20230401",
                  "20230112",
                  "y",
                ]
        _string = "4; Harry Potter; company five; 555-865865; harry_potter@five.com; 20230401; 20230112"          
        with patch('builtins.input', side_effect=_input):
            job_seeker.update_record('poc', 4, self.poc_record_file)
        with open (self.poc_record_file) as f:
            lines = f.readlines()
            self.assertTrue(lines[-1] == _string, msg = {lines[-1], _string})        
    
    def test_delete_record(self):
        with patch('builtins.input', side_effect=["y"]):
            job_seeker.delete_record(4, self.poc_record_file, 'poc')
        with open (self.poc_record_file) as f:
            lines = f.readlines()
            self.assertTrue(lines[-1] == "3; Shannon Docherty; JustInTime; 545488844; shannon@JIT.com; 2023; 2023") 
    
    def test_append_to_file(self):
        job_seeker.append_to_file(self.test_line_job, self.job_record_file)
        with open (self.job_record_file) as f:
            lines = f.readlines()
            self.assertTrue(lines[-1] == self.test_line_job + "\n")
    
    
