from pymongo import MongoClient
from config import mongo


def get_database():
    client = MongoClient(mongo['mongodb_url'])
    database = client[mongo['mongodb_db_name']]
    return database


def get_coordinates_collection():
    database = get_database()
    return database[mongo['mongodb_db_name_coordinates']]
