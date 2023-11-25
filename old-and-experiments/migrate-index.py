# Fast migration script to MongoDB Atlas that splits magnets into 2 DBs.
# This script is meant to be run on new empty MongoDB Atlas instances for the first time DBs filling.
# It includes the text indexing approach using MongoDB's text search feature.
# This script creates text indexes on the magnet_link field for both collections before migrating the data.
# This will enable faster text search on the indexed field in MongoDB.

# Speed will be around 5K doc/s.

import pymongo
from dotenv import load_dotenv
from tqdm import tqdm
import os

load_dotenv()  # Load environment variables from .env file

# MongoDB Atlas connection details for the first account
connection_string_1 = os.getenv("MONGODB_CONNECTION_STRING_1")
db_name_1 = os.getenv("DB_NAME_1")
collection_name_1 = os.getenv("COLLECTION_NAME_1")

# MongoDB Atlas connection details for the second account
connection_string_2 = os.getenv("MONGODB_CONNECTION_STRING_2")
db_name_2 = os.getenv("DB_NAME_2")
collection_name_2 = os.getenv("COLLECTION_NAME_2")

# Connect to the first MongoDB Atlas account
client_1 = pymongo.MongoClient(connection_string_1)
db_1 = client_1[db_name_1]
collection_1 = db_1[collection_name_1]

# Connect to the second MongoDB Atlas account
client_2 = pymongo.MongoClient(connection_string_2)
db_2 = client_2[db_name_2]
collection_2 = db_2[collection_name_2]

# Create text indexes on the "magnet_link" field
collection_1.create_index([("magnet_link", "text")])
collection_2.create_index([("magnet_link", "text")])

# Open the "everything.txt" file and migrate data
batch_size = 10000  # Number of documents to insert in each batch
batch_1 = []
batch_2 = []
current_batch = 1  # Counter variable for the current batch
# Get the total number of documents
total_documents = sum(1 for _ in open("everything.txt"))

with tqdm(total=total_documents, unit="doc") as pbar:
    pbar.set_postfix(
        inserted=0,
        remaining=total_documents,
        total=total_documents,
        refresh=False,
    )

    with open("everything.txt", "r") as file:
        for line in file:
            magnet_link = line.strip()

            # Create a document and add it to the appropriate batch
            document = {"magnet_link": magnet_link}
            if current_batch == 1:
                batch_1.append(document)
                current_batch = 2
            else:
                batch_2.append(document)
                current_batch = 1

            # Insert the batches when they reach the specified size
            if len(batch_1) == batch_size:
                collection_1.insert_many(batch_1)
                batch_1 = []  # Reset the batch
            if len(batch_2) == batch_size:
                collection_2.insert_many(batch_2)
                batch_2 = []  # Reset the batch

            pbar.update(1)  # Update the progress bar
            pbar.set_postfix(
                inserted=pbar.n % batch_size,
                remaining=total_documents - pbar.n,
                total=total_documents,
                refresh=False,
            )

        # Insert the remaining documents in the last batches
        if batch_1:
            collection_1.insert_many(batch_1)
            pbar.update(len(batch_1))
            pbar.set_postfix(
                inserted=pbar.n % batch_size,
                remaining=total_documents - pbar.n,
                total=total_documents,
                refresh=False,
            )
        if batch_2:
            collection_2.insert_many(batch_2)
            pbar.update(len(batch_2))
            pbar.set_postfix(
                inserted=pbar.n % batch_size,
                remaining=total_documents - pbar.n,
                total=total_documents,
                refresh=False,
            )

# Close the MongoDB connections
client_1.close()
client_2.close()
