#!/usr/bin/env python
# name:     job_seeker.py
# version:  0.1.2
# date:     20230316
# author:   Leam Hall, Michael Treadgold
# desc:     Track data on job applications

import argparse
from datetime import datetime as dt
import os.path
import sys
import os

# Define data fields for both Job and POC
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


class Job:
    """Stores the job req data"""
    def __init__(self, job_data={}):
        
        for field in JOB_FIELDS:
            setattr(self, field, job_data.get(field, None))

        # Set default values for specific attributes
        self.active = job_data.get("active", "y")
        self.last_contact = job_data.get("last_contact", convert_date(dt.now()))
        self.first_contact = job_data.get("first_contact", convert_date(dt.now()))


    def __str__(self):
        field_values = ["{}: {}".format(field, getattr(self, field)) for field in JOB_FIELDS]
        return "\n".join(field_values)


class POC:
    """Stores the contact info for each Point of Contact"""

    def __init__(self, data={}):

        for field in POC_FIELDS:
            setattr(self, field, data.get(field, None))

        # Set default values for specific attributes
        self.first_contact = data.get("first_contact", convert_date(dt.now()))
        self.last_contact = data.get("last_contact", convert_date(dt.now()))

    def __str__(self):
        """Returns a formatted string with the POC info"""
        field_values = ["{}: {}".format(field, getattr(self, field)) for field in POC_FIELDS]
        return "\n".join(field_values)
    

def list_from_file(filename):
    """Takes a file, removes comments/empty lines, and returns a list of each line."""
    lines = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if len(line) > 0 and not line.startswith("#"):
                lines.append(line)
    return lines


def is_yes(prompt):
    """ Takes a prompt, returns True/False based on user input """
    yes_choices = ["y", "yes", "yep", "yeah", "yup", "sure", "ok", "okay"]
    return prompt.lower() in yes_choices


def convert_date(date):
    """ Takes a datetime.datetime object and returns a YYYYMMDD string """
    return "{}{:0>2}{:0>2}".format(date.year, date.month, date.day)


def builder(line, _list_type):
    print(_list_type)
    print(line)
    _list = string_to_list(line)
    
    if _list_type == "job":
        _fields = JOB_FIELDS
    else:
        _fields = POC_FIELDS
    
    data = {field: _list[idx] for idx, field in enumerate(_fields)}
    if _list_type == "job":
        return Job(data)
    else:
        return POC(data)
    


def parse_list(_list, _list_type, search, _option=None):
    """ Takes a list of strings, and the element to search, and returns a list of RECORDS that match search term"""
    """ If _option is not None, then we are searching for a specific record number"""
    """ If _option is None, then we return the entire list of records"""
    items = []
    
    if _option is not None:
        for element in _list:
            if int(element.split(";")[0]) == search:
                items.append(builder(element, _list_type))
        return items 
    else:
        for element in _list:
            if search.lower() in element.lower() or search == "":
                items.append(builder(element, _list_type))
    return items


def append_to_file(line, filename):
    """ Takes a line and a filename, appends the line to the file """
    with open(filename, 'a') as f:
        f.write("\n" + line + "\n")

        
def string_to_list(data, sep = ';'):
    """ Takes a sep separated string and converts it to a list """ 
    return [ e.strip() for e in data.split(sep) ]

def dict_to_string(data, sep = ';'):
    """ Takes a dict and converts it to a sep separated string """ 
    return sep.join([str(e) for e in data.values()])

def create_new_record(job_or_poc, file_path):
    """ Collects user input based on either "job" or "poc" input, 
        and creates a new record in our data file
    """
     
    fields = JOB_FIELDS if job_or_poc == "job" else POC_FIELDS
    fields[0] = get_next_record_number(file_path)    
    input_data = get_user_data(fields)    
    new_item = dict_to_string(input_data)
    insert_new_item(new_item, file_path, job_or_poc)

