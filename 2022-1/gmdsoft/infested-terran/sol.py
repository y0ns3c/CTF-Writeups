#!/usr/bin/env python3
from pwn import *

log = success # alias
bin_fname = "./sl"
context.binary = bin_fname
context.terminal = ["tmux", "splitw", "-h"]

def readlong(elf: ELF, addr: int, nelem: int):
    output = [] # type: list[int]
    for i in range(nelem):
        ldata = elf.read(addr + i * 8, 8)
        output.append(u64(ldata))
    return output

def printx(arr): # type: (list[int]) -> None
    print([hex(v) for v in arr])

elf = ELF(bin_fname)
qword_4020 = readlong(elf, 0x4020, 36)
qword_4140 = readlong(elf, 0x4140, 36)

printx(qword_4020)
print()
printx(qword_4140)
print()

flag = [0] * 36
errs = []
for i in range(36):
    prev = qword_4140[i - 1] if i > 0 else 0
    target = qword_4140[i] - prev
    flag[i] = target // qword_4020[i]
    if flag[i] * qword_4020[i] + prev != qword_4140[i]:
        errs.append(i)

print("out:")
print(errs)
printx(flag)
print()
log(bytes(flag).decode())
