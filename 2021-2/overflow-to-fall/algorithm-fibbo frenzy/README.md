# Problem description

> Write an algorithm that calculates the fibonacci sequence for Fn = Fn-1 + Fn-2, where N is 1000,<br>
> and the starting sequence is F0 = 0, and F1 = 1. Sum each number that is prime within the fibonnaci sequence.
>
> The answer is O2F{number}

---

## Writeup 작성자

- JHH20

---

## 풀이

N = 1000 까지의 피보나치 수를 다 구해야 하니까 재귀함수로 각 원소를 구하기보다 배열에 저장하면서 구하는 게 더 효율적이다

#### 피보나치 수 구하기

python3
```python
def gen_fibbo(terms):
    output = [0, 1]
    for n in range(2, terms):
        output.append(output[n - 1] + output[n - 2])
    return output

fibbo = gen_fibbo(1000)
```

#### 소수 필터링

`pycryptodome` 라이브러리를 사용한다

```python
from Crypto.Util.number import isPrime

sum = 0
for fib in fibbo:
    if isPrime(fib):
        sum += fib

print(sum)
```

## 플래그

O2F{132725674935014129884681801561570257444232919795125324970917377000488365086871380952521159138505357911319846367559249240}