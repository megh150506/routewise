# RouteWise

**Multi-City Travel Planner and Emergency Response System**
A Design and Analysis of Algorithms (DAA) project with a Python backend and a React frontend.

<img width="1917" height="828" alt="Screenshot 2026-11-17 212552" src="https://github.com/user-attachments/assets/b7bcae5a-7c34-4584-87fa-81663312ac34" />

<img width="1917" height="840" alt="Screenshot 2026-11-13 181956" src="https://github.com/user-attachments/assets/1d82572e-453f-4264-a985-6c6e4d2d4d52" />



RouteWise runs two modes on one shared graph and one routing engine:

- **Travel Mode:** plan the best order to visit several places in Pune and compare exact and approximate TSP algorithms.
- **Emergency Mode:** find the nearest hospital, shelter or supply point by road distance, close roads, and see the route recalculated.

All algorithms are written by hand in Python (no routing libraries). Each one records its steps, and the frontend replays them on a map so the working is visible.

## Features

- Interactive map of 15 Pune areas and 25 roads (Leaflet and OpenStreetMap)
- Five algorithms: Dijkstra, Nearest Neighbor, MST 2-Approximation, Brute Force, Held-Karp DP
- Step-by-step animation with play, pause, step, jump-to-result and a slider
- Comparison dashboard: distance, running time, operation count, and ratio versus the optimal tour
- Emergency facilities by category (hospitals, shelters, relief supplies, helplines) sorted by road distance
- Road-closure simulation and an optional flood-zone avoidance setting
- **Dijkstra Explained:** why a path was chosen, with every road checked on a small graph
- **Before and After Rerouting:** close a road and watch the alternative route being drawn
- **Complexity Lab:** measured operation counts for 3 to 12 stops, drawn on a log-scale chart

## Tech stack

| Part | Technology |
|---|---|
| Backend | Python 3.9+, FastAPI, Uvicorn |
| Algorithms | Pure Python |
| Frontend | React 18 (single HTML file, no build step), SVG charts |
| Map | Leaflet and OpenStreetMap tiles |
| Data | Python module (no database) |

## Project structure

```
routewise/
├── README.md
└── backend/
    ├── main.py            FastAPI app and API endpoints, serves the frontend
    ├── algorithms.py      Dijkstra, Nearest Neighbor, MST 2-approx, Brute Force, Held-Karp, explain, complexity
    ├── data.py            Areas, roads, road weights, facilities
    ├── requirements.txt
    └── static/
        └── index.html     React frontend (map, visualizer, dashboard, analysis views)
```

## Getting started

### Requirements
- Python 3.9 or newer
- Internet connection (map tiles and the React and Leaflet libraries load from CDNs)

### Run

```bash
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --reload
```

Open http://127.0.0.1:8000 in your browser. Interactive API docs are at http://127.0.0.1:8000/docs.

## How it works

1. The frontend loads the graph from `GET /api/graph`.
2. **Travel Mode:** the chosen stops go to `POST /api/tour`. The backend runs Dijkstra between every pair of stops to build a distance matrix, then runs the four tour algorithms on it.
3. **Emergency Mode:** `POST /api/nearest` runs Dijkstra from your location and lists facilities by road distance. `POST /api/route` runs Dijkstra to the chosen facility on the graph with closed roads removed.
4. Every algorithm returns its result together with a list of recorded steps. The frontend replays them on the map.

## Algorithms

| Algorithm | Paradigm | Time | Role |
|---|---|---|---|
| Dijkstra | Greedy | O(V²) | Shortest paths, emergency routing, distance matrix |
| Nearest Neighbor | Greedy | O(n²) | Fast tour, no guarantee |
| MST 2-Approximation | Greedy and approximation | O(n²) | Tour at most 2 × optimal (metric distances) |
| Brute Force | Exhaustive search | O(n!) | Exact tour, limited to 9 stops |
| Held-Karp | Dynamic programming | O(n²·2ⁿ) | Exact tour, limited to 13 stops |

Dijkstra distances between stops satisfy the triangle inequality, which makes the 2× guarantee of the MST approximation valid. Tours return to the start.

### Reading the comparison table
- **km:** total tour length, including the return to the start
- **ms:** running time of the tour algorithm (not including the distance matrix)
- **Ops:** operations counted inside the algorithm's loops
- **vs opt:** tour length divided by the exact Held-Karp answer

## API

| Endpoint | Purpose |
|---|---|
| `GET /api/graph` | Areas, roads, facilities and road weights |
| `POST /api/tour` | Run all tour algorithms for 3 to 15 stops |
| `POST /api/route` | Dijkstra route with closed roads and flood option |
| `POST /api/nearest` | Facilities of a category sorted by road distance |
| `POST /api/explain` | Step-by-step Dijkstra on a small sub-graph |
| `GET /api/complexity` | Measured operations and time for 3 to 12 stops |

<img width="1146" height="601" alt="image" src="https://github.com/user-attachments/assets/e4f738c8-98ab-4635-b7db-5d354d03d7d6" />


## Data notes and limitations

- Road weight is the straight-line (haversine) distance multiplied by 1.3, not measured road length.
- Facilities, the flood-affected zone and helpline numbers are sample data for demonstration.
- The network is small (15 areas) and has no live traffic.
- Dijkstra uses the O(V²) array version, which is easy to visualize but slower than a heap-based version on large graphs.

## Future scope

- Real road graph from OpenStreetMap
- Live traffic as dynamic edge weights
- Priority-queue Dijkstra, Branch and Bound, and 2-opt improvements
- More cities and real facility data

## Author

Built as a DAA course project.
