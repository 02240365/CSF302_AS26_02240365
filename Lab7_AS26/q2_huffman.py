"""
Lab 7 - Q2: Huffman Coding

  build_tree(text)    -> Huffman tree from character frequencies (heapq priority queue)
  make_codes(tree)    -> code table: character -> bit string
  encode / decode     -> text <-> bit string

Run:  python q2_huffman.py
"""

import heapq
from collections import Counter

FILES = ["data/english.txt", "data/dna.txt", "data/log.txt"]


# ---------------------------------------------------------------------
# Task 1: build the Huffman tree with a priority queue
# A leaf is a character; an internal node is a (left, right) pair.
# ---------------------------------------------------------------------
def build_tree(text):
    freq = Counter(text)
    # heap items: (frequency, tie-breaker, node). The counter keeps
    # comparisons on numbers only, so nodes never need to be compared.
    heap = [(f, i, ch) for i, (ch, f) in enumerate(freq.items())]
    heapq.heapify(heap)
    count = len(heap)
    while len(heap) > 1:
        f1, _, a = heapq.heappop(heap)          # two least frequent nodes
        f2, _, b = heapq.heappop(heap)
        heapq.heappush(heap, (f1 + f2, count, (a, b)))   # merge them
        count += 1
    return heap[0][2], freq


# ---------------------------------------------------------------------
# Task 2: code table (left edge = 0, right edge = 1)
# ---------------------------------------------------------------------
def make_codes(node, prefix="", table=None):
    if table is None:
        table = {}
    if isinstance(node, str):                   # leaf
        table[node] = prefix or "0"             # a file with one symbol still needs 1 bit
    else:
        make_codes(node[0], prefix + "0", table)
        make_codes(node[1], prefix + "1", table)
    return table


# ---------------------------------------------------------------------
# Task 3: encode and decode
# ---------------------------------------------------------------------
def encode(text, codes):
    return "".join(codes[ch] for ch in text)


def decode(bits, tree):
    if isinstance(tree, str):                   # one-symbol file
        return tree * len(bits)
    out, node = [], tree
    for b in bits:
        node = node[0] if b == "0" else node[1]
        if isinstance(node, str):               # reached a leaf: one character done
            out.append(node)
            node = tree
    return "".join(out)


def show(ch):
    return {"\n": "\\n", " ": "space"}.get(ch, ch)


def print_code_table(freq, codes):
    rows = sorted(freq, key=lambda ch: (-freq[ch], ch))
    half = (len(rows) + 1) // 2
    print(f"  {'char':<6}{'freq':>5}  {'code':<13}   {'char':<6}{'freq':>5}  code")
    for i in range(half):
        line = ""
        for ch in [rows[i]] + ([rows[i + half]] if i + half < len(rows) else []):   # two columns
            line += f"  {show(ch):<6}{freq[ch]:>5}  {codes[ch]:<13} "
        print(line)


def plot(results):
    import os
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    os.makedirs("screenshots", exist_ok=True)
    names = [r[0] for r in results]
    plt.figure(figsize=(7, 3.8))
    bars = plt.bar(names, [r[4] * 100 for r in results])
    for b, r in zip(bars, results):
        plt.text(b.get_x() + b.get_width() / 2, b.get_height() + 1,
                 f"{r[4]:.1%}\n({r[5]:.2f} bits/char)", ha="center", fontsize=9)
    plt.axhline(100, color="black", ls="--", lw=1, label="8-bit fixed length (100%)")
    plt.ylim(0, 130)
    plt.ylabel("Huffman size as % of 8-bit size")
    plt.title("Huffman compression ratio for three text files")
    plt.legend(loc="upper left")
    plt.tight_layout()
    plt.savefig("screenshots/q2_graph.png", dpi=150)
    print("\nGraph saved to screenshots/q2_graph.png")


if __name__ == "__main__":
    results = []
    for i, name in enumerate(FILES):
        with open(name) as f:
            text = f.read()
        tree, freq = build_tree(text)
        codes = make_codes(tree)
        bits = encode(text, codes)
        ok = decode(bits, tree) == text

        if i == 0:
            print(f"Task 1 & 2: Huffman code table for {name} ({len(freq)} different characters)")
            print_code_table(freq, codes)
            print(f"\nTask 3: first 60 bits of the encoding: {bits[:60]}...")
            print(f"  decoded text equals the original: {ok}")
            print("\nTask 4: Compression compared with 8-bit fixed-length encoding")
            print(f"{'file':<20}{'chars':>7}{'distinct':>10}{'8-bit size':>12}{'Huffman':>10}{'ratio':>8}{'bits/char':>11}  decoded OK")
            print("-" * 91)
        fixed = 8 * len(text)
        ratio = len(bits) / fixed
        results.append((name.split("/")[-1], len(text), len(freq), fixed, ratio, len(bits) / len(text)))
        print(f"{name:<20}{len(text):>7,}{len(freq):>10}{fixed:>12,}{len(bits):>10,}{ratio:>8.1%}"
              f"{len(bits) / len(text):>11.2f}  {ok}")
    plot(results)
