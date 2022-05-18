# Problem description

> Oh no! My Latin teacher likes to touch type on her Dell laptop, but she has trouble keeping her fingers on the right keys in home row. The letters she's typing out don't really make sense. Can you help me understand what she's saying so she doesn't get upset when I come to her confused?
> 
> `ykvyg}pp[djp,rtpelru[pdoyopm|`

---

## Writeup 작성자

- JHH20

---

## 풀이

플래그 형식은 `tjctf{???}`이라는 것을 알고 있다. 그리고 키보드에서 손의 위치만 잘못된 상태에서 입력을 했다고 문제에서 명시하고 있다.

qwerty 키보드에서 `ykvyg}`를 1칸 오른쪽에 있는 키로 바꾸면 `tjctf{`가 된다. 마찬가지로 나머지도 전부 1칸 오른쪽에 있는 키로 바꾸어 입력하면 플래그를 획득할 수 있다.

## 플래그

tjctf{oopshomerowkeyposition}