---
layout: post
title: "주소를 PNU 코드로 변환해봅시다"
description: "지번 주소를 PNU 코드로 변환해 보겠습니다"
date: 2022-08-15
author: "김민석"
categories: [Data and Api]
tags: [address,api,pnu]
---
PNU(필지고유번호)라는 것이 있습니다. 
우리가 살고 있는 곳의 주소를 숫자로만 이루어진 코드로 표현하는 방식 인데요.
정부에서 제공하는 GIS OPEN API를 사용하다보면 이 코드를 이용해야 하는 경우가 많습니다.

예를들어 아래와 같은 데이터가 그러한데요.

[국토교통부_토지이용계획정보서비스](https://www.data.go.kr/data/15056930/openapi.do)

내가 살고 있는 곳이 주거지역인지 상업지역인지 등의 토지용도를 알아내려고 할 때 요청값으로 PNU코드를 사용해야 합니다. 
위 링크의 REST Request Parameter를 봐보시면 알겠지만, 요청변수에 지번주소는 존재하지 않아요.
지번주소를 PNU 코드로 변환해서 보내줘야 결과를 얻을 수 있습니다.

그런데 이 PNU 코드는 아래와 같은 규칙으로 정해집니다.

```
광역시도코드(2자리) + 시/군/구 코드(3자리) + 읍/면/동 코드(3자리) + 
리 코드(2자리) + 토지/임야 코드(1자리) + 
본번 코드(4자리) + 부번 코드(4자리)
``` 

예를들어 서울특별시 중랑구 상봉동 126-39을 PNU 코드로 바꿔보면요
- 광역시도 코드는 서울이니까 : 11
- 시군구 코드는 중랑구니까 : 260
- 읍면동 코드는 상봉동이니까 : 102
- 리 코드는 없으니까 : 00
- 토지니까 : 1 ('산' 이 붙는 주소의 경우 임야라서 2가 붙습니다)
- 본번은 4자리여야 하니까 앞에 0을 붙여서 : 0126
- 부번도 4자리여야 하니까 앞에 00을 붙여서 : 0039
- 이렇게 해서 전체코드는 : 1126010200101260039 입니다.

주소를 PNU 코드로 입력하려면 적어도 리까지는 맵타입이던지 Nested Object 데이터가 있어야 하겠죠?
그때 쓰면 좋을 시료 파일을 공유해봅니다. 2022년 4월 버젼이에요. 4만줄이 넘는 파일인데 중간에 "폐지"라고 
쓰여져 있는 부분은 사용안하는 부분 입니다.

<div class="kakao-adfit-content">
    <a href="https://link.coupang.com/a/bmKWqB" onclick="showCode()" target="_blank" referrerpolicy="unsafe-url"><img src="https://image13.coupangcdn.com/image/affiliate/event/promotion/2024/01/02/d5891507add7003701108894118c8393.png" alt=""></a>
    <div style="font-size: 9pt; color: #838383">"이 포스팅은 쿠팡 파트너스 활동의 일환으로, 이에 따른 일정액의 수수료를 제공받습니다."</div>
</div>

- [PNU 코드 리스트 파일](https://reddol18.github.io/dev5min/images/20220815/1/pnus.txt)


