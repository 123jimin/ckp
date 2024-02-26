from .finite_automata import NFA

class RegexAST:
    """
        Class for parsing (pure) regular expression into an AST.
        ```
        regex_ast = RegexAST.parse("(a|ab)*(ba|b)*")
        ```
    """

    __slots__ = ('kind', 'value', 'children')

    kind: str # '.', '+', '|', '*'
    value: str|None
    children: list|None

    def __init__(self, kind: str, value: str|None = None, children: list|None = None):
        self.kind = kind
        self.value = value
        self.children = children
    
    def __repr__(self):
        args = [repr(self.kind)]
        if self.value: args.append(repr(self.value))
        if self.children:
            if self.value: args.append(repr(self.children))
            else: args.append("children=" + repr(self.children))
        args_str = ", ".join(args)
        return f"RegexAST({args_str})"

    def kleene_star(self):
        if self.kind == '*': return self
        return RegexAST('*', None, [self])

    def __add__(self, other):
        if other is None: return self
        if not isinstance(other, RegexAST): return NotImplemented
        self_list = self.children if self.kind == '+' else [self]
        other_list = other.children if other.kind == '+' else [other]
        return RegexAST('+', None, self_list + other_list)
        
    def __radd__(self, other):
        if other is None: return self
        return NotImplemented

    def __or__(self, other):
        return RegexAST.union([self, other])

    @staticmethod
    def union(ast_list):
        if not ast_list: return None
        if len(ast_list) == 0: return None

        union_ch = []
        for ast in ast_list:
            if ast is None: continue
            if ast.kind == '|':
                union_ch.extend(ast.children)
            else:
                union_ch.append(ast)

        if len(union_ch) == 0:
            return None
        if len(union_ch) == 1:
            return union_ch[0]

        return RegexAST('|', None, union_ch)

    def _parenthesize(self) -> str:
        if self.kind == '|':
            return f"({str(self)})"
        else:
            return str(self)

    def __str__(self) -> str:
        match self.kind:
            case '.':
                return self.value
            case '+':
                return "".join(child._parenthesize() for child in self.children)
            case '|':
                return "|".join(map(str, self.children))
            case '*':
                child = self.children[0]
                return f"{child._parenthesize()}*"
    
    def to_nfa(self) -> NFA:
        match self.kind:
            case '.':
                return NFA.from_char(ord(self.value))
            case '+':
                return NFA.concat(map(RegexAST.to_nfa, self.children))
            case '|':
                return NFA.union(map(RegexAST.to_nfa, self.children))
            case '*':
                return RegexAST.to_nfa(self.children[0]).kleene_star()
    
    @staticmethod
    def parse(src: str):
        stack = []
        curr = [None]

        for (i, c) in enumerate(src):
            match c:
                case '(':
                    stack.append(curr)
                    curr = [None]
                case '|':
                    curr.append(None)
                case ')':
                    union = RegexAST.union(curr)
                    curr = stack.pop()
                    if i+1 < len(src) and src[i+1] == '*':
                        curr[-1] = curr[-1] + union.kleene_star()
                    else:
                        curr[-1] = curr[-1] + union
                case '*':
                    pass
                case _:
                    if i+1 < len(src) and src[i+1] == '*':
                        curr[-1] = curr[-1] + RegexAST('.', c).kleene_star()
                    else:
                        curr[-1] = curr[-1] + RegexAST('.', c)

        assert(not stack)
        return RegexAST.union(curr)