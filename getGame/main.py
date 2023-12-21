import os
import random
import requests
import uvicorn as uvicorn
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.trace.export import ConsoleSpanExporter
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource


provider = TracerProvider()
processor = BatchSpanProcessor(ConsoleSpanExporter())
provider.add_span_processor(processor)
trace.set_tracer_provider(
    TracerProvider(resource=Resource.create({SERVICE_NAME: "GameManager"}))
)
jaeger_exporter = JaegerExporter(
    agent_host_name=os.getenv("JAGER_HOSTNAME", "localhost"),
    agent_port=6831,
)
trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(jaeger_exporter))

tracer = trace.get_tracer("getgame")


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
    with tracer.start_as_current_span("getdatagame"):
        r_id = random.randint(1, 50)
        r = requests.get(f"https://mmo-games.p.rapidapi.com/game?id={r_id}&rapidapi-key=02e3aad88dmsh200fff7930d9119p1a6a70jsn14ce6533a67a")
        return r.json()

@app.get("/list/")
async def get_list(q: list | None = Query()):
    with tracer.start_as_current_span("getlistgame"):
        game_list = []
        for id in q:
            r = requests.get(f"https://mmo-games.p.rapidapi.com/game?id={id}&rapidapi-key=02e3aad88dmsh200fff7930d9119p1a6a70jsn14ce6533a67a")
            game_list.append(r.json())
        return game_list

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv('PORT', 80)))