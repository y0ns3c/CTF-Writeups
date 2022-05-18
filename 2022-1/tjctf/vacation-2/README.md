# Problem description

> Travel agency said we can't go there anymore...

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
0000000000401176 <vacation>:
  401176:       endbr64 
  40117a:       push   rbp
  40117b:       mov    rbp,rsp
  40117e:       sub    rsp,0x10
  401182:       lea    rdi,[rip+0xe7f]        # 402008 <_IO_stdin_used+0x8>
  401189:       call   401060 <puts@plt>
  40118e:       mov    rdx,QWORD PTR [rip+0x2ebb]        # 404050 <stdin@@GLIBC_2.2.5>
  401195:       lea    rax,[rbp-0x10]
  401199:       mov    esi,0x40
  40119e:       mov    rdi,rax
  4011a1:       call   401080 <fgets@plt>
  4011a6:       nop
  4011a7:       leave  
  4011a8:       ret
```

주어진 C 소스파일을 보면 `buf` 변수는 `fgets()`의 첫 번째 인자이므로 RDI 래지스터로 전달된다.  
`buf`는 `rbp-0x10`이므로 16 바이트 뒤에는 rbp가 8바이트, 반환 주소가 8바이트 저장되어있다.

> 소스에서 배열에 16개의 원소가 있음을 선언했지만 `objdump`로 다시 확인하는 이유는 컴파일러가 스택의 정렬을 위해 더 많은 공간을 할당할 수도 있기 때문이다.

즉, 임의의 값 24바이트 이후에는 ROP 가젯들을 주어 공격할 수 있다.

#### libc 주소 유출

ROP로 공격을 해야 하는데, 주어진 바이너리만으로는 가젯이 많지 않다. 그러므로 libc를 이용하면 좋은데, 공유 라이브러리는 정확한 주소를 알 수 없으므로 libc에 있는 주소를 유출시켜 베이스 주소를 찾아야 한다.

주어진 바이너리는 `puts()`를 포함한 여러 libc 함수를 사용한다. 그렇기 때문에 이런 함수의 주소를 `.got`에서 출력하면 유출시킬 수 있다.

`puts(&puts)`를 실행할 수 있으면 puts의 주소를 획득할 수 있고, libc에서의 `puts()` 함수 offset을 빼면 실제로 로딩된 libc의 베이스 주소를 계산할 수 있다.

ROP 가젯은 다음과 같이 만들면 된다:

```
pop rdi ; ret ;
puts_got 주소 (리틀 엔디언 8바이트)
puts_plt 주소 (리틀 엔디언 8바이트)
```

> libc 베이스 주소의 하위 12비트는 반드시 0x000으로 끝나므로 libc 주소를 토대로 libc의 버전을 알 수 있다.  
> 이번에는 Ubuntu 20.04에 기본으로 탑재된 2.31 버전을 사용하고 있는 것으로 확인됐다.  
> https://libc.nullbyte.cat/

#### Return to _start

libc의 ROP 가젯을 사용하기 위해서는 위의 가젯이 먼저 실행이 되어야 한다. 그 다음에 새로운 입력값으로 libc의 ROP 가젯을 주어야 한다.

즉, 입력을 2번에 걸처 전달해야 한다. 그러나 프로그램은 입력값을 한 번만 받는다. 그렇기 때문에 첫 ROP 가젯을 줄 때, 프로그램이 다시 입력값을 요청하는 상태로 되돌려야 한다.

이때 `vacation()`로 돌아갈 경우, 문제가 발생한다. 버퍼 오퍼블로우 공격을 하는 과정에서 RBP의 값을 덮어써버려서 이제 RBP는 더 이상 스택의 올바른 위치를 가리키지 않는다. 그러므로 `vacation()` 함수에서 `fgets()` 함수를 호출할 때, `buf`가 아닌 엉뚱한 위치를 인자로 전달하게 되고 segfault가 발생할 수 있다.

libc의 주소를 유출했듯이 이전 스택프래엠이 저장된 RBP의 값을 유출시켜 복원할 수도 있겠지만, RBP의 값을 정상으로 되돌리는 간단한 방법이 있다.

바로 프로그램을 다시 실행시키는 것이다. 단, 완전히 종료하고 다시 실행하면 공유 라이브러리가 새로운 주소로 로딩되어 이전에 획득한 libc의 주소가 쓸모 없어진다.

그렇기 때문에 주어진 바이너리만 다시 시작하고 동적 로딩이 된 라이브러리는 그대로 유지할 수 있도록 `_start` 함수로 돌아간다. `_start`는 프로그램의 진입점이므로 `main` 함수가 실행되기 전에 스택과 래지스터 값을 적절하게 세팅해준다.

#### libc ROP

이후에는 libc ROP 가젯으로 `system("/bin/sh")` 함수를 호출하게 만들면 된다.

리눅스에서 `system()` 함수는 스택이 16바이트 단위로 정렬되어 있어야 하므로 segfault가 발생할 경우, 중간에 `ret` 가젯을 하나 추가해주면 된다.

#### 쉘 획득

그 이후에는 `ls` 와 `cat flag.txt`로 플래그를 획득할 수 있다.

## 플래그

tjctf{w3_g0_wher3_w3_w4nt_t0!_66f7020620e343ff}