# TraceLab

**Interactive Data Structures & Algorithms Laboratory**  
*Version 2.0 · Python Engine + FastAPI Backend + React/Vite Frontend*

TraceLab is a local, educational laboratory for running, watching, measuring, and comparing data structures and algorithms. A Python engine executes algorithms, records intermediate state snapshots, and performs 3-pass performance measurements. A React web app replays those events step-by-step, displays measured metrics alongside theoretical asymptotic complexities, and renders fair, multi-algorithm benchmark comparisons.

---

## 🚀 Quick Start

### 1. Requirements & Setup
- **Python 3.11+**
- **Node.js 18+** & `npm`

Install backend dependencies:
```bash
pip install -r requirements.txt
```

Install frontend dependencies and build production assets:
```bash
cd frontend
npm install
npm run build
cd ..
```

### 2. Run Single Integrated Server
Launch the complete application (API + built React UI):
```bash
python main.py
```
Open **[http://localhost:8000](http://localhost:8000)** in your browser.

---

## 🛠️ Development Workflow

Run API and Vite frontend dev server in two separate terminals:

**Terminal 1 (FastAPI API on `:8000`):**
```bash
python main.py --dev
```

**Terminal 2 (Vite Dev Server on `:5173` with proxy):**
```bash
cd frontend
npm run dev
```

---

## 🧪 Testing

Run backend unit tests and trace contract tests:
```bash
pytest
```

---

## 📊 Algorithm Scope (28 Algorithms)

| Category | Algorithm | Stage | Compare Group | Best | Average | Worst | Space |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Sorting** | Bubble Sort | Array | Sorting | O(n) | O(n²) | O(n²) | O(1) |
| | Selection Sort | Array | Sorting | O(n²) | O(n²) | O(n²) | O(1) |
| | Insertion Sort | Array | Sorting | O(n) | O(n²) | O(n²) | O(1) |
| | Merge Sort | Array | Sorting | O(n log n) | O(n log n) | O(n log n) | O(n) |
| | Quick Sort | Array | Sorting | O(n log n) | O(n log n) | O(n²) | O(log n) |
| | Heap Sort | Array | Sorting | O(n log n) | O(n log n) | O(n log n) | O(1) |
| **Searching** | Linear Search | Array | Searching | O(1) | O(n) | O(n) | O(1) |
| | Binary Search | Array | Searching | O(1) | O(log n) | O(log n) | O(1) |
| **String** | Naive Search | String | String matching | O(n) | O(m*(n-m+1)) | O(m*(n-m+1)) | O(1) |
| | Rabin-Karp | String | String matching | O(n+m) | O(n+m) | O(n*m) | O(1) |
| | KMP Search | String | String matching | O(n) | O(n+m) | O(n+m) | O(m) |
| | Z Algorithm | String | String matching | O(n+m) | O(n+m) | O(n+m) | O(n+m) |
| **Dynamic Programming** | 0/1 Knapsack | DP Table | — | O(n*W) | O(n*W) | O(n*W) | O(n*W) |
| | LCS | DP Table | — | O(m*n) | O(m*n) | O(m*n) | O(m*n) |
| | LIS | DP Table | — | O(n²) | O(n²) | O(n²) | O(n) |
| | MCM | DP Table | — | O(n³) | O(n³) | O(n³) | O(n²) |
| | Edit Distance | DP Table | — | O(m*n) | O(m*n) | O(m*n) | O(m*n) |
| **Graph Traversal** | BFS | Graph | Traversal | O(V+E) | O(V+E) | O(V+E) | O(V) |
| | DFS | Graph | Traversal | O(V+E) | O(V+E) | O(V+E) | O(V) |
| **Graph Shortest Paths** | Dijkstra | Graph | Shortest path | O((V+E)log V) | O((V+E)log V) | O((V+E)log V) | O(V) |
| | Bellman-Ford | Graph | Shortest path | O(V*E) | O(V*E) | O(V*E) | O(V) |
| | Floyd-Warshall | Graph | — | O(V³) | O(V³) | O(V³) | O(V²) |
| **Graph MST** | Prim's MST | Graph | Minimum spanning tree | O((E+V)log V) | O((E+V)log V) | O((E+V)log V) | O(V+E) |
| | Kruskal's MST | Graph | Minimum spanning tree | O(E log E) | O(E log E) | O(E log E) | O(V+E) |
| **Greedy** | Activity Selection | Greedy | — | O(n log n) | O(n log n) | O(n log n) | O(1) |
| | Fractional Knapsack | Greedy | — | O(n log n) | O(n log n) | O(n log n) | O(1) |
| | Huffman Coding | Greedy | — | O(n log n) | O(n log n) | O(n log n) | O(n) |
| | Job Sequencing | Greedy | — | O(n²) | O(n²) | O(n²) | O(n) |

---

## 🏛️ System Architecture

```
React App (Catalogue, Lab, Compare) ⇄ REST API (FastAPI) ⇄ Engine
                                                          ├→ Registry
                                                          ├→ Execution Engine & State Recorder → Trace JSON
                                                          ├→ Performance Analyzer (3-pass timing/memory/ops)
                                                          └→ Comparison Benchmark Engine
```

- **Algorithm Independence**: Python algorithm functions yield step events without direct FastAPI or timing dependencies.
- **3-Pass Separate Measurement**: Timing, peak memory (`tracemalloc`), and step operation counting run in isolated passes to eliminate measurement overhead.
- **Trace Contract**: Every algorithm step snapshot contains a 1-based index, event type, plain-English message, complete visual state, and monotonically non-decreasing operation counters.
