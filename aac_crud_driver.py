from bson import is_valid
from pymongo import MongoClient
from bson.objectid import ObjectId  
import urllib.parse

DEFAULT_HOSTNAME   = 'nv-desktop-services.apporto.com'
DEFAULT_PORT       = 32471
DEFAULT_DB_NAME         = 'AAC'
DEFAULT_COLLECTION_NAME = 'animals'

#TODO: DELETE THESE CREDS!!!
# aacuser i3-bNzTV6OF#V-'a00e+=iKh&JQs

class AnimalShelter(object):
    """ CRUD operations for Animal collection in MongoDB """

    def __init__(
            self, 
            username, password, 
            host=DEFAULT_HOSTNAME, port=DEFAULT_PORT, 
            db_name=DEFAULT_DB_NAME, collection_name=DEFAULT_COLLECTION_NAME):
        # Initializing the MongoClient. This helps to 
        # access the MongoDB databases and collections.
        # This is hard-wired to use the aac database, the 
        # animals collection, and the aac user.
        # Definitions of the connection string variables are
        # unique to the individual Apporto environment.
        #
        # You must edit the connection variables below to reflect
        # your own instance of MongoDB!
        #
        # Connection Variables
        #

        # Per MongoDB doc, credentials need to be URL-escaped
        escaped_username = urllib.parse.quote_plus(username)
        escaped_password = urllib.parse.quote_plus(password)

        # Initialize Connection
        self.client = MongoClient('mongodb://%s:%s@%s:%s/' % (escaped_username, escaped_password,
                                                              host, port)
                                 )

        self.database = self.client['%s' % (db_name)]
        self.collection = self.database['%s' % (collection_name)]

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
        
   

    @staticmethod
    def is_valid_dict(data):
        """Returns true if the argument is a valid dict that can be used in MongoDB queries"""
        is_not_nothing = not (data is None)
        is_a_dict      = isinstance(data, dict)

        return (is_not_nothing and is_a_dict)


