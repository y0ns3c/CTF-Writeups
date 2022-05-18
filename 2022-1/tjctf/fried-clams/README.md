# Problem description

> so what do you do with the shells then?

주어진 파일
- chall
- Dockerfile

---

## Writeup 작성자

- JHH20

---

## 풀이

#### 접근법은 알겠으나 플래그 획득 실패

먼저 바이너리 파일에 대한 정보를 `checksec chall` 로 확인한다.

```
Arch:     amd64-64-little       # 인텔 64비트 리틀 엔디언
RELRO:    Full RELRO            # 외부 함수의 주소가 실행 시 확정, .got 쓰기 불가능
Stack:    No canary found       # 버퍼 오버플로우에 대한 보호 조치가 없다
NX:       NX enabled            # 스택에 실행권한이 없다
PIE:      PIE enabled           # 실행 시 코드의 주소가 랜덤이다
```

`objdump`를 확인한 결과, symbols가 대부분 제거된 상태이다. `.text`에 있는 명령어들이 함수 단위로 나누어지지 않아서 직접 함수로 나누고 정리했다.

#### 어셈블리 분석

`readelf -h chall`로 entry point (`_start`)가 0x11a0에 시작한다는 힌트를 얻고, `ret` / `jmp` 명령어 위주로 함수의 경계를 찾았다. 그리고 비슷한 (PIE enabled) C 프로그램을 참고해서 컴파일러가 자동 생성하는 함수를 정리했다. 이때 본인은 `favorite-color` 문제의 실행 파일을 참고했다.

`.text` 첫 부분에 있는 코드는 `main()` 함수인 듯하다.  
더 주의깊게 리버싱을 해야 하기 때문에 함수 호출 / 조건문 / 반복문 단위로 나누었다.

> 함수 호출은 `objdump`에서 `call ???  <?@plt>`와 같이 알기 쉬운 줄이 있어서 System V ABI에 따른 인자를 설정하는 부분까지를 함수 호출로 나눌 수 있다.
>
> 조건문은 `je` / `jle`와 같은 조건부 점프 명령어와 그 직전에 `test` / `cmp`와 같은 명령어를 보고 나눌 수 있다.
>
> 반복문은 반복문 안의 코드가 먼저 나오고 그 뒤에 조건문이 붙는다. 조건문의 끝에는 반복문 안의 첫 명령어로 이동하는 조건부 점프 명령어가 있다. `for` / `while`처럼 첫 회에도 조건을 확인하는 경우, 조건문으로 `jmp`해서 진입한다.

그렇게 정리한 결과가 [disasm.txt](disasm.txt) 이다.

#### 어셈블리를 C 언어로 리버싱

```c
#define _GNU_SOURCE
#include <stdio.h>
#include <string.h>
#include <stdbool.h>
#include <sys/unistd.h>
#include <sys/mman.h>

int main() {
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);

    puts("the New England special!");

    //  (addr, length, prot, flags, fd, offset)
    char *ptr = mmap(NULL, 0x1000, PROT_READ | PROT_WRITE | PROT_EXEC, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);

    // (fd, buf, count)
    ssize_t count = read(stdin, ptr, 0x1000);

    bool pass = true;
    for(int i = 0; i < count; ++i) {
        if (ptr[i] - '0' > 'N') {
            pass = false;
            break;
        }
    }

    if (pass) {
        puts("yummy!");
        strfry(ptr);
        ((void(*)())ptr)();
    } else {
        puts("yuck!");
    }
}
```

#### C 코드 해석

`mmap()`을 통해 0x1000 바이트 메모리를 할당받는다. 이때 읽기, 쓰기, 실행 권한이 전부 주어진다.

할당받은 메모리에 0x1000 바이트를 읽는다.

입력된 모든 바이트는 0x30 - 0x7e 사이의 값을 가져야 한다 ('0' - '~')

입력값을 확인한 이후에 `strfry()` 함수로 입력값을 랜덤 재배열한 다음, 실행한다.

#### 플래그 획득 실패 이유와 해결방법

`strfry()` 함수가 랜덤으로 입력값을 섞어놓기 때문에 적절한 쉘코드를 작성하지 못해 막혔다. 최대한 짧은 쉘코드를 작성하고 여러번 실행하여 변하지 않을 확률에 기대야 한다고 생각했지만, `read() syscall`을 실행하려고 해도 7바이트에 `syscall` 명령어가 허용된 값의 범위를 벗어났다.

다만, `strfry()` 함수에 대한 대처를 할 수 있다는 것을 나중에 알게 되었다. `pystrfry` pip 모듈과 같은 라이브러리가 있기 때문에 이를 활용하여 `strfry()`의 역함수를 만들어 쉘코드를 미리 재배열하면 해결된다.

오직 0x30 - 0x7e 사이의 값을 가지는 바이트로 쉘코드를 작성하면 문제를 풀 수 있을 것이다.

## 플래그

획득 실패