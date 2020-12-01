def ints(text: str):
    for line in text.splitlines():
        yield list(map(int, line.split()))