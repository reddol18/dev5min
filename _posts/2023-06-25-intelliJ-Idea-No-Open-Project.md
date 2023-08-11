---
layout: post
title: "갑자기 IntelliJ IDEA에서 프로젝트가 안 열릴 때"
description: "어떻게 하면 프로젝트가 안 열리는 문제를 해결할 수 있는지 알아봅시다"
date: 2023-06-25
author: "김민석"
categories: [Others]
tags: [intellij,jetbrains,plugin,problem]
---
- 새 버젼 인텔리제이를 다운로드 받고 작업 프로젝트를 열려고 하는데, 아래 화면에서 안넘어 가는거에요.
  - ![image](https://reddol18.github.io/dev5min/images/20230625/image.png)
- 처음엔 라이센스 문제인 줄 알고, 라이센스도 점검해 보고 별걸 다 해봤는데도 안됩니다.
- 프로젝트를 클릭하면 잠시 화면이 뜨는가 싶더니, 바로 닫히더라구요.
- 알고보니 원인은 기존에 사용했던 플러그인과의 충돌 때문이었습니다.

- 이럴 때는 ItelliJ의 실행시 나타나는 출력 메시지를 확인해야 합니다. 아래 처럼 콘솔에서 실행하면 확인가능해요.
  - ![image](https://reddol18.github.io/dev5min/images/20230625/image-1.png)
- 지금은 에러가 다 없어졌지만 플러그인과 충돌이 나면, 해당 플러그인과 관련한 에러 메시지가 뜹니다.
  - ![image](https://reddol18.github.io/dev5min/images/20230625/image-2.png)
- 혹시 플러그인을 다시 깔면 어떻게 될까요? 그래서 한 번 다시 깔아봤습니다.
  - ![image](https://reddol18.github.io/dev5min/images/20230625/image-3.png)
- 바로 에러가 나더니 또 같은 문제가 발생하네요. 지워야 겠어요 ㅠㅠ
  - ![image](https://reddol18.github.io/dev5min/images/20230625/image-4.png)  
- 지우고 실행하면 잘 뜹니다.  
