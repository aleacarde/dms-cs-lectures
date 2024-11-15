"""
Example of an I/O-bound operation in Python using
an asynchronous framework like FastAPI 
"""

from fastapi import FastAPI
import asyncio

app = FastAPI()

@app.get("/fetch-data")
async def fetch_data():
    # Simulating an I/O operation, such as a database query
    await asyncio.sleep(3)  # Simulating I/O wait
    return {"message": "Data fetched"}