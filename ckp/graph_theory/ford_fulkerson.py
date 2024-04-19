from ..data_structure.graph import AbstractWeightedGraph, DictFlowGraph

class FordFulkerson:
    """ Implements the Ford-Fulkerson max-flow algorithm. """

    __slots__ = ('capacity', 'flow', 'residual', 'source', 'sink', 'max_flow')

    def __init__(self, graph: AbstractWeightedGraph, source: int, sink: int):
        assert(source != sink)

        self.capacity = graph
        self.flow = DictFlowGraph(len(graph))
        self.residual = DictFlowGraph(len(graph))

        self.source, self.sink = source, sink
        self.max_flow = 0

        for u in range(len(graph)):
            for(v, wv) in graph.out_edges(u):
                self.residual.add_edge(u, v, wv)
        
        self._compute_max_flow()

    def _compute_max_flow(self):
        flow, residual = self.flow, self.residual

        while (path := self._find_path()):
            min_flow = min(residual.get_weight(u, v) or 0 for (u, v) in path)
            self.max_flow += min_flow

            for (u, v) in path:
                flow.add_flow(u, v, min_flow)
                residual.add_flow(u, v, -min_flow)

    def _find_path(self):
        source, sink = self.source, self.sink
        residual = self.residual

        prev_node = {}
        q = []

        sink_found = False
        for v in residual.out_neighbors(source):
            prev_node[v] = source
            if v == sink:
                sink_found = True
                break
            q.append(v)

        nq = []
        while (not sink_found) and q:
            nq.clear()
            for u in q:
                for v in residual.out_neighbors(u):
                    if v in prev_node: continue
                    prev_node[v] = u
                    if v == sink:
                        sink_found = True
                        break
                    nq.append(v)
                if sink_found: break
            if sink_found: break

            q, nq = nq, q
        
        if not sink_found: return []

        path = []
        x = sink

        while x != source:
            path.append(((y := prev_node[x]), x))
            x = y
        
        path.reverse()
        return path