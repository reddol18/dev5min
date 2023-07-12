---
layout: post
title: "AWS RDS AURORA 파라미터 그룹 적용안될 때"
description: "파라미터 그룹을 새로 만들었는데 적용이 안될 때"
date: 2023-07-12
author: "김민석"
categories: [Others]
tags: [aws,rds,parameter_group,reboot]
---
## 문제사항
- AWS RDS AURORA 서비스를 이용중에 있습니다.
- 그런데 interactive_timeout 값을 디폴트로 사용하니까, 프로세스 들이 너무 오래 살아 있게 되었어요.
- 이 문제를 해결하고자 parameter group을 새로 생성하고, interactive_timeout 값을 300초로 줄여서 적용하려고 했어요.
- ![image](https://github.com/reddol18/dev5min/assets/15623847/bfd0e7be-8229-4374-b478-af519e04d3e6)
- 분명히 AWS 공식 설명서에 dynamic 타입 밸류는 DB를 재부팅 하지 않아도 된다고 나와있는데...
- 값이 바뀌지 않았어요 ㅠㅠ
- ![image](https://github.com/reddol18/dev5min/assets/15623847/2bc57e2c-79b2-48b6-af08-2da74bd494e5)

{% include adfit2.html %}

## 해결책
- 데이터베이스 구성 탭을 보니까 아래처럼, 재부팅 보류중으로 되어 있고 변경된 파라미터 그룹이 적용되지 않고 있었어요.
- ![image](https://github.com/reddol18/dev5min/assets/15623847/d942909b-4f53-47d6-b091-f5aa2c36b903)
- 아무래도 바꾸지 않은 값중에 static 타입 밸류가 있어서 그런건가 봅니다. 어쩔 수 없이 재부팅해야 하네요.
- ![image](https://github.com/reddol18/dev5min/assets/15623847/91af64a9-6272-475e-aa41-27c76ace1a97)
- READ/WRITE 인스턴스 둘 다 재부팅 했구요. 재부팅이 그리 오래 걸리지 않네요.
- 값이 변경된 것을 확인할 수 있습니다.
- ![image](https://github.com/reddol18/dev5min/assets/15623847/9e1c29f8-9119-4347-9db3-3750d50395d9)
