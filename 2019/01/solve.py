with open("input.txt") as f:
  s = 0
  s2=0
  for line in f:
    n = int(line)
    w = int(n/3) - 2
    s += w
    while w>0:
      s2+=w
      w=int(w/3)-2
  print(s)
  print(s2)
