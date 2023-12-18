import os
import random
import requests
import uvicorn as uvicorn
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    r_id = random.randint(1, 50)
    r = requests.get(f"https://mmo-games.p.rapidapi.com/game?id={r_id}&rapidapi-key=02e3aad88dmsh200fff7930d9119p1a6a70jsn14ce6533a67a")
    return r.json()

@app.get("/list/")
async def get_list(q: list | None = Query()):
    film_list = []
    for id in q:
        r = requests.get(f"https://mmo-games.p.rapidapi.com/game?id={id}&rapidapi-key=02e3aad88dmsh200fff7930d9119p1a6a70jsn14ce6533a67a")
        film_list.append(r.json())
    return film_list

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv('PORT', 80)))