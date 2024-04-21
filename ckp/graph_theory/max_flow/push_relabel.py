from ...data_structure.graph import AbstractWeightedGraph, DictFlowGraph

class PushRelabel:
    """ Implements the push-relabel max-flow algorithm. """

    def __init__(self, graph: AbstractWeightedGraph, source: int, sink: int):
        assert(source != sink)

        self.height = [0] * len(graph)
        self.height[source] = len(graph)

        excess = self.excess = [0] * len(graph)
        excess_queue = self.excess_queue = [] # TODO: use deque

        flow = self.flow = DictFlowGraph(len(graph))

        for (v, w) in graph.out_edges(source):
            if w == 0: continue
            flow.add_flow(source, v, w)
            excess[v] += w
            excess_queue.append(v)

        self._compute_flow(graph, sink)
        self.max_flow = sum(w for (_, w) in flow.out_edges(source))
    
    def _compute_flow(self, graph: AbstractWeightedGraph, sink: int):    
        excess_queue, flow = self.excess_queue, self.flow

        while excess_queue:
            u = excess_queue.pop(0)
            assert(self.excess[u] > 0)
            for v in range(len(graph)): # TODO: get a better way to get neighbors
                if self.height[v] == self.height[u]-1 and (graph.get_weight(u, v) or 0) > (flow.get_weight(u, v) or 0):
                    self._push(graph, u, v, sink)
                    break
            else:
                self._relabel(graph, u)
                excess_queue.append(u)

    def _push(self, graph: AbstractWeightedGraph, u: int, v: int, sink: int):
        assert(self.excess[u] > 0)
        excess, flow = self.excess, self.flow
        send = min(excess[u], (graph.get_weight(u, v) or 0) - (flow.get_weight(u, v) or 0))
        flow.add_flow(u, v, send)
        excess[u] -= send
        
        prev_v_excess = excess[v]
        excess[v] = prev_v_excess + send
        if v != sink and not prev_v_excess: self.excess_queue.append(v)

    def _relabel(self, graph: AbstractWeightedGraph, u: int):
        assert(self.excess[u] > 0)
        self.height[u] += 1