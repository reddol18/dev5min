---
layout: post
title: "NodeJS 서버에서 안드로이드 인앱결제 유효성 검증을 하는 방법"
description: "여기저기서 검색해본 결과 이 방법이 가장 최신 방법입니다"
date: 2024-04-30
author: "김민석"
categories: [Data and Api]
tags: [nodejs,google,googleapis,인앱결제,안드로이드]
---
- 구글 안드로이드용 앱에서 인앱결제를 했을 경우에, 결제정보가 리턴되는데요.
- 리턴된 값이 제대로된 값인지 혹시 위조된 것은 아닌지 검증할 필요가 있습니다.
- 제가 여기저기 검색을 해본 결과, 안되는 내용을 올려놓은 포스팅들이 있더군요.
- 2024년 4월 현재, 지금 소개하는 방법은 사용가능한 것입니다.

{% include adfit2.html %}    

- 사전에 처리해야 하는 과정은 생략할게요, 그 부분은 다른데서 검색하셔도 됩니다.
- 서비스계정 만들고, 플레이스토어에서 계정 연동 시키는 등의 과정은 같아요.

```javascript
const {google} = require('googleapis')
const path = require('path')

// 서비스 계정 만들면서 다운로드 받은 json 파일이 필요합니다
const realPath = path.join(__dirname, '../XXXXXXX.json')
const auth = new google.auth.JWT(
    "서비스계정 이메일 주소",
    null,
    require(realPath).private_key,
    // 아래 scopes 꼭 지정해야 하구요
    ['https://www.googleapis.com/auth/androidpublisher'],
    null
)

google.options({auth: auth})

const iap = google.androidpublisher('v3')
const packageName = "앱의 패키지 네임이 들어갑니다"
try {
    const resp = await iap.purchases.products.get({
        packageName: packageName,
        productId: "플레이스토어에서 등록한 상품ID",
        token: "검증하고자 하는 결제 정보의 purchaseToken 값",
    })
    if (resp.data.orderId === "결제ID") {
        // 올바른 결제 정보
    }
} catch (e) {
    console.error(e)
}
```