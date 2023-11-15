---
layout: post
title: "딥러닝 기반 사진 성별 판독 라이브러리의 정확도 비교"
description: "파이썬기반 사진 성별 판독 라이브러리의 정확도를 비교해 봤습니다"
date: 2023-11-01
author: "김민석"
categories: [ComputerVision]
tags: [deeplearning,ai,insightface,keras,caffe,gender_detection]
---
- 사람의 얼굴이 들어간 사진을 입력하면 성별을 판독해주는 라이브러리들이 있죠.
- 그런데 이런 라이브러리들이 대체로 동양인에 대한 정확도가 떨어진다고 합니다.
- 성별 판독 뿐만 아니라 전반적인 얼굴관련 이미지 처리들이 그런것 같아요.
- 그래서 github에서 star를 많이 받은 3개의 라이브러리를 가지고 테스트를 진행해 봤습니다.
- 테스트에 사용한 사진은 20대 남/여 사진 100여개를 이용했습니다.
- 보통 이러한 라이브러리들의 만들어내는 결과값은, 1개의 얼굴이 있지만 여러개가 있다고 판단하는 경우가 있습니다.
- 또한 아예 얼굴을 찾아내지 못하는 경우도 있구요. 이런 2가지 케이스는 테스트수에서 뺐습니다.
- 그렇기 때문에 실제 판독 정확성은 더 떨어진다고 보는게 맞습니다.

### Gender Detection Keras
- https://github.com/arunponnusamy/gender-detection-keras
- keras 기반 라이브러리 입니다.
- 속도는 제일 느린듯 하구요.
- 여성 71/92
- 남성 51/93
- 제일 정확도가 떨어지네요

### Gender and Age Detection
- https://github.com/smahesh29/Gender-and-Age-Detection
- Caffe 플랫폼 기반입니다.
- 속도 빠릅니다.
- 여성의 경우 위에 것보다 1명으로 판독하는 정확도가 높습니다.
- 여성 82/104
- 남성 67/90
- 1명을 판독 성공했을 때 정확도는 위에것보다 높습니다.

### Insightface
- https://github.com/deepinsight/insightface
- 제일 유명한 라이브러리죠.
- 이것도 Caffe 플랫폼 기반으로 보입니다.
- 역시 속도 빠르구요.
- 여성 138/149
- 남성 83/104
- 여성의 경우 거의 정확한 반면, 남성은 상대적으로 부정확합니다.
- 그래도 위의 2개보다는 남성이 제일 정확합니다.

