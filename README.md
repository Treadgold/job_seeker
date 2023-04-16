[![<LeamHall>](https://circleci.com/gh/LeamHall/job_seeker.svg?style=shield)](https://app.circleci.com/pipelines/github/LeamHall/job_seeker?branch=master&filter=all)

# job_seeker

Tracks job applications and contacts


## Logic

- Given -j, print out all Jobs
- Given -p, prints out all Points of Contact
- Given -a, and -j or -p, and data, adds to the end of the file, you will be prompted to input details.
- Given -s <string>, searches and prints any job or poc that matches <string>
- Given -u and (-j or -p) and -r <record number> allows you to update a record
- Given -d and (-r or -p) and -r <record number> allows you to delete a record

## Examples

### List of Points of Contact

```
.\job_seeker.py -p
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
.\job_seeker.py -p -s shannon
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
.\job_seeker.py -j -s linux
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

### Update record 8

```
.\job_seeker.py -p -u -r 8
Current poc:
8; Jason Manford; JuggleBuddies Annonymous; 55/884/479'; juncle.right@r.com; 20230321; 20230321
(press enter to keep current name
: Jason Manford ->Jason Minstrel
(press enter to keep current company
: JuggleBuddies Annonymous ->International Pancake House
(press enter to keep current phone
: 55/884/479' ->555-886-9889
(press enter to keep current email
: juncle.right@r.com ->Jason.Minstrel@HOP.com
(press enter to keep current first_contact
: 20230321 ->
(press enter to keep current last_contact
: 20230321 ->20230416
Updated poc:
8; Jason Minstrel; International Pancake House; 555-886-9889; Jason.Minstrel@HOP.com; 20230321; 20230416
Update this Record? (y/n): y
Poc updated
```

 
