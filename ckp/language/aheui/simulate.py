def aheui_run_strip(code: str) -> str:
    stack: list[int] = []
    output: list[str|int] = []
    for ch in code:
        match ch:
            case '반': stack.append(2)
            case '받': stack.append(3)
            case '밤': stack.append(4)
            case '발': stack.append(5)
            case '밦': stack.append(6)
            case '밝': stack.append(7)
            case '밣': stack.append(8)
            case '밞': stack.append(9)
            case '다': assert(len(stack) >= 2); y, x = stack.pop(), stack.pop(); stack.append(x + y)
            case '따': assert(len(stack) >= 2); y, x = stack.pop(), stack.pop(); stack.append(x * y)
            case '타': assert(len(stack) >= 2); y, x = stack.pop(), stack.pop(); stack.append(x - y)
            case '나': assert(len(stack) >= 2); y, x = stack.pop(), stack.pop(); stack.append(x // y)
            case '라': assert(len(stack) >= 2); y, x = stack.pop(), stack.pop(); stack.append(x % y)
            case '빠': assert(len(stack) >= 1); stack.append(stack[-1])
            case '파': assert(len(stack) >= 2); stack[-1], stack[-2] = stack[-2], stack[-1]
            case '마': assert(len(stack) >= 1); stack.pop()
            case '망': assert(len(stack) >= 1); output.append(stack.pop())
            case '맣': assert(len(stack) >= 1); output.append(chr(stack.pop()))
            case '아': pass
            case '멓': output.append("".join(map(chr, reversed(stack)))); stack = []
            case _: raise ValueError(f"Unknown {ch=}")
    return "".join(map(str, output))