---
layout: post
title: "구글 애드몹(GOOGLE ADMOB) 광고의 app-ads.txt 연결하기"
description: "github 블로그에 app-ads.txt 올리고 애드몹에서 확인할 수 있게 하는 방법을 설명합니다."
date: 2023-05-18
author: "김민석"
categories: [Data and Api]
tags: [admob,app-ads]
---
- 개발한 앱에 애드몹 광고를 달았어요. 아래처럼 광고는 잘 나옵니다. 그런데 애드몹에서 메시지를 보내왔어요.
  - ![image](https://github.com/reddol18/dev5min/assets/15623847/06f1d9eb-1400-4255-8297-2b59f62348b3)
- 플레이 스토어에서 앱정보에 올린 URL에 app-ads.txt를 올려야 한다네요.
  - ![image](https://github.com/reddol18/dev5min/assets/15623847/d5ac4c06-4cc8-44ab-b9ed-3dd696835ea0)
  - app-ads.txt 메뉴찾기가 좀 어려운데요, 위 화면 참고하세요.
- github io blog에 올렸더니 여전히 404 에러로 인식된다고 나옵니다.
- 자세히 보니까 reddol18.github.io/dev5min/app-ads.txt이 아니라 reddol18.github.io/app-ads.txt를 찾고있네요.
  
{% include adfit.html %}

- 어쩔수 없이 만원짜리 도메인을 하나 샀습니다. 네임서버 연결을 했구요.
  - [Github IO 블로그 DNS 설정](https://kyungyeon.dev/posts/24)
  - ![image](https://github.com/reddol18/dev5min/assets/15623847/1f3a0511-2e16-4f55-b8d5-f53ec4739b25)
  - 잘 설정되었다고 나옵니다. 그런데!
- 구입한 도메인으로 연결하니까 블로그 화면이 깨져버리네요.
  - ![image](https://github.com/reddol18/dev5min/assets/15623847/17f237b0-8e3d-4fbb-82d7-db3948590181)
  - 스타일을 불러오는 주소가 달라져서 그렇습니다. _config.yml 가서 url, baseurl 값을 바꿔줘야 합니다.
