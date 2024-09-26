---
layout: post
title: "AWS API-GATEWAY에서 우리쪽 서버가 발생시킨 에러코드를 그대로 전달하는 방법"
description: "생각보다 방법이 간단합니다."
date: 2024-06-05
author: "김민석"
categories: [Data and Api]
tags: [api-gateway,proxy,error-code]
---
- API-GATEWAY를 사용하다 보면 에러 응답 코드라던가, 응답 형식 등을 JSON으로 규정할 수 있음을 알 수 있습니다.
- 이러다 보니까 우리가 사용하고 있는 에러 응답 코드들을 일일이 JSON으로 다 정의해서 올려야 하는건가? 하고 의구심이 들텐데요.
  - 안정적이고 다양한 확장 가능성이 있는 "좋은" 방법입니다만, "효율적"인 방법인지는 잘 모르겠네요.
  - 왜냐면 AWS가 제공하는 대시보드 전반의 불편한 UI 때문에, 이러한 JSON 입력도 상당히 까다롭기 때문입니다.
  - 저는 그래서 간단하게 PROXY만 제공하고 싶다면 아래와 같은 방법을 추천합니다.

{% include adfit2.html %}    

- 먼저 해당하는 메소드에서 통합요청탭의 편집 버튼을 클릭해주세요.
    - ![alt text](https://reddol18.github.io/dev5min/images/20240605/image1.png)
- 그런다음 아래처럼 HTTP 프록시 통합을 체크하면 끝!
    - ![alt text](https://reddol18.github.io/dev5min/images/20240605/image2.png)
