---
layout: post
title: "지라(JIRA)에서 Github Repository 연동하기 왜 안되는거야??"
description: "지라(JIRA)의 Github APP에서 내가 원하는 Repository를 추가하는 방법을 알아봤습니다"
date: 2023-11-17
author: "김민석"
categories: [Others]
tags: [jira,github,commit]
---
- 저희 팀은 협업툴로 지라(JIRA)를 사용하고 있습니다.
- 그런데 기존에 형상관리는 github을 이용하고 있었고, 앞으로도 바꿀 생각이 없어요.
- 그러다보니 JIRA와 Github을 연동시켜야 했는데요...
    ![Alt text](https://reddol18.github.io/dev5min/images/jira1.png)
- 그런데 위에서 처럼 백날 추가를 클릭해도 안되는거에요. 아래와 같은 에러만 나옵니다.
    ![Alt text](https://reddol18.github.io/dev5min/images/jira2.png)
- 다른 팀원들은 잘만 하던데, 왜 나는 안되는걸까? 고민하던 중...

{% include adfit2.html %}

- 방법을 알아냈습니다.
- 바로 커밋 메시지에 내가 작업하고 있는 지라 이슈이름만 입력해주면 자동으로 추가되는 거였습니다.
- 예를들어 이슈이름이 ILLUA-156 이면 아래와 같은 커밋 메시지를 입력해 주면 됩니다.
    ![Alt text](https://reddol18.github.io/dev5min/images/image.png)

```
ILLUA-156 연동되라 뿅!
제발~
```

- 그리고 코드 페이지로 가보면 자동으로 추가되어 있을겁니다.
    ![Alt text](https://reddol18.github.io/dev5min/images/image-1.png)