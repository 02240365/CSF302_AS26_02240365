"""
Lab 7 - Q3: Shortest Paths and Minimum Spanning Trees

  dijkstra(graph, source)  -> shortest distances and paths, binary heap   O((V + E) log V)
  kruskal(V, edges)        -> MST, sort edges + union-find                 O(E log E)
  prim(V, adj)             -> MST, grow one tree with a binary heap        O(E log V)
  prim_array(V, adj)       -> extra: Prim with a plain array, no heap      O(V^2)
  bellman_ford(...)        -> correct shortest paths even with negative edges (for Task 5)

Run:  python q3_graphs.py      (about 1 minute)
"""

import heapq
import random
import time


# ---------------------------------------------------------------------
# Task 1: Dijkstra with a binary heap, graph read from a file
# ---------------------------------------------------------------------
def read_graph(filename):
    """First line: number of vertices and the source. Then 'from to weight' per line."""
    with open(filename) as f:
        lines = [l.split() for l in f if l.strip() and not l.startswith("#")]
    V, source = map(int, lines[0])
    graph = {v: [] for v in range(V)}
    for u, v, w in lines[1:]:
        graph[int(u)].append((int(v), float(w)))
    return graph, source


def dijkstra(graph, source):
    dist = {v: float("inf") for v in graph}
    prev = {v: None for v in graph}
    dist[source] = 0
    done = set()                                   # vertices whose distance is final
    heap = [(0, source)]
    while heap:
        d, u = heapq.heappop(heap)                 # closest vertex not yet finished
        if u in done:
            continue                               # old, longer copy in the heap
        done.add(u)
        for v, w in graph[u]:
            if v not in done and d + w < dist[v]:  # relax the edge u -> v
                dist[v], prev[v] = d + w, u
                heapq.heappush(heap, (dist[v], v))
    return dist, prev


def path_to(prev, v):
    path = []
    while v is not None:
        path.append(v)
        v = prev[v]
    return path[::-1]


def task1():
    graph, s = read_graph("data/graph.txt")
    print(f"Task 1: Dijkstra from vertex {s} on data/graph.txt ({len(graph)} vertices)")
    dist, prev = dijkstra(graph, s)
    print(f"  {'vertex':>6} | {'distance':>8} | path")
    print("  " + "-" * 36)
    for v in graph:
        if dist[v] == float("inf"):
            print(f"  {v:>6} | {'inf':>8} | unreachable")
        else:
            print(f"  {v:>6} | {dist[v]:>8g} | {' -> '.join(map(str, path_to(prev, v)))}")


