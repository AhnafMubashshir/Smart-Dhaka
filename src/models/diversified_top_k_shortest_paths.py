import heapq
from typing import List, Dict, Tuple

class DiversifiedTopKShortestPaths:
    def __init__(self, graph: Dict[str, List[Tuple[str, float]]], similarity_threshold: float, k: int):
        self.graph = graph
        self.similarity_threshold = similarity_threshold
        self.k = k

    def similarity(self, path1: List[str], path2: List[str]) -> float:
        # Implement a similarity function (e.g., Jaccard similarity) 
        intersection = len(set(path1) & set(path2))
        union = len(set(path1) | set(path2))
        return intersection / union if union != 0 else 0

    def find_shortest_paths(self, start: str, target: str) -> List[List[str]]:
        # Priority queue for Dijkstra's algorithm: stores tuples of (cost, path)
        min_heap = [(0, [start])]
        # List to store the k shortest paths
        paths = []
        # Dictionary to keep track of the minimum cost to reach each node
        min_cost = {start: 0}

        while min_heap and len(paths) < self.k:
            # Pop the path with the smallest cost
            cost, path = heapq.heappop(min_heap)
            node = path[-1]

            # Check if we reached the target node
            if node == target:
                paths.append(path)
                continue

            # Explore neighbors
            for neighbor, weight in self.graph.get(node, []):
                new_cost = cost + weight

                # Only consider this path if it provides a cheaper way to reach `neighbor`
                if neighbor not in min_cost or new_cost < min_cost[neighbor]:
                    min_cost[neighbor] = new_cost
                    heapq.heappush(min_heap, (new_cost, path + [neighbor]))

        return paths

    def diversified_top_k_paths(self, start: str, target: str) -> List[List[str]]:
        all_paths = self.find_shortest_paths(start, target)
        diversified_paths = []

        for path in all_paths:
            if all(self.similarity(path, p) <= self.similarity_threshold for p in diversified_paths):
                diversified_paths.append(path)
                if len(diversified_paths) == self.k:
                    break

        return diversified_paths
