# Problem description

> Travel agency said we can't go there anymore...

주어진 파일
- chall.c
- chall

---

## Writeup 작성자

- JHH20

---

## 풀이

먼저 바이너리 파일에 대한 정보를 `checksec chall` 로 확인한다.

```
Arch:     amd64-64-little       # 인텔 64비트 리틀 엔디언
RELRO:    Full RELRO            # 외부 함수의 주소가 실행 시 확정, .got 쓰기 불가능
Stack:    No canary found       # 버퍼 오버플로우에 대한 보호 조치가 없다
NX:       NX enabled            # 스택에 실행권한이 없다
PIE:      PIE enabled           # 실행 시 코드의 주소가 랜덤이다
```

#### 소스 분석

`main()` 함수에서 rgb 값을 입력으로 받는다. 이때, 상수값으로 주어진 `myFavoriteColor`와 일치하면 안 된다.

그 다음에는 이름을 문자열로 받는다. 이때, scanf에 길이 제한이 없으므로 버퍼 오버플로우가 발생할 수 있다.

> scanf는 공백 문자(`\x09, \x0a, \x0b, \x0c, \x0d, \x20`)가 입력될 때까지 계속 문자열을 받는다  
> (`\x00`에서는 멈추지 않는다)

그 다음에는 첫 입력에서 받은 rgb 값을 구조체에 전달한다.

#### 지역변수 주소

`objdump`로 `main()` 함수를 disassemble하면 지역변수의 주소를 알 수 있댜.

소스에서 두 번째 `scanf()` 함수가 호출되는 부분 다음을 확인하면 아래와 같다.

```
0000000000001229 <main>:
    1229:                 endbr64 
    122d:                 push   rbp
    122e:                 mov    rbp,rsp
    1231:                 sub    rsp,0xa0

    ...                   ...    // 생략

// r, g, b 지역변수에서 c 구조체 변수 값 지정
    12df:                 movzx  eax,BYTE PTR [rbp-0x9]
    12e3:                 mov    BYTE PTR [rbp-0x10],al
    12e6:                 movzx  eax,BYTE PTR [rbp-0xa]
    12ea:                 mov    BYTE PTR [rbp-0xf],al
    12ed:                 movzx  eax,BYTE PTR [rbp-0xb]
    12f1:                 mov    BYTE PTR [rbp-0xe],al
// printf 호출
    12f4:                 movzx  eax,BYTE PTR [rip+0x2d47]        # 4042 <myFavoriteColor+0x22>
    12fb:                 movzx  r8d,al
    12ff:                 movzx  eax,BYTE PTR [rip+0x2d3b]        # 4041 <myFavoriteColor+0x21>
    1306:                 movzx  edi,al
    1309:                 movzx  eax,BYTE PTR [rip+0x2d30]        # 4040 <myFavoriteColor+0x20>
    1310:                 movzx  esi,al
    1313:                 movzx  eax,BYTE PTR [rbp-0xe]     // c.b
    1317:                 movzx  r10d,al
    131b:                 movzx  eax,BYTE PTR [rbp-0xf]     // c.g
    131f:                 movzx  ecx,al
    1322:                 movzx  eax,BYTE PTR [rbp-0x10]    // c.r
    1326:                 movzx  edx,al
    1329:                 lea    rax,[rbp-0x30]             // c.friendlyName
    132d:                 sub    rsp,0x8
    1331:                 push   r8
    1333:                 push   rdi
    1334:                 push   rsi
    1335:                 lea    r9,[rip+0x2ce4]        # 4020 <myFavoriteColor>
    133c:                 mov    r8d,r10d
    133f:                 mov    rsi,rax
    1342:                 lea    rdi,[rip+0xd37]        # 2080 <_IO_stdin_used+0x80>
    1349:                 mov    eax,0x0
    134e:                 call   10f0 <printf@plt>
```

리눅스가 따르는 System V ABI에 따르면 인자는 다음 순으로 전달된다:  
`RDI > RSI > RDX > RCX > R8 > R9 > 스택에 push`

`printf()` 함수의 인자로부터 `c` 변수의 주소를 파악한 다음, rgb 값이 전달되는 부분을 통해 `r`, `g`, `b` 변수의 주소를 파악할 수 있다.
그러므로 지역변수의 주소는 다음과 같다:

```
             r = rbp-0x9
             g = rbp-0xa
             b = rbp-0xb
           c.b = rbp-0xe
           c.g = rbp-0xf
           c.r = rbp-0x10
c.friendlyName = rbp-0x30
```

#### 버퍼 오버플로우 공격

첫 입력값은 (0x32, 0x54, 0x34)가 아닌 임의의 rgb 값을 주면 된다.

> 단, 직접 실행했을 때, 버그였는지 rgb 값이 제대로 저장되지 않았다.  
> `1 2 3`을 입력하면 `r = 1`만 입력되어 `c.friendlyName = "2"`가 되었고  
> `1, 2, 3`을 입력하면 `b = 3`만 입력되었다.  
> 만약 첫 입력이 제대로 전달되었다면, rgb 중 하나만 다르게 설정하고 버퍼 오버플로우 공격에서 더 적은 데이터만 수정해도 되었을 것이다.

두 번째 입력값에서는 `c.friendlyname`에서 `r`, `g`, `b`, 변수까지 덮어써야 하므로 임의의 문자 `0x30 - 0xb = 0x25`바이트 다음에 `b`, `g`, `r` 값을 1바이트씩 주면 된다.

## 플래그

tjctf{i_l1k3_gr3y_a_l0t_f49ad3}