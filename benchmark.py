"""Repeatable synthetic scalability benchmark; writes CSV, chart, and run trace."""
from __future__ import annotations
import csv, random, statistics, time
from pathlib import Path
import matplotlib.pyplot as plt
from app import Parcel, load_graph, load_parcels, ROOT
from src.dijkstra import dijkstra
from src.knapsack import knapsack_select_parcels
from src.sorting import sort_parcels_by_priority_and_deadline
from src.tsp import plan_nearest_neighbor_route

OUT = ROOT / "images"
OUT.mkdir(exist_ok=True)
REPEATS = 5
SIZES = [10, 50, 100, 200]

def synthetic(n: int):
    rng = random.Random(2026 + n)
    return [Parcel(f"S{i:04}", f"N{i}", rng.randint(1, 10), rng.randint(10, 100), rng.randint(1, 10), rng.choice(["High", "Medium", "Low"])) for i in range(n)]

def median_ms(fn):
    samples=[]
    for _ in range(REPEATS):
        start=time.perf_counter(); fn(); samples.append((time.perf_counter()-start)*1000)
    return statistics.median(samples)

def ring_graph(n):
    graph={f"N{i}":{} for i in range(n)}
    for i in range(n):
        a,b=f"N{i}",f"N{(i+1)%n}"
        graph[a][b]=1; graph[b][a]=1
    # Add deterministic chords to make this a modest connected road network.
    for i in range(n):
        a,b=f"N{i}",f"N{(i+7)%n}"
        if a != b: graph[a][b]=3; graph[b][a]=3
    return graph

def main():
    rows=[]
    for n in SIZES:
        parcels=synthetic(n); graph=ring_graph(n); destinations=[f"N{i}" for i in range(min(n, 30))]
        cap=min(100, max(12,n//2))
        rows.append({"parcels_nodes":n,"capacity_kg":cap,
          "sorting_median_ms":median_ms(lambda: sort_parcels_by_priority_and_deadline(parcels)),
          "knapsack_median_ms":median_ms(lambda: knapsack_select_parcels(parcels,cap)),
          "dijkstra_median_ms":median_ms(lambda: dijkstra(graph,"N0")),
          "route_median_ms":median_ms(lambda: plan_nearest_neighbor_route(graph,"N0",destinations))})
    csvpath=OUT/"runtime_benchmarks.csv"
    with csvpath.open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
    fig,axes=plt.subplots(2,2,figsize=(10,7),constrained_layout=True)
    for ax,key,title in zip(axes.flat,["sorting_median_ms","knapsack_median_ms","dijkstra_median_ms","route_median_ms"],["Parcel sorting","0/1 knapsack (capacity scales)","Dijkstra (nodes/edges scale)","Nearest-neighbor route (up to 30 stops)"]):
        ax.plot([r["parcels_nodes"] for r in rows],[r[key] for r in rows],marker="o")
        ax.set_title(title); ax.set_xlabel("Input size (parcels / graph nodes)"); ax.set_ylabel("Median runtime (ms)"); ax.grid(True,alpha=.3)
    fig.suptitle(f"Mini Courier Planner runtime benchmark ({REPEATS} runs; median)")
    fig.savefig(OUT/"runtime_benchmarks.png",dpi=180); plt.close(fig)
    demo=ROOT/"sample_output.txt"
    from app import run
    demo.write_text(run(),encoding="utf-8")
    print(f"Wrote {csvpath.relative_to(ROOT)}, images/runtime_benchmarks.png, sample_output.txt")
    print("Sizes:", ", ".join(map(str,SIZES)), "| repeats:",REPEATS)
    for r in rows: print(r)
if __name__=="__main__": main()
