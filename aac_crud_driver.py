from bson import is_valid
from pymongo import MongoClient
from bson.objectid import ObjectId  
import urllib.parse


class AnimalShelter(object):
    """ CRUD operations for Animal collection in MongoDB """

    def __init__(self):
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

        USER = urllib.parse.quote_plus('aacuser')
        PASS = urllib.parse.quote_plus("i3-bNzTV6OF#V-'a00e+=iKh&JQs")
        HOST = 'nv-desktop-services.apporto.com'
        PORT = 32471
        DB = 'AAC'   # TODO: change this to 'AAC' for production
        COL = 'animals'
        # 
        # Initialize Connection
        #
        self.client = MongoClient('mongodb://%s:%s@%s:%s/' % (USER,PASS,HOST,PORT))
        self.database = self.client['%s' % (DB)]
        self.collection = self.database['%s' % (COL)]

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

        matching_documents = []

        try:
            matching_documents = self.find(query)
        finally:
            []

        if len(matching_documents) == 0:
            return 0

        update_result = self.collection.update_many(query, newdata)

        return update_result.modified_count
    
        

    @staticmethod
    def is_valid_dict(data):
        """Returns true if the argument is a valid dict that can be used in MongoDB queries"""
        is_not_nothing = not (data is None)
        is_a_dict      = isinstance(data, dict)

        return (is_not_nothing and is_a_dict)


