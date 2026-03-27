class Graph:
    def __init__(self, num_nodes):
        self.n = num_nodes
        self.adjList = [[] for _ in range(num_nodes + 1)]  # 1-based indexing

    def add_edge(self, u, v, distance, accessibility):
        self.adjList[u].append((v, distance, accessibility))
        self.adjList[v].append((u, distance, accessibility))  # undirected

    def dijkstra(self, start, use_accessibility=False):
        max_val = 999999
        dist = [max_val] * (self.n + 1)
        visited = [False] * (self.n + 1)
        previous = [-1] * (self.n + 1)

        dist[start] = 0

        for _ in range(self.n):
            u = -1
            min_dist = max_val
            for i in range(1, self.n + 1):
                if not visited[i] and dist[i] < min_dist:
                    min_dist = dist[i]
                    u = i

            if u == -1:
                break

            visited[u] = True

            for neighbor, d, a in self.adjList[u]:
                weight = a if use_accessibility else d
                if dist[u] + weight < dist[neighbor]:
                    dist[neighbor] = dist[u] + weight
                    previous[neighbor] = u

        return dist, previous

    def get_path(self, previous, end):
        path = []
        while end != -1:
            path.insert(0, end)
            end = previous[end]
        return path