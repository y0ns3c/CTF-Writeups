# Problem description

드림이의 VM이 해킹당했어요! 나쁜 해커가 채굴을 위해 입력한 플래그를 찾아주세요!

주어진 파일
- bzImage
- rootfs.ext2
- run.sh

---

## Writeup 작성자

- JHH20

---

## 풀이


#### 챌린지 관련 파일 찾기

먼저 rootfs.ext2를 mount해서 챌린지 파일을 추출한다.

`mkdir -p mnt && sudo mount rootfs.ext2 mnt`

그 다음 `find` 로 실행권한이 있는 파일을 찾아보면 `mnt/home/ubuntu/.helper` 파일을 찾을 수 있다.  
이 파일을 추출해서 IDA로 분석하면 `execve("/usr/bin/sl", ?, NULL)` 을 호출하는 것을 볼 수 있다.

`mnt/usr/bin/sl` 도 같이 추출해주면 준비 끝.  
`sudo umount mnt` 로 파일 시스템은 unmount하자.

#### 첫 파일 분석

`.helper` 를 IDA로 분석하면 다음과 같이 나온다.
```c
__int64 __fastcall main(int argc, char **argv, char **envp)
{
    char *buf[3]; // [rsp+10h] [rbp-20h] BYREF
    unsigned __int64 __canary; // [rsp+28h] [rbp-8h]

    __canary = __readfsqword(0x28u);
    if ( argc != 2 )
        exit(0);

    if ( strcmp(argv[1], "MINING_BOOST") )
        exit(0);

    read(0, &unk_4040, 64uLL);
    buf[0] = "[kworker]";
    buf[1] = (char *)&unk_4040;
    buf[2] = 0LL;
    execve("/usr/bin/sl", buf, 0LL);
    return 0LL;
}
```

프로그램 인자를 1개 받아서 "MINING_BOOST"와의 일치여부를 확인한다.

다음에는 사용자로부터 64바이트를 받아 .bss 영역의 버퍼에 저장하고 다음과 같이 `/usr/bin/sl`을 실행한다.

```c
execve("/usr/bin/sl", [
    "[kworker]",                            // argv[0]
    [사용자로부터 받은 64바이트의 데이터],     // argv[1]
    0
], NULL)
```

#### 두 번째 파일 분석

`/usr/bin/sl` 을 IDA로 분석하면 다음과 같이 나온다.

```c
void __fastcall __noreturn main(int argc, char **argv, char **envp)
{
    int i; // [rsp+1Ch] [rbp-14h]
    int j; // [rsp+20h] [rbp-10h]
    int k; // [rsp+24h] [rbp-Ch]
    __int64 sum; // [rsp+28h] [rbp-8h]

    // Stage 1 - 해설을 위해 코드를 나눔
    for ( i = 0; i <= 35; ++i )
    {
        chArr[i] = (__int64 *)calloc(1uLL, 32uLL);
        *(_BYTE *)chArr[i] = argv[1][i];
    }

    // Stage 2 - 해설을 위해 코드를 나눔
    for ( j = 0; j <= 35; ++j )
    {
        sum = 0LL;
        for ( k = 0; k <= j; ++k )
            sum += *chArr[k] * qword_4020[k];

        qword_4280[j] = sum;
        if ( qword_4280[j] != qword_4140[j] )
        {
            puts("who are u?");
            exit(-1);
        }
    }
    puts("ok I know you!");
    loop();
}
```

###### Stage 1을 분석해보자.

`chArr`는 동적할당으로 반환된 `int *` 36개를 담는 배열이다.  
argv[1]은 사용자의 입력값이 담긴 배열이다.

각 원소의 공간에는 사용자의 입력값이 1바이트씩 저장된다.  
즉, 사용자의 입력값을 바이트 단위로 `char` -> `int` 변환한 것이다.

###### Stage 2를 분석해보자.

`chArr[k]`는 사용자의 입력값이다.  
`qword_4020`은 어느 `long[]` 전역변수이다.  
`qword_4140`은 어느 `long[]` 전역변수이다.  
`qword_4280`은 어느 `long[]` 전역변수이다.

코드를 조금 정리해보면 다음과 같이 줄일 수 있다.

```c
long sum = 0;
for ( j = 0; j <= 35; ++j )
{
    sum += *chArr[j] * qword_4020[j];
    if ( sum != qword_4140[j] )
    {
        puts("who are u?");
        exit(-1);
    }
}
```

사용자 입력값을 1바이트씩 어느 64비트 정수와 곱한 결과가 기대값과 일치하는지를 검사할 뿐이다. 이 검사를 통과시키는 사용자 입력값이 바로 플래그가 된다.

#### 플래그 획득하기

Stage 2의 코드를 아래와 같이 역산하면 필요한 사용자 입력값을 얻을 수 있다.

```c
long flag[36];
long prev = 0;
for ( j = 0; j <= 35; ++j)
{
    if (j > 0) prev = qword_4140[j - 1];
    long target = qword_4140[j] - prev;
    flag[j] = target / qword_4020[j];
}
```

`pwntools`로 `/usr/bin/sl` 파일에서 필요한 전역변수 데이터를 추출하고 플래그를 계산하는 코드는 [sol.py](sol.py) 파일을 참고.

## Flag

DH{7aa4cfea30020841179787e66b91ce63}