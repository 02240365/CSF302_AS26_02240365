"""
Lab 6 - Q4 (Optional): Optimal Binary Search Tree

Keys k1..k5 with search probabilities p, and dummy keys d0..d5 (failed
searches that fall between keys) with probabilities q.

  optimal_bst(p, q)  -> e[i][j] = expected cost of the best tree for k_i..k_j
                        root[i][j] = the key at its root                 O(n^3)

Run:  python q4_optimal_bst.py
"""

p = [0.15, 0.10, 0.05, 0.10, 0.20]           # p1..p5
q = [0.05, 0.10, 0.05, 0.05, 0.05, 0.10]     # q0..q5


def optimal_bst(p, q):
    """e[i][j] = min over root r of  e[i][r-1] + e[r+1][j] + w(i, j),
    where w(i, j) = p_i + ... + p_j + q_(i-1) + ... + q_j
    (every key in the subtree moves one level deeper, adding its probability once)."""
    n = len(p)
    p = [0] + p                                       # 1-based keys
    e = [[0.0] * (n + 1) for _ in range(n + 2)]
    w = [[0.0] * (n + 1) for _ in range(n + 2)]
    root = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(1, n + 2):                         # empty trees: only dummy key d_(i-1)
        e[i][i - 1] = w[i][i - 1] = q[i - 1]
    for length in range(1, n + 1):
        for i in range(1, n - length + 2):
            j = i + length - 1
            e[i][j] = float("inf")
            w[i][j] = w[i][j - 1] + p[j] + q[j]
            for r in range(i, j + 1):                 # try every key as the root
                cost = e[i][r - 1] + e[r + 1][j] + w[i][j]
                if cost < e[i][j] - 1e-12:
                    e[i][j], root[i][j] = cost, r
    return e[1][n], root


def print_tree(root, i, j, prefix="", label="root"):
    """Print the tree sideways: each line is one node, children are indented."""
    if i > j:                                         # no keys left: a dummy leaf
        print(f"{prefix}{label}: d{j}")
        return
    r = root[i][j]
    print(f"{prefix}{label}: k{r}")
    print_tree(root, i, r - 1, prefix + "    ", "left ")
    print_tree(root, r + 1, j, prefix + "    ", "right")


if __name__ == "__main__":
    print("Q4: Optimal binary search tree")
    print(f"  p (keys k1..k5)     = {p}")
    print(f"  q (dummies d0..d5)  = {q}")
    cost, root = optimal_bst(p, q)
    print(f"\n  Expected search cost = {cost:.2f}   (expected: 2.75, match: {abs(cost - 2.75) < 1e-9})")
    print("\n  Structure of the optimal tree:")
    print_tree(root, 1, len(p), "    ")
