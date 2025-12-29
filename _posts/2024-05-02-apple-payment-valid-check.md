---
layout: post
title: "NodeJS 서버에서 애플 인앱결제 유효성 검증을 하는 방법"
description: "여기저기서 검색해본 결과 이 방법이 가장 최신 방법입니다"
date: 2024-05-02
feature_image: /images/default-thumbnail.jpg
author: "김민석"
categories: [Data and Api]
tags: [nodejs,apple,인앱결제,ios]
---
- 지난 시간에 구글 안드로이드 인앱결제 유효성 검증을 알아봤습니다.
- 오늘은 애플 아이폰용 앱에서 인앱결제를 했을 경우에, 결제정보의 유효성 검증을 알아보겠습니다.
- 2024년 5월 현재, 지금 소개하는 방법은 사용가능한 것입니다.
- 사전에 처리해야 하는 과정은 생략할게요, 그 부분은 다른데서 검색하셔도 됩니다.
- 저는 iap 패키지를 이용했습니다.

```javascript
const iap = require('iap')

const platform = 'apple';
const payment = {
    receipt: "애플로부터 받은 pay receipt",
    productId: "애플에 등록해둔 상품ID",
    packageName: '앱 패키지 네임',
    excludeOldTransactions: true,
};
try {
    const resp = await new Promise((resolve, reject) => {
        iap.verifyPayment(platform, payment, (err, response) => {
            if (err) {
                reject(err)
            }
            resolve(response)
        })
    })
    if (resp.transactionId === "애플에서 보내온 결제ID") {
        return true
    }
} catch (e) {
    console.error(e)
}
```

- secret을 넣으라고 되어 있는 글들이 있던데요, 제가 확인한 바로는 오히려 에러가 납니다.
- iap 패키지의 함수가 async/await을 지원하지 않아서 직접 구현했습니다.