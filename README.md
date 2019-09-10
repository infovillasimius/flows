# flows
Python network flows optimization algorithms

Shortest Path

Label Setting Algorithms:

1. Dynamic (for topologically ordered graphs)
2. Dijkstra 
3. Dial - Dijkstra (with a circular queue)
4. Radix Heap - Dijkstra (with a radix heap queue)


Label Correcting Algorithms:

1. Generic Label correcting
2. F.I.F.O. L.C.
3. Deque L.C.
4. Negative Cycle immune Label Correcting


Max Flow Algorithms:

1. Ford Fulkerson - Labeling
2. Pre flow - Push


Min Cost Flow Algorithms:

1. Successive shortest path
2. Cycle canceling


Others:

1. Topological ordering
2. Depth First Search
3. Flow decomposition


Loading a graph:
You need a text file with this structure:
1. Adjacency matrix (node - node) dimension (ex. 5)
2. Mass balance excess of nodes (ex. 25 0 0 0 -25)
3. Adjacency Matrix (ex. 0 1 1 0 0 0 0 1 1 0 0 0 0 1 1 0 0 0 0 1 0 0 0 0 0 )
4. Cost Matrix (ex. 0 7 6 0 0 0 0 6 4 0 0 0 0 2 2 0 0 0 0 1 0 0 0 0 0 )
5. Capacity Matrix (ex. 0 30 20 0 0 0 0 25 10 0 0 0 0 20 25 0 0 0 0 20 0 0 0 0 0 )