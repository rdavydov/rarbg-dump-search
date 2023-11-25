# fast migration script to MongoDB Atlas because of the batches
# good for new empty db filling
# speed will be around 1076.34 doc/s

import pymongo
from dotenv import load_dotenv
from tqdm import tqdm
import os

load_dotenv()  # Load environment variables from .env file

# MongoDB Atlas connection details
connection_string = os.getenv("MONGODB_CONNECTION_STRING")
db_name = os.getenv("DB_NAME")
collection_name = os.getenv("COLLECTION_NAME")

# Connect to MongoDB Atlas
client = pymongo.MongoClient(connection_string)
db = client[db_name]
collection = db[collection_name]

# Open the "everything.txt" file and migrate data
batch_size = 10000  # Number of documents to insert in each batch
batch = []
# Get the total number of documents
total_documents = sum(1 for _ in open("everything.txt"))

with tqdm(total=total_documents, ncols=80, unit="doc") as pbar:
    pbar.set_postfix(
        inserted=0,
        remaining=total_documents,
        total=total_documents,
        refresh=False,
    )

    with open("everything.txt", "r") as file:
        for line in file:
            magnet_link = line.strip()

            # Create a document and add it to the batch
            document = {"magnet_link": magnet_link}
            batch.append(document)

            # Insert the batch when it reaches the specified size
            if len(batch) == batch_size:
                collection.insert_many(batch)
                batch = []  # Reset the batch

            pbar.update(1)  # Update the progress bar
            pbar.set_postfix(
                inserted=pbar.n % batch_size,
                remaining=total_documents - pbar.n,
                total=total_documents,
                refresh=False,
            )

        # Insert the remaining documents in the last batch
        if batch:
            collection.insert_many(batch)
            pbar.update(len(batch))
            pbar.set_postfix(
                inserted=pbar.n % batch_size,
                remaining=0,
                total=total_documents,
                refresh=False,
            )

# Close the MongoDB connection
client.close()
