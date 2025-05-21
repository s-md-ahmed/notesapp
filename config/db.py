from pymongo import MongoClient
import urllib.parse
username = urllib.parse.quote_plus("s-md-ahmed")
password = urllib.parse.quote_plus("RFAgIaxoF5I12VTX")
uri = f"mongodb+srv://{username}:{password}@cluster0.izqpyt7.mongodb.net/"
conn = MongoClient(uri)
