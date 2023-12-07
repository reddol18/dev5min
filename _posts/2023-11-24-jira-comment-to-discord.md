---
layout: post
title: "지라(JIRA)의 자동화 기능을 이용해서 새로 달린 댓글의 멘션을 디스코드로 보내기"
description: "지라(JIRA)의 자동화와 Smart Value를 이용해서 디스코드 웹훅과 연동하는 방법입니다"
date: 2023-11-24
author: "김민석"
categories: [Others]
tags: [jira,automation,smart_value,metion,discord,webhook]
---
- 저희팀은 이슈트래커는 지라를, 메신저는 디스코드를 사용하고 있습니다.
- 누군가를 언급하는 댓글, 즉 멘션이 발생했을 때 디스코드의 특정 채널에 전달되면 바로 확인할 수 있어서 좋겠죠.
- 지라의 자동화 기능은 템플릿을 제공하는데요, 안타깝게도 멘션에 관한 것은 없습니다. 당연히 디스코드에 대응되는 것도 없구요.
- 그래서 지라의 Smart Value를 이용해서 직접 만들어 보기로 했습니다.
- 이때 두 가지 개념에 대한 이해가 필요한데요.
    - 첫째 지라에서 사용하는 accountId
    - 둘째 디스코드의 webhook
- 아래에서 차근 차근 설명해 보겠습니다.    
    
## 지라의 accountId
- 지라에서 특정 이슈에 멘션이 ``@ㅁㅁㅁㅁ 빨리 처리해주세요`` 달린 댓글을 작성하면, 아래와 같은 형식으로 저장이 됩니다.
```
[~accountId:XXXXXXXXXXXXXXXXXXXXXXXXXX] 빨리 처리해주세요
```
- 그러니까 ㅁㅁㅁㅁ 의 사용자ID인 accountId로 저장이 된다는 거에요.
- 그런데 이걸 자동화 기능에서 ``comment.body``나 ``issues.comments.last.body`` 로 가져오려고하면 저장된 형태 그대로 가져오게 됩니다.
- 디스코드에는 ㅁㅁㅁㅁ 로 표기되어야 하지만 그렇게 안된다는 거죠. 아래처럼 갑니다.
  - ![Alt text](https://reddol18.github.io/dev5min/images/20231124/image.png)
- 이걸 사용자 이름으로 바꾸려고 온갖 방법을 찾아봤지만 결국 실패했어요. ㅠㅠ
- 그래서 if 노가다로 처리했습니다. 예제 코드는 아래와 같습니다.
- ![Alt text](https://reddol18.github.io/dev5min/images/20231124/image5.png)
- 주의 하실 점은 중간에 공백문자 들어가면 오류날 수 있다는 점이에요. 아무튼 잘 도착하면 아래처럼 메시지가 전달됩니다.
![Alt text](https://reddol18.github.io/dev5min/images/20231124/image2.png)

## 디스코드의 webhook
- 물론 이 모든것은 디스코드 상에서 webhook url을 만든 다음에 수행할 수 있다는 점 잊지마세요.
- 디스코드 채널 편집 메뉴에서 연동을 선택하면, 웹후크를 만들고 수정할 수 있는 화면이 나옵니다.
![Alt text](https://reddol18.github.io/dev5min/images/20231124/image3.png)
- 웹후크 URL 복사를 통해서 확보한 URL을 지라의 자동화 메뉴에서 웹 요청전송 부분에 입력하면 됩니다.
![Alt text](https://reddol18.github.io/dev5min/images/20231124/image4.png)
