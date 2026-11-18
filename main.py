from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
import algorithms as alg
from data import PLACES, EDGES, FACILITIES, WEIGHTS

app = FastAPI(title="RouteWise API")
HERE = Path(__file__).parent

class TourReq(BaseModel): stops: list[int]
class RouteReq(BaseModel):
    src: int; dst: int; blocked: list[list[int]] = []; flood: bool = False
class NearReq(BaseModel):
    src: int; cat: str; blocked: list[list[int]] = []; flood: bool = False

@app.get("/api/graph")
def graph(): return {"places": PLACES, "edges": EDGES, "facilities": FACILITIES, "weights": WEIGHTS}

@app.post("/api/tour")
def tour(r: TourReq):
    if not 3 <= len(r.stops) <= 15 or len(set(r.stops)) != len(r.stops) or any(not 0 <= s < len(PLACES) for s in r.stops):
        raise HTTPException(400, "Send 3 to 15 distinct valid stop ids")
    return alg.solve_tour(r.stops)

@app.post("/api/route")
def route(r: RouteReq): return alg.route(r.src, r.dst, r.blocked, r.flood)

@app.post("/api/nearest")
def nearest(r: NearReq): return alg.nearest(r.src, r.cat, r.blocked, r.flood)

@app.get("/")
def index(): return FileResponse(HERE / "static" / "index.html")

class ExplainReq(BaseModel):
    nodes: list[int]; src: int; dst: int; blocked: list[list[int]] = []

@app.post("/api/explain")
def explain(r: ExplainReq):
    if r.src not in r.nodes or r.dst not in r.nodes or any(not 0 <= n < len(PLACES) for n in r.nodes):
        raise HTTPException(400, "src and dst must be in nodes")
    return alg.explain(r.src, r.dst, r.nodes, r.blocked)

@app.get("/api/complexity")
def complexity(): return alg.complexity()
