def aheui_stack_step(stack: tuple[int, ...], op: str) -> tuple[int, ...]|None:
    if op in "23456789":
        return stack + (int(op),)
    if op in "+-*/%":
        if len(stack) < 2: return None
        x, y = stack[-2:]
        match op:
            case '+': res = x + y
            case '-': res = x - y
            case '*': res = x * y
            case '/':
                if not y: return None
                res = x // y
            case '%':
                if not y: return None
                res = x % y
        return stack[:-2] + (res,)
    if op == '^':
        if len(stack) < 1: return None
        return stack + (stack[-1],)
    if op == '~':
        if len(stack) < 2: return None
        return stack[:-2] + (stack[-1], stack[-2])

def aheui_bruteforce():
    init_state = ((), "")
    queue: list[tuple[tuple[int, ...], str]] = [init_state]

    stack_seen: dict[tuple[int, ...], int] = {(): 0}

    allowed_ops = "23456789+-*/%^~"
    # allowed_ops = "23456789+-*/^"

    for stack, code in queue:
        next_code_len = len(code)+1
        for op in allowed_ops:
            if (next_stack := aheui_stack_step(stack, op)) is None: continue
            if (prev_len := stack_seen.get(next_stack)) is not None and prev_len <= next_code_len: continue

            min_to_single = next_code_len + len(next_stack) - 1
            if min_to_single > 12: continue

            next_code = code + op
            if len(next_stack) == 1: yield (next_stack[0], next_code)

            stack_seen[next_stack] = next_code_len
            queue.append((next_stack, next_code))

if __name__ == '__main__':
    import gc; gc.disable()
    from random import choice
    curr_len = 0
    min_code = dict[int, str]()

    def format_dict(d: dict[int, str]):
        elems = list(d.items())
        lines = []
        for i in range(0, len(elems), 50):
            lines.append("    " + "".join(f"{k}: {repr(v)}, " for (k, v) in elems[i:i+50]).rstrip())
        return "{\n" + "\n".join(lines) + f"{'}'} # {len(d)} elements"

    for (v, code) in aheui_bruteforce():
        if curr_len < len(code):
            if curr_len:
                print(curr_len, len(min_code), "range", min(min_code.keys()), max(min_code.keys()))
                random_v = choice(list(min_code.keys()))
                print("Example:", random_v, "=>", min_code[random_v])
                if curr_len == 11:
                    code_arr = ["OPTIMAL_CODE = " + format_dict(min_code) + "\n\n"]

                    code_arr.append("i = 0; OPTIMAL_POS_INT_CODE = []\n")
                    code_arr.append("while i in OPTIMAL_CODE: OPTIMAL_POS_INT_CODE.append(OPTIMAL_CODE[i]); i += 1\n")
                    code_arr.append("OPTIMAL_POS_INT_LEN = list(map(len, OPTIMAL_POS_INT_CODE))\n\n")

                    code_arr.append("i = 0; OPTIMAL_NEG_INT_CODE = []\n")
                    code_arr.append("while i in OPTIMAL_CODE: OPTIMAL_NEG_INT_CODE.append(OPTIMAL_CODE[i]); i -= 1\n")
                    code_arr.append("OPTIMAL_NEG_INT_LEN = list(map(len, OPTIMAL_NEG_INT_CODE))")

                    with open("aheui-optimal.py", "w") as f:
                        f.writelines(code_arr)
                    exit(0)
            curr_len = len(code)
        min_code[v] = code