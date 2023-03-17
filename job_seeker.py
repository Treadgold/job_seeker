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
    "first_contact",
]

POC_FIELDS = [
    "record_number",
    "name",
    "company",
    "phone",
    "email",
    "first_contact",
    "last_contact",
]


class Job:
    """Stores the job req data"""

    def __init__(self, job_data=None):
        
        if job_data is None:
            job_data = {}
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

    def __init__(self, data=None):
        if data is None:
            data = {}
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
 
    if prompt.lower() in yes_choices:
        return True
    else:
        return False
    

def convert_date(date):
    """ Takes a datetime.datetime object and returns a YYYMMDD string """
    return "{}{:0>2}{:0>2}".format(date.year, date.month, date.day)

def job_builder(line):
    _list = string_to_list(line)
    data = {field: _list[idx] for idx, field in enumerate(JOB_FIELDS)}
    return Job(data)


def poc_builder(line):
    _list = string_to_list(line)
    data = {field: _list[idx] for idx, field in enumerate(POC_FIELDS)}
    return POC(data)


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

def append_to_file(line, filename):
    """ Takes a line and a filename, appends the line to the file """
    with open(filename, 'a') as f:
        f.write("\n" + line + "\n")
        
def string_to_list(data, sep = ';'):
    """ Takes a sep separated string and converts it to a list """ 
    return [ e.strip() for e in data.split(sep) ]

def create_new_record(job_or_poc: str):
    """ Collects user input based on either "job" or "poc" input, 
        and creates a new record in our data file
    """
    data = {}
    fields = JOB_FIELDS if job_or_poc == "job" else POC_FIELDS
    record_number = get_next_record_number(job_or_poc)

    # get the data from the user
    # loop through each field and get the data
    for field in fields:
        if field == "record_number":
            data[field] = record_number
        else:
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

    new_item = "; ".join([str(data[field]) for field in fields])
        
    # print out the new records values
    # and the type of record we are creating
    print(f"adding a new {job_or_poc},\n{new_item}")
    
    # Ask the user if they want to add the job
    if is_yes(input(f"Add this new {job_or_poc}?")):
        try:
            # Check if POC or Job
            if job_or_poc == "job":
                # Append the new job to the job file using the append_to_file function
                append_to_file(new_item, os.path.join(datadir, job_file))
            elif job_or_poc == "poc":
                # Append the new poc to the poc file using the append_to_file function
                append_to_file(new_item, os.path.join(datadir, poc_file))
            # confirm the new record was added
            print(f"New {job_or_poc} added to database")
        except:
            print("Error writing to file")
    else:
        print("Input cancelled")
        
    return()

def get_next_record_number(job_or_poc: str) -> int:
    """ Get the next record number for a job or POC """

     # Check whether we are working with job or POC records
    if job_or_poc == "job":
        # Read lines from the job data file
        lines = list_from_file(os.path.join(datadir, job_file))
        # Initialize an empty list to store job records
        records = []
        # Iterate through each line from the job data file
        for line in lines:
            # Create a job record from the line and append it to the records list
            records.append(job_builder(line))
    elif job_or_poc == "poc":
        # Read lines from the POC data file
        lines = list_from_file(os.path.join(datadir, poc_file))
        # Initialize an empty list to store POC records
        records = []
        # Iterate through each line from the POC data file
        for line in lines:
            # Create a POC record from the line and append it to the records list
            records.append(poc_builder(line))

    # Initialize an empty list to store record numbers
    record_numbers = []

    # Iterate through each record in the records list
    for record in records:
        # Convert the record number to an integer and append it to the record_numbers list
        record_numbers.append(int(record.record_number))

    # Find the maximum record number in the record_numbers list, or use 0 if the list is empty
    max_record_number = max(record_numbers, default=0)

    return max_record_number + 1



def update_record(job_or_poc: str, record_number: str):
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
        while True:
            user_input = input(f"{field} (current: {current_record[idx]}): ")
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

    if is_yes(input(f"Update this {job_or_poc}?")):
        records[i] = updated_item
        with open(filepath, 'w') as f:
            f.write("\n".join(records))
        print(f"{job_or_poc.capitalize()} updated")
    else:
        print("Update cancelled")

def delete_record(job_or_poc: str, record_number: str):
    """ Delete an existing job or POC record """
    filepath = os.path.join(datadir, job_file) if job_or_poc == "job" else os.path.join(datadir, poc_file)
    
    records = list_from_file(filepath)

    for i, line in enumerate(records):
        if line.startswith(record_number):
            break
    else:
        print(f"No {job_or_poc} found with record number {record_number}")
        return

    deleted_record = records[i]
    print(f"Deleting {job_or_poc}:")
    print(deleted_record)

    if is_yes(input(f"Delete this {job_or_poc}?")):
        del records[i]
        with open(filepath, 'w') as f:
            f.write("\n".join(records))
        print(f"{job_or_poc.capitalize()} deleted")
    else:
        print("Deletion cancelled")

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
    parser.add_argument("-a", "--add", help="add data, requires -j or -p", action="store_true")
    parser.add_argument("-j", "--job", help="use the Job info", action="store_true")
    parser.add_argument("-p", "--poc", help="use the POC info", action="store_true")
    parser.add_argument("-s", "--search", help="SEARCH for", default="")
    parser.add_argument("-name", "--name", help="POC name", default="")
    parser.add_argument("-u", "--update", help="update data, requires -j or -p and record number", action="store_true")
    parser.add_argument("-r", "--record", help="record number for update", default="")
    parser.add_argument("-d", "--delete", help="delete data, requires -j or -p and record number", action="store_true")

    args = parser.parse_args()

    if args.add:
        if args.poc:
            create_new_record("poc")
        elif args.job:
            create_new_record("job")
            
    if args.delete:
        if args.poc:
            delete_record("poc", args.record)
        elif args.job:
            delete_record("job", args.record)
        else:
            print("Please specify -j for Job or -p for POC when using the --delete option.")


    if args.update:
        if args.poc:
            update_record("poc", args.record)
        elif args.job:
            update_record("job", args.record)

    if args.job and not args.add and not args.update:
        for job in parse_list(job_list, "job", args.search):
            print(job, "\n")
    
    if args.search:
        for job in parse_list(job_list, "job", args.search):
            print(job, "\n")

    if args.poc and not args.add and not args.update:
        for poc in parse_list(poc_list, "poc", args.search):
            print(poc, "\n")

    # allow name search in POC and Job
    if args.name:
        for poc in parse_list(poc_list, "poc", args.name):
            print("poc - ", poc, "\n")
        for job in parse_list(job_list, "job", args.name):
            print("job - ", job, "\n")

