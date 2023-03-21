[![<LeamHall>](https://circleci.com/gh/LeamHall/job_seeker.svg?style=shield)](https://app.circleci.com/pipelines/github/LeamHall/job_seeker?branch=master&filter=all)

# job_seeker

Tracks job applications and contacts


## Logic

- Given -j, print out all jobs
- Given -p, prints out all Points of Contact
- Given -a, and -j or -p, and data, adds to the end of the file
- Given -s `string`, searches and prints any job or poc that matches `string`
- Given -u and -j or -p and -r <record number> allows you to update a record
- Given -d and -r or -p and -r <record number> allows you to delete a record

- - An empty `string` prints all jobs or pocs
- - Not really going to use wildcards or regexs yet
    
## Examples

### List of Points of Contact

```
./job_seeker.py -p
record_number: 1
name: Frank Green Zappa
company: United Music Federation
phone: 0225 666 444
email: zappa@UMF.com
first_contact: 2023
last_contact: 2023

record_number: 2
name: Killian
company: Run Fast
phone: 8666544646
email: kill@run.com
first_contact: 2023
last_contact: 2023

```

### Find a specific contact's info

```
./job_seeker.py -p -s shannon
record_number: 3
name: Shannon Docherty
company: JustInTime
phone: 545488844
email: shannon@JIT.com
first_contact: 2023
last_contact: 2023
```

### Find jobs that mention linux

```
./job_seeker.py -j -s linux
record_number: 4
title: Linux Server Admin
active: Yes
notes: Arch, Redhat, NGIX, docker
company: Company number 7
url: comp7.com
poc_name: Martin Freeman
last_contact: 20230314
first_contact: 20230112
```



 
