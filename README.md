# CS 340 README Template

## About the Project/Project Title

AnimalShelter -- a Python library for interacting with an Animal Shelter
MongoDB database

## Motivation

The goal of AnimalShelter is to make it simple to create, find, update,
and delete animal shelter records using Python.

## Getting Started

Using this library is easy.

1. Download the **aac_crud_driver.py** and edit it with your database
connection and authentication details, in the **__init__** method:

```python
USER = urllib.parse.quote_plus(username)
PASS = urllib.parse.quote_plus(password) 
HOST = 'mongosb.example.com' 
PORT = 27019
DB = 'AAC' # name of the database       
COL = 'animals' # name of the collection
```

## Installation

This library requires **Python 3** and the **pymongo** library, which is
used as the backend MongoDB driver.

## Usage

### Code Example

```python
from aac_crud_driver import AnimalShelter
# create the driver object
driver = AnimalShelter()

# add a new record into the database using regular Python dicts
driver.create( { "breed": "Wombat", "Name": "Spunky" } )

# get a list of matching records
matches = driver.find( { "breed": "Zebra" } )
```

## Functions

* *create(data)*: Takes a dictionary object representation
of the record to add. It returns True if the insertion succeeded and
False if it did not.

* *find(query)*: Takes a dictionary object of the to search
for. Returns a list of all matching records. Returns an empty list if
no matching records were found.


### Screenshots

![](media/image1.png){width="6.5in" height="3.245138888888889in"}

## Challenges

Getting the authentication to go through has been the most difficult to
get right so far. Credentials need to be url-escaped (which is now
handled in the driver code); this was not an easy requirement to figure
out.

## Roadmap/Features (Optional)

- [ ] Implement the **update** and **delete** functions

- [ ] Improve the way database connection/authentication details are
      stored (e.g. a YAML file)

- [ ] Perform validation on the dict data when creating a new record

## Contact

Andrew Wilson
