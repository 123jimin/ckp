from .from_text import aheui_from_text

lines = []

try:
    while True:
        lines.append(input())
except:
    pass

print(aheui_from_text("\n".join(lines)))