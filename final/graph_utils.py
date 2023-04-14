from random import randint, shuffle


def random_cycle(n):
    cycle_list = [i for i in range(n)]
    shuffle(cycle_list)

    shifted = cycle_list[1:]

    graph = set()

    for pair in zip(cycle_list, shifted):
        graph.add(pair)

    final_pair = (cycle_list[0], cycle_list[-1])
    graph.add(final_pair)
    return graph


def fair_graph(n, e):
    """
    Iterative builds up a graph with n nodes and e edges.
    The maximum degree - minimum degree will always be less than 3.
    """
    max_edges = (n*(n - 1))/2
    e = min(e, max_edges)

    # Create a cycle
    nodes = [i for i in range(n)]
    shifted = nodes[1:]
    graph = set()
    for pair in zip(nodes, shifted):
        graph.add(pair)
    final_pair = (nodes[0], nodes[-1])
    graph.add(final_pair)

    # Current number of edges
    edges = n

    node_idx = 0
    shift_val = 2

    while edges < e:
        node = nodes[node_idx]
        neighbour = nodes[(node_idx + shift_val) % n]
        pair = (node, neighbour)
        graph.add(pair)

        node_idx = (node_idx + 1) % n
        if node_idx == 0:
            shift_val += 1

        edges += 1

    return graph


def random_connected_graph(n):
    """
    Given n nodes.
    return a set of n edges that make up a connected graph.
    """
    edges = set()

    for a in range(n):
        b = randint(0, n - 1)

        # Rejection sampling
        same = lambda a, b: a == b
        repeat = lambda a, b: (a, b) in edges or (b, a) in edges
        while same(a, b) or repeat(a, b):
            b = randint(0, n - 1)

        # avoid dupes
        lt, gt = (a, b) if a < b else (b, a)
        edges.add((lt, gt))

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