def get_user_data(fields):
    # get the data from the user
    # loop through each field and get the data
    
    data = {'record_number': fields[0]}
    for field in fields[1:]:
        while True:
            if field == "first_contact" or field == "last_contact":
                data[field] = convert_date(dt.now())
                print(f"(press enter to accept {data[field]} as {field})")
                _input = input("or provide a date in YYYYMMDD format :")
                if _input != "":
                    data[field] = _input
                break
            data[field] = input("{}: ".format(field))
            if data[field] == "":
                data[field] = "Null"
                break
            elif ";" in data[field]:
                print("No semicolons allowed")
                continue
            else:
                break
    return data



def insert_new_item(line, file, job_or_poc):
    """ Inserts the new line into the given file """ 
    # print out the new records values
    # and the type of record we are creating
    #print(f"adding a new {job_or_poc},\n{line}")
    # Ask the user if they want to add the job or poc
    while True:
        print(f"New {job_or_poc} defined:")
        print(line)
        _answer = input(f"Do you want to add this {job_or_poc}? (y/n): ")
        if is_yes(_answer) and _answer != "":
            _answer = True
            break
        elif is_yes(_answer) == False and _answer != "":
            _answer = False
            break
        print("Please answer the question")
            
    if _answer == True:
        try:
            # Check if POC or Job
            if job_or_poc == "job":
                # Append the new job to the job file using the append_to_file function
                append_to_file(line, file)
            elif job_or_poc == "poc":
                # Append the new poc to the poc file using the append_to_file function
                append_to_file(line, file)
            # confirm the new record was added
            print(f"New {job_or_poc} added to database")
        except:
            print("Error writing to file")
    else:
        print("Input cancelled")
        
    return()


def get_next_record_number(file):
    """ Get the next record number for a job or POC """
    record_numbers = []
    with open(file, 'r') as f:
        for line in f:
            line = line.strip()
            if ';' in line:
                data = line.split(";")
                record_numbers.append(int(data[0].strip()))
    max_record_number = max(record_numbers, default=0)
    return max_record_number + 1



def update_record(job_or_poc, record_number):
    """ Update an existing job or POC record """
    updated_data = {}
    fields = JOB_FIELDS if job_or_poc == "job" else POC_FIELDS
    filepath = os.path.join(datadir, job_file) if job_or_poc == "job" else os.path.join(datadir, poc_file)

    records = list_from_file(filepath)

    for i, line in enumerate(records):
        if line.startswith(record_number):
            current_record = string_to_list(line)
            break
    else:
        print(f"No {job_or_poc} found with record number {record_number}")
        return

    print(f"Current {job_or_poc}:")
    print("; ".join(current_record))

    for idx, field in enumerate(fields):
        # skip the record number field
        if field == "record_number":
            updated_data[field] = current_record[idx]
            continue
        while True:
            print(f"(press enter to keep current {field}")
            user_input = input(f": {current_record[idx]} ->")
            if user_input == "":
                updated_data[field] = current_record[idx]
                break
            elif ";" in user_input:
                print("No semicolons allowed")
                continue
            else:
                updated_data[field] = user_input
                break

    updated_item = "; ".join([str(updated_data[field]) for field in fields])
    
    # Ask the user if they want to update the record
    while True:
        print(f"Updated {job_or_poc}:")
        print(updated_item)
        _answer = input("Update this Record? (y/n): ")
        if is_yes(_answer) and _answer != "":
            _answer = True
            break
        elif is_yes(_answer) == False and _answer != "":
            _answer = False
            break
        print("Please answer the question")
            
    if _answer == True:
        records[i] = updated_item
        with open(filepath, 'w') as f:
            f.write("\n".join(records))
        print(f"{job_or_poc.capitalize()} updated")
    else:
        print("Update cancelled")


