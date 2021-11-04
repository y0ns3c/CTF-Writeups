# Problem description

> Can you guess the correct flag to recreive an invite to the club?

주어진 파일
- rev1.py

---

## Writeup 작성자

- JHH20

---

## 풀이

주어진 `rev1.py` 코드는 입력값을 받고 `verify` 함수의 변환을 거쳐 지정된 상수와 일치한지를 판별해준다

이때 일치하도록 만드는 입력값이 플래그가 된다

#### verify 함수의 입력 변환

xor 연산은 같은 값으로 두 번 하면 서로 상쇄되어 원래 값이 된다
> (a xor b) xor b == a xor (b xor b) == a

입력값 `guess`에 대해...
> guess[i] xor 199 == vals[i] 가 성립하면<br>
> guess[i] xor 199 xor 199 == vals[i] xor 199 또한 성립하고<br>
> guess[i] == vals[i] xor 199 가 된다

#### 역변환

`vals`는 소스에 주어졌으므로 각 숫자에 xor 199 연산을 하여 나온 값을 python chr() 함수로 문자로 변환해주면 플래그를 획득할 수 있다

python3
```python
sol = [chr(x ^ 199) for x in vals]
print(''.join(sol))
```

## 플래그

O2F{Xor_u_2_c00l_4_zch0o1}