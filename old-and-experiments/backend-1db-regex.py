# run command: TZ='Europe/Moscow' uvicorn backend-2dbs:app --host 0.0.0.0 --port 31337 --log-config uvicorn_logging.conf

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import re

load_dotenv()  # Load environment variables from .env file

app = FastAPI()
client = MongoClient(os.getenv("MONGODB_CONNECTION_STRING"))
db = client[os.getenv("DB_NAME")]
collection = db[os.getenv("COLLECTION_NAME")]

app.add_middleware(CORSMiddleware,
                   allow_origins=["*"],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])


@app.get("/search")
async def search(query: str):
    keywords = query.split()
    regex_pattern = ".*".join(re.escape(keyword) for keyword in keywords)
    results = collection.find(
        {"magnet_link": {"$regex": regex_pattern, "$options": "i"}}
    )
    return {"results": [result["magnet_link"] for result in results]}