def delete_record(record_number, file, job_or_poc):
    """ Delete an existing job or POC record """
    
    records = list_from_file(file)
    line_to_delete = None
    for i, line in enumerate(records):
        if line.startswith(str(record_number)):
            line_to_delete = i
            break
    
    if line_to_delete is None:
        print(f"No {job_or_poc} found with record number {record_number}")
        return

    deleted_record = records[line_to_delete]
    print(f"Deleting {job_or_poc}:")
    print(deleted_record)

    if is_yes(input(f"Delete this {job_or_poc}?")):
        del records[line_to_delete]
        with open(file, 'w') as f:
            f.write("\n".join(records))
        print(f"{job_or_poc.capitalize()} deleted")
    else:
        print("Deletion cancelled")


if __name__ == "__main__":

    datadir     = "data"
    job_file    = "jobs.txt"
    poc_file    = "pocs.txt"
    
    job_file_path = os.path.join(datadir, job_file)
    poc_file_path = os.path.join(datadir, poc_file)
    
    try:
        poc_list = list_from_file(os.path.join(datadir, poc_file))
        job_list = list_from_file(os.path.join(datadir, job_file))
    except:
        print("Can't find the data files")
        sys.exit(1)
    

    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--add", help="add data, requires -j or -p", action="store_true")
    parser.add_argument("-j", "--job", help="use the Job info", type=str, nargs='?', const=True, default=None)
    parser.add_argument("-p", "--poc", help="use the POC info", type=str, nargs='?', const=True, default=None)
    parser.add_argument("-s", "--search", help="SEARCH for", default="")
    parser.add_argument("-u", "--update", help="update data, requires -j or -p and record number", action="store_true")
    parser.add_argument("-r", "--record", help="record number for update", type=int, nargs='?', const=True, default=None)
    parser.add_argument("-d", "--delete", help="delete data, requires -j or -p and record number", action="store_true")

    

    args = parser.parse_args()

    if args.add:
        if args.poc:
            create_new_record("poc", poc_file_path)
        elif args.job:
            create_new_record("job", job_file_path)
        else:
            print("Please specify -j for Job or -p for POC when using the --add option.")
        sys.exit(1)
            
    if args.delete:
        if args.poc:
            delete_record(args.record, poc_file_path, 'poc')
        elif args.job:
            delete_record(args.record, job_file_path, 'job')
        else:
            print("Please specify -j for Job or -p for POC when using the --delete option.")
        sys.exit(1)

    if args.update:
        if args.poc:
            update_record("poc", args.record)
        elif args.job:
            update_record("job", args.record)
        else:
            print("Please specify -j for Job or -p for POC")
            print("and -r <RECORD NUMBER> when using the --update option.")
        sys.exit(1)
        
    if args.job is not None:
        if args.job == True:
            job_search = args.search
        else:
            job_search = args.job
        for job in parse_list(job_list, "job", job_search):
            print("Jobs\n", job, "\n")
        sys.exit(1)
    
    if args.poc is not None:
        if args.poc == True:
            poc_search = args.search
        else:
            poc_search = args.poc
        for poc in parse_list(poc_list, "poc", poc_search):
            print("Person of Concerns\n", poc, "\n")
        sys.exit(1)
        
    if args.search:
        found = 0
        for job in parse_list(job_list, "job", args.search):
            print("Job\n", job, "\n")
            found += 1
        for poc in parse_list(poc_list, "poc", args.search):
            print("Person of Concern\n", poc, "\n")
            found += 1
        if found == 0:
            print("No matches found")
        sys.exit(1)

    if args.record is not None:

        if type(args.record) == bool and args.record == True:
            print("arg was True")
            for poc in parse_list(poc_list, "poc", ""):
                print("poc - ", poc, "\n")
            for job in parse_list(job_list, "job", ""):
                print("job - ", job, "\n")
        else:
            for job in parse_list(job_list, "job", args.record, "record_number"):
                print("Job\n", job, "\n")
            for poc in parse_list(poc_list, "poc", args.record, "record_number"):
                print("Person of Concern\n", poc, "\n")

        sys.exit(1)

