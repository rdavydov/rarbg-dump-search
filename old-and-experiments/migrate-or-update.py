# very slow because of the overhead of the MongoDB connection
# speed will be around 1.78 lines/s

import pymongo
from dotenv import load_dotenv
import os
from tqdm import tqdm

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
with open("everything.txt", "r") as file:
    batch_size = 10000  # Number of documents to process in each batch
    total_count = 0
    skipped_count = 0
    progress_bar = tqdm(total=sum(1 for _ in file), unit='lines')

    file.seek(0)  # Reset the file pointer to the beginning

    for line in file:
        magnet_link = line.strip()

        # Check if the magnet link already exists in the collection
        if collection.count_documents({"magnet_link": magnet_link}) > 0:
            skipped_count += 1
            progress_bar.update(1)
            continue

        # Create a document and insert into MongoDB
        document = {"magnet_link": magnet_link}
        collection.insert_one(document)

        total_count += 1
        progress_bar.update(1)
        if total_count % batch_size == 0:
            tqdm.write(
                f"Processed: {total_count} | Skipped: {skipped_count} | Remaining: {progress_bar.total - progress_bar.n}")

    progress_bar.close()

    print("Migration complete!")
    print(f"Total documents: {total_count}")
    print(f"Skipped documents (already existing): {skipped_count}")

# Close the MongoDB connection
client.close()
