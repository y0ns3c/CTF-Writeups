# Problem description

> We do have the encrypted data, the program they used to generate a secure password, and the bash history. Maybe you can help us out?
>
> Note: Timestamps are in GMT-04:00 format

주어진 파일
- evidence.zip
  - data.zip (암호로 잠김)
  - .bash_history
  - passwordgen.py

---

## Writeup 작성자

- JHH20

---

## 풀이

#### 접근법은 알겠으나 플래그 획득 실패

`.bash_history`를 통해 data.zip은 `passwordgen.py`가 생성한 암호로 잠겨있음을 알 수 있다
> 즉, 동일한 출력을 재현할 수 있으면 data.zip의 압축을 풀 수 있을 것이다

`passwordgen.py`는 Random의 기본 생성자로 객체를 만들기 때문에 PRNG의 seed는 다음과 같이 주어진다
```python
self.seed = round(int(time.time() * (10 ** 5)))
```

그러므로 `passwordgen.py`의 Random 객체의 seed를 `.bash_history`에 나온 시간을 Unix time으로 변환하고 10^5를 곱해 반올림한 값으로 고정하고 동일게 `python3 passwordgen.py 16`으로 실행시키면 답이 나올거라 생각했다

## 플래그

획득 실패