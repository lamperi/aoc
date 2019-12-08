with open("input.txt") as f:
    data = f.read().strip()

W=25
H=6

layers = []
while data:
    layers.append(data[:W*H])
    data = data[W*H:]

print(sorted((l.count("0"), l.count("1")*l.count("2")) for l in layers)[0][1])

pic=[]
for i in range(len(layers[0])):
    for l in layers:
        if l[i] != "2":
            pic.append(l[i])
            break

for j in range(0, W*H, W):
    print("".join(pic[j:j+W]).replace("0", " ").replace("1", "#"))
