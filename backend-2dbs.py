# run command: TZ='Europe/Moscow' uvicorn backend-2dbs:app --host 0.0.0.0 --port 31337 --log-config uvicorn_logging.conf

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import re

load_dotenv()  # Load environment variables from .env file

app = FastAPI()
client_1 = MongoClient(os.getenv("MONGODB_CONNECTION_STRING_1"))
db_1 = client_1[os.getenv("DB_NAME_1")]
collection_1 = db_1[os.getenv("COLLECTION_NAME_1")]

client_2 = MongoClient(os.getenv("MONGODB_CONNECTION_STRING_2"))
db_2 = client_2[os.getenv("DB_NAME_2")]
collection_2 = db_2[os.getenv("COLLECTION_NAME_2")]

app.add_middleware(
    CORSMiddleware,
    # allow_origins=["*"],
    allow_origins=[
        "http://a92836ve.beget.tech",
        "https://rarbg.coomer.party"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def search(q: str):
    keywords = q.split()
    regex_patterns = [re.escape(keyword) for keyword in keywords]

    regex_queries = [
        {"magnet_link": {"$regex": pattern, "$options": "i"}} for pattern in regex_patterns
    ]

    search_pipeline = [
        {"$match": {"$and": regex_queries}},
        {"$project": {"magnet_link": 1}}
    ]

    results_1 = collection_1.aggregate(search_pipeline)
    results_2 = collection_2.aggregate(search_pipeline)

    all_results = []
    for result in results_1:
        all_results.append(result["magnet_link"])
    for result in results_2:
        all_results.append(result["magnet_link"])

    return {"results": all_results}
