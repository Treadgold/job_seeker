#!/usr/bin/env python
# name:     job_seeker.py
# version:  0.0.1
# date:     20211129
# author:   Leam Hall
# desc:     Track data on job applications

import argparse
from datetime import datetime as dt
import os.path
import sys




class Job:
    """ Stores the job req data """ 
    def __init__(self, job_data = {}):
        self.title          = job_data.get("title", None)
        self.active         = job_data.get("active", "y")
        self.notes          = job_data.get("notes", None)
        self.company        = job_data.get("company", None)
        self.url            = job_data.get("url", None)
        self.poc_name       = job_data.get("poc_name", None)
        self.last_contact   = job_data.get("last_contact", convert_date(dt.now()))
        self.first_contact  = job_data.get("first_contact", convert_date(dt.now()))

    def __str__(self):
        return "{}\nActive: {}  Notes: {}\n{},  {}\n{} \nLast chat: {}, First chat: {}".format(
            self.title,
            self.active,
            self.notes,
            self.company,
            self.url,
            self.poc_name,
            self.last_contact,
            self.first_contact,
        )

def job_builder(line):
    _list = string_to_list(line)
    data = {
        "last_contact":     _list[0],
        "first_contact":    _list[1],
        "poc_name":         _list[2],
        "company":          _list[3],
        "notes":            _list[4],
        "active":           _list[5],
        "url":              _list[6],
        "title":            _list[7],
    }
    return Job(data)



class POC():
    """ Stores the contact info for each Point of Contact """
    def __init__(self, data = {}):
        self.name   = data.get('name', None)
        self.company        = data.get('company', None)
        self.phone          = data.get('phone', None)
        self.email          = data.get('email', None)
        self.first_contact  = data.get("first_contact", convert_date(dt.now()))
        self.last_contact   = data.get('last_contact', convert_date(dt.now()))

    def __str__(self):
        """ Returns a formatted string with the POC info """
        return "{}, ({}) {}  [{}]\nFirst Contact: {}, Last Contact: {}".format(
            self.name, 
            self.phone,
            self.email,
            self.company,
            self.first_contact,
            self.last_contact)

def poc_builder(line):
    _list = string_to_list(line)
    data = {
        "name":             _list[0],
        "phone":            _list[1],
        "email":            _list[2],
        "company":          _list[3],
        "first_contact":    _list[4],
        "last_contact":     _list[5], 
        }
    return POC(data)
 
def convert_date(date):
    """ Takes a datetime.datetime object and returns a YYYMMDD string """
    return "{}{:0>2}{:0>2}".format(date.year, date.month, date.day)

def list_from_file(filename):
    """ Takes a file, removes comments/empty lines, returns a list of each line """
    lines = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if len(line) > 5 and not line.startswith("#"):
                lines.append(line)
    return lines

def append_to_file(line, filename):
    """ Takes a line and a filename, appends the line to the file """
    with open(filename, 'a') as f:
        f.write("\n" + line + "\n")
            

def parse_list(_list, _list_type, search):
    """ Takes a list, and the element type, and prints any that match search """
    items = [] 
    for element in _list:
        if search.lower() in element.lower():
            if _list_type == "poc":
                items.append(poc_builder(element))
            if _list_type == "job":
                items.append(job_builder(element))
    return items
 
def string_to_list(data, sep = ';'):
    """ Takes a sep separated string and converts it to a list """ 
    return [ e.strip() for e in data.split(sep) ]
 
def is_yes(prompt):
    """ Takes a prompt, returns True/False based on user input """
    yes_choices = ["y", "yes", "yep", "yeah", "yup", "sure", "ok", "okay"]
    no_choices = ["n", "no", "nope", "nah", "no way", "no way jose", "nup", "no thanks"]
    
    if prompt.lower() in yes_choices:
        return True
    elif prompt.lower() in no_choices:
            return False
    else:
        return None

 
def create_new_job():
    """ Creates a new job from user input and appends to data file """
      
    # define the data fields and create a dict to store the data
    data = {
        "last_contact":     0,
        "first_contact":    0,
        "poc_name":         0,
        "company":          0,
        "notes":            0,
        "active":           0,
        "url":              0,
        "title":            0,
    }
    # get the data from the user
    # loop through each field and get the data
    for field in data:
        
        # Check the input is not empty or contains a semicolon
        while True:
            data[field] = input("{}: ".format(field))
            if data[field] == "":
                data[field] = "Null"
                break
            elif ";" in data[field]:
                print("No semicolons allowed")
                continue
            else:
                break
    
    # 20230123;20230201;Fred Smythe; Some Great Place, LLC; linux, ansible, python; y; https://example.com/r12345; Senior Automation Engineer
    new_job = "{}; {}; {}; {}; {}; {}; {}; {}".format(
            data['first_contact'],
            data['last_contact'],
            data['poc_name'],
            data['company'],
            data['notes'],
            data['active'],
            data['url'],
            data['title'],
        )
    
    # print out the new job values
    print(new_job)
    
    # Ask the user if they want to add the job
    if is_yes(input("Add this job?")):
        try:
            # Append the new job to the job file using the append_to_file function
            append_to_file(new_job, os.path.join(datadir, job_file))
            print("New Job added to database")
        except:
            print("Error writing to file")
    else:
        print("Input cancelled")
    
    
    return()



if __name__ == "__main__":

    datadir     = "data"
    job_file    = "jobs.txt"
    poc_file    = "pocs.txt" 
    try:
        poc_list = list_from_file(os.path.join(datadir, poc_file))
        job_list = list_from_file(os.path.join(datadir, job_file))
    except:
        print("Can't find the data files")
        sys.exit(1)

    parser = argparse.ArgumentParser()
    parser.add_argument(
                    "-a", "--add", 
                    help    = "add data, requires -r or -p", 
                    action  = "store_true")
    parser.add_argument(
                    "-j", "--job",
                    help        = "use the Job info",
                    action      = "store_true")
    parser.add_argument(
                    "-p", "--poc", 
                    help        = "use the POC info",
                    action      = "store_true")
    parser.add_argument(
                    "-s", "--search",
                    help    = "SEARCH for",
                    default = "")
    parser.add_argument(
                    "-name", "--name",
                    help   = "POC name",
                    default= "")
    
    args = parser.parse_args()

    if args.add:
        create_new_job()


    if args.job:
        for job in parse_list(job_list, "job", args.search):
            print(job, "\n")
    
    if args.search:
        for job in parse_list(job_list, args.search, args.search):
            print(job, "\n")       
    
    elif args.poc:
        for poc in parse_list(poc_list, "poc", args.search):
            print(poc, "\n")


