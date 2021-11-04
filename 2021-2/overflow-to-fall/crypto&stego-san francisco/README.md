# Problem description

> Never leave your router unprotected. Especially in San Francisco

주어진 파일
- running-config

* Writeup을 늦게 작성했기 때문에 문제 복원이 안 된 일부가 있을 수 있음

---

## Writeup 작성자

- JHH20

---

## 풀이

* 여럿이서 풀었기 때문에 생략된 과정이 있을 수 있음

`running-config` 파일에서 비밀번호가 어떤 프로토콜에 따라 plaintext로 저장되어 있음
> `enable password 7 0211570F003919704B405A0B0`

구글 검색을 통해 라우터 매뉴얼을 찾음
- https://www.cisco.com/c/en/us/support/docs/smb/switches/cisco-small-business-300-series-managed-switches/smb5563-configure-password-settings-on-a-switch-through-the-command.html#enable

해당 프로토콜로 암호화된 암호 해독방법을 검색해서 해독
- https://www.firewall.cx/cisco-technical-knowledgebase/cisco-routers/358-cisco-type7-password-crack.html

## 플래그

O2F{w34k_v1gn3re}