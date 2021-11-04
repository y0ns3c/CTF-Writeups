with open("scrambled.jpg", "rb") as scrambled_img:
    dump = scrambled_img.read()

grid = []
size = len(dump)
assert size % 5 == 0
for n in range(0, size, 5):
    temp = []
    for k in range(5):
        temp.append(dump[n + k])
    grid.append(temp)

def swapRow(a, b):
    for c in range(5):
        temp = grid[a][c]
        grid[a][c] = grid[b][c]
        grid[b][c] = temp


# Step 4
for i, row in enumerate(grid):
    if i % 2 == 0:
        for _ in range(2):
            temp = row[0]
            for k in range(4):
                row[k] = row[k + 1]
            row[4] = temp
    else:
        temp = row[4]
        for k in range(4, 0, -1):
            row[k] = row[k - 1]
        row[0] = temp


# Step 3
for n in range(0, len(grid), 2):
    swapRow(n, n + 1)


# Step 2 swap columns
for row in grid:
    temp = row[0]
    row[0] = row[4]
    row[4] = temp
    temp = row[1]
    row[1] = row[3]
    row[3] = row[2]
    row[2] = temp




# Write output
with open("flag.jpg", "wb") as output:
    for row in grid:
        output.write(bytearray(row))
