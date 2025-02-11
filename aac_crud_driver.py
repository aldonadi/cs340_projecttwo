from bson import is_valid
from pymongo import MongoClient
from bson.objectid import ObjectId  
import urllib.parse
import sys

import yaml

CONFIG_FILENAME = 'db.yml'

# some (hopefully) sane defaults

DEFAULT_HOSTNAME = 'localhost'
DEFAULT_PORT     = 27017
DEFAULT_USERNAME = 'root'
DEFAULT_PASSWORD = ''

DEFAULT_DB_NAME  = 'AAC'
DEFAULT_COLLECTION_NAME = 'animals'

class AnimalShelter(object):
    """ CRUD operations for Animal collection in MongoDB """

    def __init__(self, configs = {}):
        """
        Sets up configuration options and state for talking to the backend database.
        
        You can pass in values for server hostname, password, etc either in a 'db.yml'
        file or into this constructor; e.g. 

          s = AnimalShelter( { 'hostname': 'srv.example.com', 'username': 'user1' } )

        The precedence of config options, from highest to lowest, are:

           1. options passed into the constructor
           2. Options read from 'db.yml'
           3. Default value
        """

        # load default and file (db.yml) config settings
        self.load_configs()

        # overwrite any config settings given as argument
        self.config.update(configs)

        # Per MongoDB doc, credentials need to be URL-escaped
        escaped_username = urllib.parse.quote_plus(self.config['username'])
        escaped_password = urllib.parse.quote_plus(self.config['password'])

        # Initialize Connection
        self.client = MongoClient(
                'mongodb://%s:%s@%s:%s/' % (escaped_username, escaped_password,
                                            self.config['hostname'], self.config['port'])
            )

        self.database = self.client['%s' % (self.config['db_name'])]
        self.collection = self.database['%s' % (self.config['collection_name'])]

    def create(self, data):
        """
        Creates a new animal record.

        Args:
            data (dict): The animal record to be created, expected as a dictionary.

        Returns:
            bool: True if the insertion was successful and acknowledged by the database,
                  False otherwise.

        Raises:
            Exception: If the `data` parameter is None or empty
        """
        if AnimalShelter.is_valid_dict(data):
            result = self.database.animals.insert_one(data)  # data should be dictionary 
            return result.acknowledged
        else:
            raise Exception("Nothing to save, because data parameter is empty")

    def find(self, data):
        """
        Retrieves animal records based on an optional query filter.

        Args:
            query (dict): A dictionary specifying the query criteria to filter documents.

        Returns:
            list: A list of documents that match the query. If no documents are found, returns an empty list.

        Example:
            To find all documents where age is greater than 25:
                query = {"breed": "Bat", "age_upon_outcome_in_weeks" : {"$gt": 50}}
                results = self.find(query)
        """
        if AnimalShelter.is_valid_dict(data):
            results = []     # if the find fails, results will be an empty list
            try:
                results = list(self.database.animals.find(data)) # data should be a dict
            
            finally:
                return results

        else:
            raise Exception("Nothing to find, because data parameter is empty")
    

    def update(self, query, newdata):
        """
        Updates all existing animal documents that match a query filter.

        Args:
          query (dict):   A dictionary specifying the query criteria to filter documents.
          newdata (dict): A dictionary containing the new fields and values to save to
                            all matching documents.

        Returns:
            int: the number of documents that were modified

        Raises:
            Exception if the query or newdata args are not valid dicts

        Example:
            To change the name of a certain breed for all records:
                boring_name =  { "breed": "Bat" }
                awesome_name = { "breed": "Chiroptera" }
                num_modified = shelter.update(boring_name, awesome_name)
        """
        if not AnimalShelter.is_valid_dict(query):
            raise Exception("Nothing to update, because query parameter is invalid")

        if not AnimalShelter.is_valid_dict(newdata):
            raise Exception("Nothing to update, because newdata parameter is invalid")
        
        # package the new data into a '$set' operation 
        data_update_dict = { "$set": newdata }

        # execute the update operation on the database server
        update_result = self.collection.update_many(query, data_update_dict)

        # report how many documents were actually modified
        return update_result.modified_count
    
    def delete(self, query):
        """
        Deletes all matching animal records.

        Args:
            query (dict): A dictionary specifying which documents should be deleted.

        Returns:
            int: The number of records that were deleted.

        Raises:
            Exception: If the `data` parameter is None or empty
        """

        if not AnimalShelter.is_valid_dict(query):
            raise Exception("Nothing to save, because data parameter is empty")

        result = self.database.animals.delete_many(query)  # data should be dictionary 
        return result.acknowledged
        

    def load_configs(self):
        """ Loads config settings from either a yaml file or defaults. """

        # first, load all the default, built-in config values
        self.config = {
            "hostname": DEFAULT_HOSTNAME,
            "port":     DEFAULT_PORT,
            "username": DEFAULT_USERNAME,
            "password": DEFAULT_PASSWORD,
            "db_name":  DEFAULT_DB_NAME,
            "collection_name": DEFAULT_COLLECTION_NAME
        }

        configs_from_file = {}

        # try to read configs from a YAML config file
        try:
            with open(CONFIG_FILENAME) as config_file:
                configs_from_file = yaml.safe_load(config_file)
        except FileNotFoundError:
            print("Config file '{CONFIG_FILENAME}' not found; using built-in default settings.",
                  file=sys.stderr)

        # override defaults with any settings from the config file
        self.config.update(configs_from_file)
   

    @staticmethod
    def is_valid_dict(data):
        """Returns true if the argument is a valid dict that can be used in MongoDB queries"""
        is_not_nothing = not (data is None)
        is_a_dict      = isinstance(data, dict)

        return (is_not_nothing and is_a_dict)

