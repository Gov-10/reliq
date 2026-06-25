from fastapi import FastAPI, HTTPException, Request, Depends, Response
from utils.graph import sdg
from sqlalchemy.orm import Session
from sqlalchemy import text
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from utils.receiver import server, LAST_TRACE_RECEIVED, TOTAL_TRACE_BATCHES
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (OTLPSpanExporter)
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry import trace 
import os, json, logging
from dotenv import load_dotenv
from redis import Redis
load_dotenv()
#redis_client=Redis(host=os.getenv("REDIS_HOST"), port=int(os.getenv("REDIS_PORT")), password=os.getenv("REDIS_PASSWORD"), decode_responses=True)
app=FastAPI()
resource = Resource.create({"service.name": "network-service"})
provider = TracerProvider(resource=resource)
trace.set_tracer_provider(provider)
otlp_exporter = OTLPSpanExporter( endpoint="jaeger.tracing.svc.cluster.local:4317",insecure=True,)
provider.add_span_processor(SimpleSpanProcessor(otlp_exporter))
FastAPIInstrumentor.instrument_app(app)
tracer = trace.get_tracer(__name__)
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger("network")

@app.get("/")
def chek():
    return {"status": "Running"}

@app.get("/receiver-status")
def receiver_status():
    return {"grpc_receiver": "running", "last_trace_received": LAST_TRACE_RECEIVED,"total_trace_batches": TOTAL_TRACE_BATCHES}

@app.on_event("startup")
def startup():
    server.start()

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.get("/test-trace")
def test_trace():
    with tracer.start_as_current_span("topology-test"):
        return {"status": "trace generated"}

@app.get("/graph")
def get_graph():
    return {"nodes": list(sdg.nodes()), "edges": [{"source": u, "target": v, **attrs} for u,v, attrs in sdg.edges(data=True)]}
