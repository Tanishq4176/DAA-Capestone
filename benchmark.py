"""Repeatable synthetic scalability benchmark; writes CSV, chart, and evidence images."""
from __future__ import annotations

import csv
import random
import statistics
import time
from pathlib import Path

import matplotlib.pyplot as plt

from app import ROOT, Parcel, format_dp_table, load_graph, load_parcels, run
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
    return [
        Parcel(
            f"S{i:04}",
            f"N{i}",
            rng.randint(1, 10),
            rng.randint(10, 100),
            rng.randint(1, 10),
            rng.choice(["High", "Medium", "Low"]),
        )
        for i in range(n)
    ]


def median_ms(fn):
    samples = []
    for _ in range(REPEATS):
        start = time.perf_counter()
        fn()
        samples.append((time.perf_counter() - start) * 1000)
    return statistics.median(samples)


def ring_graph(n):
    graph = {f"N{i}": {} for i in range(n)}
    for i in range(n):
        a, b = f"N{i}", f"N{(i + 1) % n}"
        graph[a][b] = 1
        graph[b][a] = 1
    for i in range(n):
        a, b = f"N{i}", f"N{(i + 7) % n}"
        if a != b:
            graph[a][b] = 3
            graph[b][a] = 3
    return graph


def save_text_image(text: str, path: Path, title: str) -> None:
    lines = text.splitlines()
    fig, ax = plt.subplots(figsize=(13, max(8, 0.18 * len(lines) + 1.4)))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, len(lines) + 2)
    ax.set_axis_off()
    ax.set_title(title, loc="left", fontsize=12, pad=12)
    for index, line in enumerate(lines):
        ax.text(0.01, len(lines) - index, line, fontfamily="monospace", fontsize=7.2, va="top")
    fig.savefig(path, dpi=160, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def save_graph_image(path: Path) -> None:
    graph = load_graph(ROOT / "datasets/routes.csv")
    nodes = sorted(graph)
    angles = {node: i * 2 * 3.1415926535 / len(nodes) for i, node in enumerate(nodes)}
    xs = {node: 1.15 * __import__("math").cos(angles[node]) for node in nodes}
    ys = {node: 1.15 * __import__("math").sin(angles[node]) for node in nodes}
    drawn = set()
    fig, ax = plt.subplots(figsize=(8, 8))
    for src, edges in graph.items():
        for dst, dist in edges.items():
            key = tuple(sorted((src, dst)))
            if key in drawn:
                continue
            drawn.add(key)
            ax.plot([xs[src], xs[dst]], [ys[src], ys[dst]], color="#8aa0b4", linewidth=1)
            ax.text((xs[src] + xs[dst]) / 2, (ys[src] + ys[dst]) / 2, str(dist), fontsize=7, color="#334")
    for node in nodes:
        ax.scatter(xs[node], ys[node], s=520, color="#1f6feb" if node == "Warehouse" else "#d0e2ff", zorder=3)
        label = "WH" if node == "Warehouse" else node
        ax.text(xs[node], ys[node], label, ha="center", va="center", fontsize=7, color="white" if node == "Warehouse" else "#102", zorder=4)
    ax.set_axis_off()
    ax.set_title("Sample undirected road graph (edge labels = km)")
    fig.savefig(path, dpi=160, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def main():
    rows = []
    for n in SIZES:
        parcels = synthetic(n)
        graph = ring_graph(n)
        destinations = [f"N{i}" for i in range(min(n, 30))]
        cap = min(100, max(12, n // 2))
        rows.append(
            {
                "parcels_nodes": n,
                "capacity_kg": cap,
                "sorting_median_ms": median_ms(lambda: sort_parcels_by_priority_and_deadline(parcels)),
                "knapsack_median_ms": median_ms(lambda: knapsack_select_parcels(parcels, cap)),
                "dijkstra_median_ms": median_ms(lambda: dijkstra(graph, "N0")),
                "route_median_ms": median_ms(lambda: plan_nearest_neighbor_route(graph, "N0", destinations)),
            }
        )
    csvpath = OUT / "runtime_benchmarks.csv"
    with csvpath.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    fig, axes = plt.subplots(2, 2, figsize=(10, 7), constrained_layout=True)
    series = [
        ("sorting_median_ms", "Parcel sorting (Timsort)"),
        ("knapsack_median_ms", "0/1 knapsack (capacity scales)"),
        ("dijkstra_median_ms", "Dijkstra (nodes/edges scale)"),
        ("route_median_ms", "Nearest-neighbor route (up to 30 stops)"),
    ]
    for ax, (key, title) in zip(axes.flat, series):
        ax.plot([r["parcels_nodes"] for r in rows], [r[key] for r in rows], marker="o")
        ax.set_title(title)
        ax.set_xlabel("Input size (parcels / graph nodes)")
        ax.set_ylabel("Median runtime (ms)")
        ax.grid(True, alpha=0.3)
    fig.suptitle(f"Mini Courier Planner runtime benchmark ({REPEATS} runs; median)")
    fig.savefig(OUT / "runtime_benchmarks.png", dpi=180)
    plt.close(fig)

    demo = run()
    (ROOT / "sample_output.txt").write_text(demo, encoding="utf-8")
    save_text_image(demo, OUT / "console_demo.png", "Phase 5 demonstration — py app.py")
    large = run(25, ROOT / "datasets/parcels_large.csv", ROOT / "datasets/routes_large.csv")
    (ROOT / "sample_output_large.txt").write_text(large, encoding="utf-8")
    save_text_image(large, OUT / "console_demo_large.png", "Phase 4 larger dataset — py app.py --capacity 25 --parcels datasets/parcels_large.csv")
    save_graph_image(OUT / "road_graph.png")
    sample_parcels = sort_parcels_by_priority_and_deadline(load_parcels(ROOT / "datasets/parcels.csv"))
    _, _, dp = knapsack_select_parcels(sample_parcels, 12)
    save_text_image("\n".join(format_dp_table(sample_parcels, dp)), OUT / "dp_table.png", "Phase 2 DP table evidence (capacity 12 kg)")

    print(f"Wrote {csvpath.relative_to(ROOT)}, images/runtime_benchmarks.png, sample_output.txt")
    print("Sizes:", ", ".join(map(str, SIZES)), "| repeats:", REPEATS)
    for row in rows:
        print(row)


if __name__ == "__main__":
    main()
