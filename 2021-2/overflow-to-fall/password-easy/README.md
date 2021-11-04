# Problem description

> Can you figure out what the original text was? 538fecccb94780103d3f68360d52d041

---

## Writeup 작성자

- JHH20

---

## 풀이

텍스트를 (16진수) 숫자로 인코딩되었다면 해시 / 암호화를 떠올릴 수 있다

그러나 비밀번호를 유추할 수 있는 힌트가 전혀 없는 것으로 보아 암호화는 아닐 거라는 것을 알 수 있다<br>
그러니 해시일 것이다

그러나 어떤 해시 알고리즘을 썼을지 모르겠으니까 구글에 의지하자
> hash analyzer 같은 검색어로 적당한 사이트를 찾는다<br>
> 예: https://www.tunnelsup.com/hash-analyzer/

이제 주어진 해시가 md5 알고리즘으로 만들어진 것을 알아냈다

인터넷에서 적당한 md5 decrypter를 찾아서 원본 텍스트를 복원한다
> 예: https://crackstation.net/

## 플래그

#dare2stealmapassword#