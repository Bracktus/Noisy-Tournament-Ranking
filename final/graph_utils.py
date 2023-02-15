from random import randint

def random_connected_graph(n):
    """
    Given n nodes. 
    return a set of n edges that make up a connected graph.
    """
    edges = set()
    
    for a in range(n):
        b = randint(0, n - 1)

        # Rejection sampling
        same = lambda a, b : a == b
        repeat = lambda a, b: (a,b) in edges or (b,a) in edges
        while same(a, b) or repeat(a,b):
            b = randint(0, n - 1)

        edges.add((a,b))

    return edges


def connected_graph(n, k):
    """
    Given n nodes.
    Return a set of ~n*k edges that make up a connected graph
    """
    edges = set()

    for _ in range(k):
        g = random_connected_graph(n)
        edges = edges.union(g)

    return list(edges)

        

            
        

    
