# Problem description

> Too much school, too much work, too much writing CTF challenges... can I just go on vacation?

주어진 파일
- chall.c
- chall
- Dockerfile

---

## Writeup 작성자

- JHH20

---

## 풀이

먼저 바이너리 파일에 대한 정보를 `checksec chall` 로 확인한다.

```
Arch:     amd64-64-little       # 인텔 64비트 리틀 엔디언
RELRO:    Partial RELRO         # GOT에 쓰기 가능, 외부 함수 첫 호출 시 주소 확정
Stack:    No canary found       # 버퍼 오버플로우에 대한 보호 조치가 없다
NX:       NX enabled            # 스택에 실행권한이 없다
PIE:      No PIE (0x400000)     # 실행 시 코드의 주소가 고정이다
```

`objdump`로 `vacation()` 함수 disassemble하면 아래와 같다.

```
00000000004011ad <vacation>:
  4011ad:       endbr64 
  4011b1:       push   rbp
  4011b2:       mov    rbp,rsp
  4011b5:       sub    rsp,0x10
  4011b9:       lea    rdi,[rip+0xe50]        # 402010 <_IO_stdin_used+0x10>
  4011c0:       call   401070 <puts@plt>
  4011c5:       mov    rdx,QWORD PTR [rip+0x2e94]        # 404060 <stdin@@GLIBC_2.2.5>
  4011cc:       lea    rax,[rbp-0x10]
  4011d0:       mov    esi,0x40
  4011d5:       mov    rdi,rax
  4011d8:       call   4010a0 <fgets@plt>
  4011dd:       nop
  4011de:       leave  
  4011df:       ret
```

주어진 C 소스파일을 보면 `buf` 변수는 `fgets()`의 첫 번째 인자이므로 RDI 래지스터로 전달된다.  
`buf`는 `rbp-0x10`이므로 16 바이트 뒤에는 rbp가 8바이트, 반환 주소가 8바이트 저장되어있다.

> 소스에서 배열에 16개의 원소가 있음을 선언했지만 `objdump`로 다시 확인하는 이유는 컴파일러가 스택의 정렬을 위해 더 많은 공간을 할당할 수도 있기 때문이다.

즉, 24바이트 + `shell_land()` 함수의 주소를 리틀 엔디언으로 8바이트, 총 32바이트를 주면 될 것 같다.

그러나 오류가 발생하고 프로그램이 종료하게 된다. 왜냐하면 리눅스에서 `system()` 함수는 호출될 때 스택이 16바이트 단위로 정렬되어야 하는데 그렇지 않았기 때문에다.

그러므로 중간에 `ret` 가젯을 하나 추가하면 8바이트 주소가 추가되어 스택이 정렬된다.

정리하자면, 임의의 값 24 바이트 + `ret` 가젯 8바이트 + `shell_land()` 주소 8바이트를 입력값으로 넣어주면 쉘을 획득할 수 있다.

그 이후에는 `ls` 와 `cat flag.txt`로 플래그를 획득할 수 있다.

## 플래그

tjctf{wh4t_a_n1c3_plac3_ind33d!_7609d40aeba4844c}