# Problem description

> My friend was making breakfast and accidentally scrambled the JPEG (He meant to make a sunny-side up)<br>
> Thankfully, he has photographic memory and remembers exactly how the JPEG got scrambled.<br>
> If you can unscramble the JPEG, he says he can give you a flag!<br>
> The instructions will be attached in a document.

주어진 파일
- scrambled.jpg
- instructions.txt

---

## Writeup 작성자

- JHH20

---

## 풀이

`instructions.txt`에 적힌 변환을 역순으로 실행취소하면 된다

이때 주어진 `scrambled.jpg`는 바이너리 파일로 byte 데어터를 읽어드린다
> `solver.py` 참고

## 플래그

![image](images/flag.jpg)