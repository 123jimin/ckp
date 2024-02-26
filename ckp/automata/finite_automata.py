import unittest

class DFA:
    """
        A class representing deterministic finite automatas.
        Alphabets should be integers.
    """

    __slots__ = ('nodes', 'accept')
    nodes: list[dict[int, int]]
    accept: set[int]

    def __init__(self, nodes: list[dict[int, set[int]]], accept: set[int]):
        self.nodes = nodes
        self.accept = accept

    def __repr__(self): return f"DFA({self.nodes}, {self.accept})"
    def __len__(self) -> int: return len(self.nodes)
    
    def get_alphabet(self) -> set[int]:
        """ Returns the set of integers used as alphabets in this DFA. """
        alphabet = set[int]()
        for node in self.nodes:
            alphabet.update(node.keys())
        return alphabet
    
    def test(self, s) -> bool:
        """ Check whether `s` is accepted by this DFA. `s`'s type is `Iterable[int]`. """
        curr_state = 0
        nodes = self.nodes
        for c in s:
            next_state = nodes[curr_state].get(c)
            if next_state is None:
                return False
            curr_state = next_state
        
        return curr_state in self.accept
    
    def find_accept_str(self, allow_empty:bool = True) -> list[int]|None:
        """ Find an input that's accepted by this DFA. """
        nodes, accept = self.nodes, self.accept
        if allow_empty and (0 in accept):
            return []

        queue = [0]
        history = {0: (None, 0)}
        i = 0
        while i < len(queue):
            state = queue[i]
            for (ch, next_state) in nodes[state].items():
                if next_state in history: continue
                if next_state in accept:
                    seq = [ch]
                    while state:
                        ch, state = history[state]
                        seq.append(ch)
                    seq.reverse()
                    return seq
                history[next_state] = (ch, state)
                queue.append(next_state)
            i += 1
        return None

    def __and__(self, other):
        """ Construct a DFA that accepts intersection of this DFA and the other DFA's languages. """
        accept = set()
        len_other = len(other)
        nodes = []
        for (i, node_i) in enumerate(self.nodes):
            is_i_accept = i in self.accept
            for (j, node_j) in enumerate(other.nodes):
                if is_i_accept and (j in other.accept):
                    accept.add(len_other*i + j)
                node = dict()
                for (ch, ni) in node_i.items():
                    nj = node_j.get(ch)
                    if nj is not None:
                        node[ch] = len_other*ni + nj
                nodes.append(node)
        return DFA(nodes, accept)

    def to_dot(self, alphabet_names: dict[int, str]|None = None) -> str:
        """
            Generate a DOT represention of this DFA, which can be viewed with Graphviz.
            The `alphabet_names` argument, if present, will be used for displaying alphabets.
        """
        accept = "".join(f"{a}[peripheries=2];" for a in self.accept)
        edges = "".join("".join(f"\"{i}\"->\"{x}\"[label=\"{(alphabet_names.get(ch) if alphabet_names else ch) or ch}\"]" for (ch, x) in node.items()) for (i, node) in enumerate(self.nodes))
        return f"digraph DFA {{{accept}{edges}}}"

