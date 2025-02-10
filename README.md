# CS 340 README Template

## About the Project/Project Title

AnimalShelter -- a Python library for interacting with an Animal Shelter
MongoDB database

## Motivation

The goal of AnimalShelter is to make it simple to create, find, update,
and delete animal shelter records using Python.

## Getting Started

Using this library is easy.

1. Download the `aac_crud_driver.py`.

2. Import the module and create an `AnimalShelter` object with server 
   config details:

    ```python
    from aac_crud_driver import AnimalShelter

    shelter = AnimalShelter( { "username": "aacuser", "password": "123456" } )

    lucy = shelter.find( { "name": "Lucy", "breed": "Dog" } )
    ```

## Installation

This library requires **Python 3** and the **pymongo** library, which is
used as the backend MongoDB driver.

1. **Install Python 3.x**
   * Download and install it from [https://www.python.com/](the Python official website)

2. **Install MongoDB**
   * Follow MongoDB's [https://www.mongodb.com/docs/manual/installation/](official guide)

3. **Install `pymongo`**
   * `pip install pymongo` or `apt install python3-pymongo` (or the package manager 
     of your choice)

4. **Clone the repo**
   * `git clone https://github.com/aldonadi/TODO-UPLOAD-REPO`

## Usage

### Server Connection and Authentication

The main Python file `aac_crud_driver.py` contains some (hopefully) reasonable default
values for MongoDB server hostname, port, username, etc. It assumes a locally-hosted 
MongoDB at the default port. To configure this, along with credentials, you have two 
options: you can specify them in a dict you pass to the constructor, or put them in a
`db.yml` file that is in the same directory as `aac_crud_driver.py`. 

#### Specifying in the constructor

```python
shelter = AnimalShelter( 
    { 
        "hostname": "db.example.com", 
        "port":     12345,
        "username": "user1",
        "password": "very-insecure1",
        "db_name":  "main-street-shelter",
        "collection_name": "animal_records"
    }
```

#### Specifying in `db.yml`

In `db.yml`:
```yml
hostname: "db.example.com" 
port:     1234
username: "user1"
password: "very-insecure1"
db_name:  "main-street-shelter"
collection_name: "animal_records"
```

In your Python script:
```python
shelter = AnimalShelter()
```

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
for. Returns a list of all matching records. If no records are found,
returns an empty list.

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