# ---------------------------------------------------------------------
# Task 2: Kruskal (union-find) and Prim (heap)
# ---------------------------------------------------------------------
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]   # path halving
            x = self.parent[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False                                   # already connected: would make a cycle
        if self.rank[ra] < self.rank[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra                               # union by rank
        if self.rank[ra] == self.rank[rb]:
            self.rank[ra] += 1
        return True


def kruskal(V, edges):
    """edges = [(weight, u, v)]. Take the lightest edge that joins two different trees."""
    uf, total, used = UnionFind(V), 0, 0
    for w, u, v in sorted(edges):
        if uf.union(u, v):
            total += w
            used += 1
            if used == V - 1:
                break
    return total


def prim(V, adj):
    """adj[u] = [(weight, v)]. Grow one tree from vertex 0, always adding
    the lightest edge that leaves the tree."""
    in_tree = [False] * V
    heap, total, count = [(0, 0)], 0, 0
    while heap and count < V:
        w, u = heapq.heappop(heap)
        if in_tree[u]:
            continue
        in_tree[u] = True
        total += w
        count += 1
        for wv, v in adj[u]:
            if not in_tree[v]:
                heapq.heappush(heap, (wv, v))
    return total


def prim_array(V, adj):
    """Extra: Prim without a heap. Keep the cheapest known edge to each vertex in
    a plain list and scan it for the minimum each time: O(V^2), no matter how many
    edges there are, so it suits dense graphs where E is close to V^2."""
    INF = float("inf")
    best = [INF] * V
    in_tree = [False] * V
    best[0], total = 0, 0
    for _ in range(V):
        u = min((b, v) for v, b in enumerate(best) if not in_tree[v])[1]   # O(V) scan
        in_tree[u] = True
        total += best[u]
        for w, v in adj[u]:
            if not in_tree[v] and w < best[v]:
                best[v] = w
    return total


def random_connected_graph(V, E, rng):
    """A random spanning tree first (so the graph is connected), then extra random edges."""
    edges, seen = [], set()
    order = list(range(V))
    rng.shuffle(order)
    for i in range(1, V):
        u, v = order[i], order[rng.randrange(i)]
        seen.add((min(u, v), max(u, v)))
        edges.append((rng.randint(1, 1000), u, v))
    while len(edges) < E:
        u, v = rng.randrange(V), rng.randrange(V)
        if u != v and (min(u, v), max(u, v)) not in seen:
            seen.add((min(u, v), max(u, v)))
            edges.append((rng.randint(1, 1000), u, v))
    adj = [[] for _ in range(V)]
    for w, u, v in edges:
        adj[u].append((w, v))
        adj[v].append((w, u))
    return edges, adj


# ---------------------------------------------------------------------
# Task 3: both MST algorithms give the same total weight
# ---------------------------------------------------------------------
def task3():
    print("\nTask 3: Kruskal vs Prim on 200 random connected graphs (5 to 60 vertices)")
    rng = random.Random(3)
    for t in range(200):
        V = rng.randint(5, 60)
        E = rng.randint(V - 1, V * (V - 1) // 2)
        edges, adj = random_connected_graph(V, E, rng)
        k, p = kruskal(V, edges), prim(V, adj)
        assert k == p, f"mismatch on graph {t}"
        if t < 5:
            print(f"  graph {t + 1}: V = {V:>2}, E = {E:>4}, Kruskal = {k:>6}, Prim = {p:>6}")
    print("  ... all 200 graphs give the same total weight")


# ---------------------------------------------------------------------
# Task 4: timing for V = 1,000, sparse and dense
# ---------------------------------------------------------------------
def best_time(func, *args):
    best = None
    for _ in range(3):
        start = time.perf_counter()
        result = func(*args)
        t = time.perf_counter() - start
        best = t if best is None else min(best, t)
    return result, best


def task4():
    print("\nTask 4: Time for V = 1,000 (best of 3 runs, ms)")
    rng = random.Random(4)
    V, rows = 1000, []
    print(f"  {'graph':<8}{'E':>9} | {'Kruskal':>9} | {'Prim (heap)':>11} | {'Prim (array, extra)':>19} | same weight")
    print("  " + "-" * 76)
    for name, E in [("sparse", 3 * V), ("dense", V * V // 4)]:
        edges, adj = random_connected_graph(V, E, rng)
        k, tk = best_time(kruskal, V, edges)
        p, tp = best_time(prim, V, adj)
        a, ta = best_time(prim_array, V, adj)
        rows.append((name, E, tk, tp, ta))
        print(f"  {name:<8}{E:>9,} | {tk*1000:>9.1f} | {tp*1000:>11.1f} | {ta*1000:>19.1f} | {k == p == a}")
    return rows


# ---------------------------------------------------------------------
# Task 5: one negative edge makes Dijkstra wrong
# ---------------------------------------------------------------------
def bellman_ford(graph, source):
    dist = {v: float("inf") for v in graph}
    dist[source] = 0
    for _ in range(len(graph) - 1):               # relax every edge V - 1 times
        for u in graph:
            for v, w in graph[u]:
                if dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
    return dist


def task5():
    print("\nTask 5: One negative edge (C -> B = -3)")
    names = "ABCD"
    #        A -> B 2,  A -> C 4,  C -> B -3,  B -> D 2
    graph = {0: [(1, 2), (2, 4)], 1: [(3, 2)], 2: [(1, -3)], 3: []}
    print("  edges: A->B 2, A->C 4, C->B -3, B->D 2   (source A)")
    d, _ = dijkstra(graph, 0)
    b = bellman_ford(graph, 0)
    print(f"  {'vertex':>6} | {'Dijkstra':>8} | {'correct (Bellman-Ford)':>22}")
    print("  " + "-" * 44)
    for v in graph:
        mark = "   <- wrong" if d[v] != b[v] else ""
        print(f"  {names[v]:>6} | {d[v]:>8g} | {b[v]:>22g}{mark}")
    print("  Dijkstra finishes B at distance 2 before it sees the cheaper path A -> C -> B = 1,")
    print("  and never updates B (or D, which is reached through B) again.")


def plot(rows):
    import os
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    os.makedirs("screenshots", exist_ok=True)
    labels = [f"{r[0]}\n(E = {r[1]:,})" for r in rows]
    x = range(len(rows))
    plt.figure(figsize=(7.5, 4.2))
    groups = [(2, "Kruskal (sort + union-find)", -0.27), (3, "Prim (binary heap)", 0.0),
              (4, "Prim (array, O(V²), extra)", 0.27)]
    for k, label, off in groups:
        bars = plt.bar([i + off for i in x], [r[k] * 1000 for r in rows], width=0.27, label=label)
        for b in bars:
            plt.text(b.get_x() + b.get_width() / 2, b.get_height() * 1.1, f"{b.get_height():.1f}",
                     ha="center", fontsize=8)
    plt.yscale("log")
    plt.xticks(list(x), labels)
    plt.ylabel("time in ms (log scale)")
    plt.title("MST for V = 1,000: Kruskal vs Prim")
    plt.legend()
    plt.grid(True, axis="y", which="both", ls=":", alpha=0.6)
    plt.tight_layout()
    plt.savefig("screenshots/q3_graph.png", dpi=150)
    print("\nGraph saved to screenshots/q3_graph.png")


if __name__ == "__main__":
    task1()
    task3()
    rows = task4()
    task5()
    plot(rows)
