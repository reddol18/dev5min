---
layout: post
title: "IntelliJ Idea Remote Development 사용시 한글 타이핑 거꾸로 입력되는 문제 해결"
description: "원격 개발 IDE에서 한글 타이핑이 거꾸로 되는 문제를 해결해봅시다"
date: 2024-01-23
author: "김민석"
categories: [Others]
tags: [intellij,jetbrains,korean,typing]
---
- IntelliJ Idea Remote Development 에서 한글을 입력하면 거꾸로 입력되는 현상 때문에 고생을 했었습니다.
- 예를들어 저는 "우리말"이라고 입력했는데, 에디터에는 "말리우"라고 나타나 있는것이죠.
- 상황이 아래 처럼 발생합니다.
  - ![Alt text](https://reddol18.github.io/dev5min/images/20240123/problem_ide.png)

- 플러그인도 깔아보고 OS의 한글 세팅이 문제인지 이것저것 조치를 해보았지만 해결되지 않았었는데요.
- 저와 같은 문제를 보고한 유저가 있었더라구요.
  - [Order of Korean hieroglyphs is broken with very fast typing](https://youtrack.jetbrains.com/issue/GTW-5972/Order-of-Korean-hieroglyphs-is-broken-with-very-fast-typing)


### 해결방법

- 해결방법은 너무 간단한데요... IDE를 업데이트 하는 겁니다.
- 여기서 중요한건 본체가 되는 Intellij IDE가 아니라 원격에 깔려있는 Intellij IDE를 업데이트 해야 한다는 점 인데요.
- 방법은 아래와 같습니다.
  - 먼저 점3개 버튼을 클릭하고 Select Diffrent IDE...을 클릭하세요. 참고로 위에 체크되어 있는건 현재 사용중인 버젼입니다.
    - ![Alt text](https://reddol18.github.io/dev5min/images/20240123/image1.png)
  - 그럼 아래와 같은 화면이 나오는데, 여기서 최신버전을 설치해주세요.
    - ![Alt text](https://reddol18.github.io/dev5min/images/20240123/image2.png)
  - 만약 과거 버전을 지우고 싶다면? 아래와 같이 설정버튼을 클릭하고, Manage IDE Backends...을 클릭하세요.
    - ![Alt text](https://reddol18.github.io/dev5min/images/20240123/image3.png)
  - 그런 다음 삭제하고 싶은 버전의 X 버튼을 클릭하면 됩니다.
    - ![Alt text](https://reddol18.github.io/dev5min/images/20240123/image4.png)
- 최신 버전으로 설치하니까 한글입력이 잘 됩니다. 이로인해 생산성이 많이 향상되었습니다.
  