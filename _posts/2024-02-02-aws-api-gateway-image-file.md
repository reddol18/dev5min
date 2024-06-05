---
layout: post
title: "AWS API-GATEWAY에서 이미지 파일을 읽어보자"
description: "프록시 서버로부터 전달되는 이진형식의 이미지 파일을 읽을 수 있는 방법을 소개합니다"
date: 2024-02-02
author: "김민석"
categories: [Data and Api]
tags: [aws,apigateway,binary,png,image]
---
- API-GATEWAY를 통해서 Rest API를 구현할 경우 기본적으로 텍스트 형태의 반응값을 받게 됩니다.
- 그런데 프록시 서버등을 통해서 이미지 파일을 그대로 전달받는 경우, 결과가 이진(BINARY) 데이터여야만 하죠
- 이럴 때 설정을 어떻게 하는지 소개해보고자 합니다.
- 먼저 API 설정 메뉴로 가주세요.

![STEP1](https://reddol18.github.io/dev5min/images/20240202/1.png)

- 거기서 이진 미디어 유형 관리를 선택해주세요. 그런 다음 아래처럼 image/png를 입력해주세요.

![STEP2](https://reddol18.github.io/dev5min/images/20240202/2.png)

- 그런 다음에 해당 리소스 상의 메소드에서 "메서드 응답" 탭으로 이동합니다. 편집을 클릭해서 아래와 같이 입력합니다.
  - 이렇게 Content-Type을 설정해 줘야 합니다.

![STEP3](https://reddol18.github.io/dev5min/images/20240202/3.png)

- 마지막으로 "통합 응답" 택에서 편집을 클릭해주세요.
  - 콘텐츠 처리를 "이진으로 변환"으로 지정하고
  - 아까 입력한 Content-Type을 'image/png'로 입력해주세요. 여기서 중요한 점은 작은따옴표를 함께 입력한다는 점 입니다.

![STEP4](https://reddol18.github.io/dev5min/images/20240202/4.png)

- 그러면 이미지가 온전히 전달되는 것을 확인 할 수 있습니다.

![STEP5](https://reddol18.github.io/dev5min/images/20240202/5.png)

- 제대로 설정이 되지 않으면 `{"message": "Internal server error"}`가 출력된다던가, 이진 파일이 텍스트로 출력되는 결과가 나타날수도 있으니 위 과정을 그대로 따라해주세요.