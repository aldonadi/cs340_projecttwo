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

  **Example:**
  ```python
  if shelter.create( { "breed": "Wombat", "name": "Huggles", "age": 5 } ):
    print("A new wombat has joined our shelter")
  ```

* *find(query [, include_id=False])*: Takes a dictionary object representing
  search criteria. Returns a list of all matching records. If no records are found,
  returns an empty list. By default, the Mongo ObjectId of matching records is not
  included. Set `include_id` to `True` to include ObjectId in returned results.

  **Example:**
  ```python
  shelter.find(
    query = { "breed": "Wombat", "name": "Huggles", "age": 5 },
    include_id = True)
  ```

* *update(query, newdata)*: Updated all documents that match the `query`
  dictionary with the fields and values in the `newdata` dict. Returns
  a dict in the form
  
      { 
        "success": bool,          # True if at least 1 document was modified
        "modified_count": int     # Number of documents that were modified
      }

  Raises an exception if either `query` or `newdata` are not dicts.

  **Example:**
  ```python
  birthday_boy = { "breed": "Wombat", "name": "Huggles", "age": 5 }
  new_age = { "age": 6" }

  if shelter.update(birthday_boy, new_age)['success']:
      print("Happy birthday!")
  ```

* *delete(query)*: Deletes all documents that match the `query`
  dictionary. Returns a dict in the form: 

      { 
        "success": bool,          # True if at least 1 document was deleted 
        "deleted_count": int      # Number of documents that were deleted
      }

  Raises an exception if `query` is not a dict.

  **Example:**
  ```python
  adopted_wombat = { "breed": "Wombat", "name": "Huggles", "age": 6 }

  if shelter.delete(adopted_wombat)['success']:
      print("Another happy family!")
  ```
### Testing

To test the functionality, use the following:

```python
# Test inserting a valid record
assert driver.create({"breed": "Dog", "name": "Buddy"}) == True

# Test inserting an invalid record (should return False)
assert driver.create(None) == False

# Test reading a record that exists
assert len(driver.find({"breed": "Dog"})) > 0

# Test reading a record that doesn't exist (should return empty list)
assert driver.find({"breed": "Dragon"}) == []

# Test updating a record
assert driver.update( { "breed": "Dog", "name": "Buddy"},    # query dict
                      { "name": "Bud" }                      # dict with into to update
                    )['success']   # will be True if at least 1 document was updated

# Test deleting a record
assert len(driver.find( { "objectId": "67a56b32ec2435f6e169c472" })) == 1     # verify it exists
assert driver.delete(   { "objectId": "67a56b32ec2435f6e169c472" })['success']  # delete it
assert len(driver.find( { "objectId": "67a56b32ec2435f6e169c472" })) == 0     # verify it is gone
```

### Screenshots

**MongoDB Import Execution**:
![](media/image1.png){width="6.5in" height="3.245138888888889in"}

**User Authentication Execution**:
![](media/image1.png){width="6.5in" height="3.245138888888889in"}

**CRUD Functionality Test Execution**:
![](media/image1.png){width="6.5in" height="3.245138888888889in"}

## Challenges

Getting the authentication to go through has been the most difficult to
get right so far. Credentials need to be url-escaped (which is now
handled in the driver code); this was not an easy requirement to figure
out.

Refactoring the database connection and authentication config away from
the source code and into a YAML file took a bit of work, especially
getting a nice order-of-precedence.

## Roadmap/Features (Optional)

- [X] Implement the **update** and **delete** functions

- [X] Improve the way database connection/authentication details are
      stored (e.g. a YAML file)

- [ ] Perform validation on the dict data when creating a new record

- [X] Update API for better return values from update and delete

- [X] Hide ObjectID from found documents by default

## Contact

Andrew Wilson