class NFA:
    """
        A class representing non-deterministic finite automatas.
        Alphabets should be non-zero integers.
    """

    __slots__ = ('nodes', 'accept')

    nodes: list[dict[int, set[int]]]
    accept: set[int]

    def __init__(self, nodes:list[dict[int, set[int]]], accept:set[int]):
        self.nodes = nodes
        self.accept = accept

    def __repr__(self) -> str: return f"NFA({self.nodes}, {self.accept})"
    def __len__(self) -> int: return len(self.nodes)
    
    def get_alphabet(self) -> set[int]:
        """ Returns the set of integers used as alphabets in this NFA. """
        alphabet = set[int]()
        for node in self.nodes:
            alphabet.update(node.keys())
        alphabet.remove(0)
        return alphabet

    def test(self, s) -> bool:
        """ Check whether `s` is accepted by this NFA. `s`'s type is `Iterable[int]`. """
        curr = self.eps_closure({0})
        for c in s:
            curr = self.next_closure(curr, c)
            if len(curr) == 0:
                return False
        return not self.accept.isdisjoint(curr)
    
    def eps_closure(self, start:set[int]) -> frozenset[int]:
        """ Returns the epsilon-closure of `start`, by modifying it in-place and returning the `frozenset` version of it. """
        
        check = list(start)
        while check:
            x = check.pop()
            for (e, ns) in self.nodes[x].items():
                if e: continue
                for n in ns:
                    if n not in start:
                        start.add(n)
                        check.append(n)

        return frozenset(start)
    
    def next_closure(self, curr_closure:frozenset[int], ch:int) -> frozenset[int]:
        """ Assuming that `curr_closure` is an epsilon-closure, returns the set of reachable states (which shall be another epsilon-closure) via `ch`. """
        next_closure = set()
        for s in curr_closure:
            if xl := self.nodes[s].get(ch):
                next_closure.update(xl)
        return self.eps_closure(next_closure)
    
    def to_powerset_dfa(self, alphabet:set[int]|None = None) -> DFA:
        """ Constructs a DFA, via the powerset construction. """
        start_set = self.eps_closure({0})
        powersets = [start_set]
        powerset_inds = {start_set: 0}
        nodes = []

        if alphabet is None:
            alphabet = self.get_alphabet()
        else:
            alphabet.remove(0)

        i = 0
        while i < len(powersets):
            node = dict[int, int]()
            curr_set = powersets[i]

            for c in alphabet:
                next_set = self.next_closure(curr_set, c)
                if len(next_set) == 0: continue

                next_ind = powerset_inds.get(next_set)
                if next_ind is None:
                    next_ind = len(powersets)
                    powersets.append(next_set)
                    powerset_inds[next_set] = next_ind

                node[c] = next_ind
            
            nodes.append(node)
            i += 1
        
        accept = self.accept
        accept = set(i for (i, s) in enumerate(powersets) if not accept.isdisjoint(s))

        return DFA(nodes, accept)

    def reversed(self):
        """ Returns the NFA accepting reversed `s`, whenever `s` is a string accepted by this NFA. """
        return NFA.from_reversed(self)

    def minimize(self) -> DFA:
        """ Returns the minimal DFA. Currently, the Brzozowski's algorithm is used. """
        return self.minimize_brzozowski()

    def minimize_brzozowski(self) -> DFA:
        """ Returns the minimal DFA by using the Brzozowski's algorithm. """
        return NFA.from_reversed_dfa(self.reversed().to_powerset_dfa()).to_powerset_dfa()

    def kleene_star(self):
        accept = len(self.nodes)+1
        nodes = [{0:{1,accept}}]
        nodes.extend(dict((ch, set(x+1 for x in xl)) for (ch, xl) in node.items()) for node in self.nodes)
        nodes.append({})

        for x in self.accept:
            curr_node = nodes[x+1] = NFA._copy_node(nodes[x+1])
            edges = NFA._get_edge(curr_node, 0)
            edges.update((1, accept))

        return NFA(nodes, {accept})

    def __add__(self, other):
        return NFA.concat([self, other])
    
    @staticmethod
    def concat(nfa_it):
        nodes: list[dict[int, set[int]]] = []
        prev_offset = 0
        curr_offset = 0
        prev_nfa = None
        
        for nfa in nfa_it:
            assert(isinstance(nfa, NFA))

            nodes.extend(dict((ch, set(x+curr_offset for x in xl)) for (ch, xl) in node.items()) for node in nfa.nodes)
            if prev_nfa:
                for a in prev_nfa.accept:
                    NFA._get_edge(nodes[a+prev_offset], 0).add(curr_offset)

            prev_nfa = nfa
        
            prev_offset = curr_offset
            curr_offset += len(nfa.nodes)
        
        accept = set(a + prev_offset for a in prev_nfa.accept)

        return NFA(nodes, accept)

    def __or__(self, other):
        if other is None: return self
        return NFA.union([self, other])
    
    @staticmethod
    def union(nfa_it):
        nodes: list[dict[int, set[int]]] = [{}]
        accept = set()
        curr_offset = 1

        for nfa in nfa_it:
            if not nfa: continue
            assert(isinstance(nfa, NFA))

            NFA._get_edge(nodes[0], 0).add(curr_offset)
            accept.update(a+curr_offset for a in nfa.accept)
            nodes.extend(dict((ch, set(x+curr_offset for x in xl)) for (ch, xl) in node.items()) for node in nfa.nodes)

            curr_offset += len(nfa.nodes)

        return NFA(nodes, accept)

    @staticmethod
    def from_char(ch: int):
        return NFA([{ch:{1}}, dict()], {1})
    
    @staticmethod
    def from_str(s):
        nodes = [dict({c: {i+1}}) for (i, c) in enumerate(s)]
        nodes.append(dict())
        return NFA(nodes, {len(s)})
    
    @staticmethod
    def from_dfa(dfa: DFA):
        return NFA([{(ch, {x}) for (ch, x) in node.items()} for node in dfa.nodes], dfa.accept)
    
    @staticmethod
    def from_reversed_dfa(dfa: DFA):
        nodes = [{0: set(x+1 for x in dfa.accept)}]
        nodes.extend(dict() for _ in range(len(dfa)))

        for (i, node) in enumerate(dfa.nodes):
            for (ch, x) in node.items():
                NFA._get_edge(nodes[x+1], ch).add(i+1)
        
        return NFA(nodes, {1})
    
    @staticmethod
    def from_reversed(nfa):
        nodes = [{0: set(x+1 for x in nfa.accept)}]
        nodes.extend(dict() for _ in range(len(nfa)))

        for (i, node) in enumerate(nfa.nodes):
            for (ch, xl) in node.items():
                for x in xl:
                    NFA._get_edge(nodes[x+1], ch).add(i+1)
        
        return NFA(nodes, {1})

    @staticmethod
    def _get_edge(node: dict[int, set[int]], out: int) -> set[int]:
        e = node.get(out)
        if not e: node[out] = e = set[int]()
        return e
    
    @staticmethod
    def _copy_node(node: dict[int, set[int]]) -> dict[int, set[int]]:
        return dict((k, v.copy()) for (k, v) in node.items())
    
    def to_dot(self, alphabet_names: dict[int, str]|None = None) -> str:
        """
            Generate a DOT represention of this DFA, which can be viewed with Graphviz.
            The `alphabet_names` argument, if present, will be used for displaying alphabets.
        """
        def get_name(ch: int) -> str:
            if alphabet_names:
                if s := alphabet_names.get(ch):
                    return s
            if ch == 0:
                return "\u03B5"
            return f"{ch}"
                
        accept = "".join(f"{a}[peripheries=2];" for a in self.accept)
        edges = "".join("".join(
            "".join(f"\"{i}\"->\"{x}\"[label=\"{get_name(ch)}\"]" for x in xl)
            for (ch, xl) in node.items()) for (i, node) in enumerate(self.nodes))
        return f"digraph NFA {{{accept}{edges}}}"