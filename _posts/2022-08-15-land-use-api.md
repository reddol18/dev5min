---
layout: post
title: "PNU 코드를 이용해서 토지이용계획 확인하기"
description: "정부공공데이터 API에서 PNU 코드를 이용해서 토지이용계획(주거지역 등)을 알아보겠습니다"
date: 2022-08-15
author: "김민석"
categories: [Data and Api]
tags: [address,api,pnu,data.go.kr,landuse]
---
지번주소를 PNU 코드로 바꾸는 것에 관한 내용은 아래 링크 참고해주세요.

[주소를 PNU 코드로 변환해봅시다](make-pnu-code)

오늘은 PNU 코드를 이용해서 국토교통부 토지이용계획정보서비스 API에 요청을 보내고
해당 필지의 토지이용계획정보를 얻어와 보겠습니다.

[국토교통부_토지이용계획정보서비스](https://www.data.go.kr/data/15056930/openapi.do)

토지이용계획은 굉장히 다양한 정보를 담고 있습니다.
예를들어 해당 필지가 상업지역이면서 대공방어협조구역 일 수도 있고 재정비촉진지구 일 수 도 있어요.
즉, API 정보를 보내면 필드가 1개만 있는게 아니라 배열로 반환된다는 점 입니다.

아래는 저희 동네에 있는 어떤 시설의 결과 값을 API로 요청해서 받은것 입니다. 
JSON 내용을 봐보면 배열에 담겨 있는 것을 확인할 수 있죠? 
이점 참고해서 데이터를 가공하거나 사용하시면 되겠습니다.
{% include more_front.html %}
```JSON
{
  "landUses": {
    "field": [
      {
        "regstrSeCode": "1",
        "pnu": "1126010200100830008",
        "lastUpdtDt": "2022-07-14",
        "manageNo": "15000001126020000000UQA01X0001001",
        "ldCode": "1126010200",
        "ldCodeNm": "서울특별시 중랑구 상봉동",
        "mnnmSlno": "83-8",
        "regstrSeCodeNm": "토지대장",
        "cnflcAt": "1",
        "cnflcAtNm": "포함",
        "prposAreaDstrcCode": "UQA01X",
        "prposAreaDstrcCodeNm": "도시지역",
        "registDt": "2017-09-05"
      },
      {
        "regstrSeCode": "1",
        "pnu": "1126010200100830008",
        "lastUpdtDt": "2022-07-14",
        "manageNo": "15000001126020000000UQA2200017017",
        "ldCode": "1126010200",
        "ldCodeNm": "서울특별시 중랑구 상봉동",
        "mnnmSlno": "83-8",
        "regstrSeCodeNm": "토지대장",
        "cnflcAt": "1",
        "cnflcAtNm": "포함",
        "prposAreaDstrcCode": "UQA220",
        "prposAreaDstrcCodeNm": "일반상업지역",
        "registDt": "2017-09-05"
      },
      {
        "regstrSeCode": "1",
        "pnu": "1126010200100830008",
        "lastUpdtDt": "2022-07-14",
        "manageNo": "15000001126020090001UBA1000001001",
        "ldCode": "1126010200",
        "ldCodeNm": "서울특별시 중랑구 상봉동",
        "mnnmSlno": "83-8",
        "regstrSeCodeNm": "토지대장",
        "cnflcAt": "1",
        "cnflcAtNm": "포함",
        "prposAreaDstrcCode": "UBA100",
        "prposAreaDstrcCodeNm": "과밀억제권역",
        "registDt": "2017-09-05"
      },
      {
        "regstrSeCode": "1",
        "pnu": "1126010200100830008",
        "lastUpdtDt": "2022-07-14",
        "manageNo": "15800001126020192019UNE2000001003",
        "ldCode": "1126010200",
        "ldCodeNm": "서울특별시 중랑구 상봉동",
        "mnnmSlno": "83-8",
        "regstrSeCodeNm": "토지대장",
        "cnflcAt": "1",
        "cnflcAtNm": "포함",
        "prposAreaDstrcCode": "UNE200",
        "prposAreaDstrcCodeNm": "대공방어협조구역",
        "registDt": "2019-07-01"
      },
      {
        "regstrSeCode": "1",
        "pnu": "1126010200100830008",
        "lastUpdtDt": "2022-07-14",
        "manageNo": "30600001126020110009UMZ1000001001",
        "ldCode": "1126010200",
        "ldCodeNm": "서울특별시 중랑구 상봉동",
        "mnnmSlno": "83-8",
        "regstrSeCodeNm": "토지대장",
        "cnflcAt": "1",
        "cnflcAtNm": "포함",
        "prposAreaDstrcCode": "UMZ100",
        "prposAreaDstrcCodeNm": "가축사육제한구역",
        "registDt": "2017-09-05"
      },
      {
        "regstrSeCode": "1",
        "pnu": "1126010200100830008",
        "lastUpdtDt": "2022-07-14",
        "manageNo": "30600001126020190027ZA00130001001",
        "ldCode": "1126010200",
        "ldCodeNm": "서울특별시 중랑구 상봉동",
        "mnnmSlno": "83-8",
        "regstrSeCodeNm": "토지대장",
        "cnflcAt": "2",
        "cnflcAtNm": "저촉",
        "prposAreaDstrcCode": "ZA0013",
        "prposAreaDstrcCodeNm": "건축선",
        "registDt": "2019-11-21"
      },
      {
        "regstrSeCode": "1",
        "pnu": "1126010200100830008",
        "lastUpdtDt": "2022-07-14",
        "manageNo": "61100001126020150099UDA1000003001",
        "ldCode": "1126010200",
        "ldCodeNm": "서울특별시 중랑구 상봉동",
        "mnnmSlno": "83-8",
        "regstrSeCodeNm": "토지대장",
        "cnflcAt": "1",
        "cnflcAtNm": "포함",
        "prposAreaDstrcCode": "UDA100",
        "prposAreaDstrcCodeNm": "재정비촉진지구",
        "registDt": "2017-09-05"
      },
      {
        "regstrSeCode": "1",
        "pnu": "1126010200100830008",
        "lastUpdtDt": "2022-07-14",
        "manageNo": "61100001126020170174UQS1160001001",
        "ldCode": "1126010200",
        "ldCodeNm": "서울특별시 중랑구 상봉동",
        "mnnmSlno": "83-8",
        "regstrSeCodeNm": "토지대장",
        "cnflcAt": "2",
        "cnflcAtNm": "저촉",
        "prposAreaDstrcCode": "UQS116",
        "prposAreaDstrcCodeNm": "대로3류(폭 25m~30m)",
        "registDt": "2017-09-05"
      },
      {
        "regstrSeCode": "1",
        "pnu": "1126010200100830008",
        "lastUpdtDt": "2022-07-14",
        "manageNo": "61100001126020170402UDA1000001001",
        "ldCode": "1126010200",
        "ldCodeNm": "서울특별시 중랑구 상봉동",
        "mnnmSlno": "83-8",
        "regstrSeCodeNm": "토지대장",
        "cnflcAt": "1",
        "cnflcAtNm": "포함",
        "prposAreaDstrcCode": "UDA100",
        "prposAreaDstrcCodeNm": "재정비촉진지구",
        "registDt": "2017-12-06"
      },
      {
        "regstrSeCode": "1",
        "pnu": "1126010200100830008",
        "lastUpdtDt": "2022-07-14",
        "manageNo": "61100001126020170402UQQ3000001001",
        "ldCode": "1126010200",
        "ldCodeNm": "서울특별시 중랑구 상봉동",
        "mnnmSlno": "83-8",
        "regstrSeCodeNm": "토지대장",
        "cnflcAt": "1",
        "cnflcAtNm": "포함",
        "prposAreaDstrcCode": "UQQ300",
        "prposAreaDstrcCodeNm": "지구단위계획구역",
        "registDt": "2017-12-06"
      }
    ],
    "totalCount": "10",
    "numOfRows": "10",
    "pageNo": "1",
    "resultCode": null,
    "resultMsg": null
  }
}
```
{% include more_tail.html %}