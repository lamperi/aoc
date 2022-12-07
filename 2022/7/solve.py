import os.path
import re

FILE = os.path.join(os.path.dirname(__file__), 'input.txt')
with open(FILE) as f:
    INPUT = f.read()

TEST = """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k"""

def solve(data):
    cwd = None
    fs = listing = {}
    stack = []
    for line in data.splitlines():
        if line.startswith("$"):
            cmd, *args = line[2:].split()
            if cmd == "cd":
                assert len(args) == 1
                if args[0] == "/":
                    cwd = "/"
                elif args[0] == "..":
                    cwd = cwd.rsplit("/")[0]
                    listing = stack.pop()
                else:
                    cwd = cwd + "/" + args[0]
                    stack.append(listing)
                    listing = listing[args[0]]
            elif cmd == "ls":
                assert len(args) == 0
                assert not listing
            else:
                assert False, cmd
        else:
            size, fname = line.split()
            assert fname not in listing
            if size == "dir":
                listing[fname] = {}
            else:
                listing[fname] = int(size)

    sizes = {}
    def walk(p, ls):
        s = 0
        for fname, size in ls.items():
            if isinstance(size, int):
                s += size
            else:
                s += walk(p + "/" + fname, size)
        sizes[p] = s
        return s
    total = walk("/", fs)

    # PART 1
    res1 = 0
    # PART 2
    target = 40000000
    best = 0
    res2 = 0
    for path, total_size in sizes.items():
        # PART 1
        if total_size <= 100000:
            res1 += total_size
        # PART 2
        if total - total_size <= target:
            if total-total_size > best:
                best = total-total_size
                res2 = total_size
    return res1, res2

print(solve(TEST))
print(solve(INPUT))
