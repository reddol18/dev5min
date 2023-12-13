---
layout: post
title: "API Gateway 대시보드 사용중 갑자기 뜬 Network Failure???"
description: "API Gateway를 이용하기 위해 정보수정을 하고 저장을 눌렀는데 Network Failure가 떠서 당황하셨나요? 그 해결책을 고민해 봅니다."
date: 2023-12-13
author: "김민석"
categories: [Data&Api]
tags: [aws,apigateway,networkfailure]
---
- 저희 회사는 서비스 부하분산과 API 버젼관리를 위해서 AWS의 API-Gateway를 사용하고 있는데요.
- 대시보드가 좀 엉성하지만, 그래도 테스트도 해볼 수 있고 필요한 기능은 다 있어서 잘 쓰고 있었습니다.
- 그런데 어느날 새로운 메써드를 만들고 저장을 하려고 하는데 `Network Failure` 메시지가 계속 뜨면서 저장이 안되는거에요.

 {% include adfit.html %}

### 문제는 크롬 CORS 익스텐션
- 정확한 이유는 모르겠지만 추정컨데 크롬에 설치한 CORS 익스텐션이 문제를 일으킨 것 같습니다.
- 해당 익스텐션을 비활성화 시키니까 문제가 해결되었어요.
- 그러고나서 다시 활성화 시키면 또 저장이 되네요...