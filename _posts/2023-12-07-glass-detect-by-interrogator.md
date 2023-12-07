---
layout: post
title: "Interrogator를 이용해서 안경을 쓴 사람의 사진 알아내기"
description: "clip-interrogator를 이용해서 glasses detection을 해보겠습니다."
date: 2023-12-07
author: "김민석"
categories: [ComputerVision]
tags: [clip-interrogator,glasses-detection]
---
- 지난번에 clip-interrogator와 stable diffusion을 이용해서 재미난 실험을 해봤는데요.
- 오늘은 clip-interrogator을 이용해서 사진 속 사람이 안경을 썼는지 여부를 측정해 보도록 하겠습니다.
- 사실 안경을 디텍팅하는 AI 기술은 여러가지 접근법에 의해서 발표된 바가 있습니다.
- 굳이 AI가 아니어도 OpenCV등을 이용한 이미지 처리 기술로 디텍팅하는 방식도 있지요.
- 하지만 오늘은 순수하게 clip-interrogator을 이용해서 한 번 디텍팅 해보겠습니다.
- 실험 대상이 되는 사진들은 아래와 같습니다.
  - ![Alt text](https://reddol18.github.io/dev5min/images/20231207/image.png)

## 몇 가지 참고사항
- clip-interrogator는 best모드와 fast모드로 나뉘는데요. best는 조금더 정확하고 자세한 표현을 출력합니다. fast는 말그대로 빠릅니다.
- best가 fast에 비해서 5~10초 정도 더 느립니다. (GPU를 이용할 때 입니다)
- 같은 사진을 여러번 돌리면 설명이 조금씩 달라지지만, 아주 큰 차이가 나지는 않습니다.
- 사진 설명속에서 glasses 혹은 spectacled 와 같은 단어가 나오면 안경을 쓴걸로 처리하겠습니다.

## 1차 결과
- Best 모드
  - 20개의 사진속에서 2개를 제외하고 glasses, spectacled라는 단어가 나타났습니다.
  - 아래 사진속에서 붉은색 동그라미 사진에서만 단어가 검출되지 않았는데요.
    - ![Alt text](https://reddol18.github.io/dev5min/images/20231207/image2.png)
  - 각 사진의 설명을 한 번 보겠습니다.
    ```
    arafed asian man in a suit sitting at a desk with papers, popular south korean makeup, evening news program, solemn face, official government photo, who is a robot, sad exasperated expression, jaeyeon nam, standing microphones, photograph of april
    양복을 입고 서류를 들고 책상에 앉아 있는 아시아 남자, 한국의 인기 메이크업, 저녁 뉴스 프로그램, 엄숙한 얼굴, 공식 정부 사진, 로봇인 사람, 슬픈 분노 표정, 남재연, 스탠딩 마이크, 4월 사진
    ```
    ```
    there is a man sitting at a table with a bird on his head, by Gao Fenghan, the secrets inside the vatican, profile portrait, interconnections, sangyeob park, local conspirologist, cathedrals and abbeys, feng zhu |, florentine school, professional profile picture
    테이블에 앉아 있는 남자와 머리에 새가 있다, Gao Fenghan, 바티칸 내부의 비밀, 프로필 초상화, 상호 연결, 박상엽, 지역 음모론자, 대성당과 수도원, 풍주 |, 피렌체 학교, 전문 프로필 사진
    ```
- Fast 모드
  - Fast 모드의 경우도 큰 차이는 없었는데요.
  - spectacled로 표현되었던 모인물의 사진에서 해당 단어가 사라졌습니다.
    - ![Alt text](https://reddol18.github.io/dev5min/images/20231207/image3.png)
  - Best 모드와 Fast 모드일 때 해당 사진의 설명을 비교해보면 다음과 같습니다.
    ```
    arafed image of a man in a suit and tie with a surprised look, kim jong-un, kawaii hair style, without eyebrows, red cloud, weird portrait angle, caseless ammunition, profile photo, spectacled, made in 2019, 8k octan advertising photo, key is on the center of image
    놀란 표정의 양복과 넥타이를 입은 남자의 아라페드 이미지, 김정은, 귀여운 머리 스타일, 눈썹 없음, 붉은 구름, 이상한 초상화 각도, 케이스 없는 탄약, 프로필 사진, 안경 쓴, 2019년산, 8k 옥탄 광고 사진 , 키는 이미지 중앙에 있습니다.
    ```
    ```
    arafed image of a man in a suit and tie with a surprised look, kim jung giu, overshadowing kim jong-il, kim jong-un, kim jong - un, kim jong un, kim jung-gi, kim jong - il, kim jong-il, korean symmetrical face, korean face features, kim jung gi, hyung-tae kim
    양복과 넥타이를 매고 놀란 표정의 남자의 아라페드 이미지, 김정기, 김정일을 무색하게 하는 김정일, 김정은, 김정은, 김정은, 김중기, 김정일, 김 종일, 한국 대칭 얼굴, 한국 얼굴 특징, 김정기, 김형태
    ```
  - 아무래도 Fast 모드일 때는 그 사진을 가장 대표하는 단어위주로 표현을 하기 때문에 비슷한 단어가 많이 나타나고, 이러다보니 디텍팅 확률은 감소하는 것으로 추측됩니다.

** 광고를 클릭하면 후속 내용을 확인할 수 있어요~ **
{% include adfit.html %}
{% include more_front.html %}
## 해상도 높이기
- 체크하지 못했던 2개까지 디텍팅 할 수 없을까요?
- 먼저 이미지의 해상도를 높여봤습니다. 이미지 해상도를 3배 늘렸는데요, 단순히 크기만 늘린건 아니고 AI를 이용해서 정확도 복원까지 해봤습니다.
- 그랬더니 Best 모드에서는 1개를 제외하고 안경을 찾아냅니다.
  - ![Alt text](https://reddol18.github.io/dev5min/images/20231207/image4.png)
- 안타깝게도 Fast 모드에서는 결과가 그대로 입니다.   

## 얼굴위주 사진으로 크롭
- 이번에는 얼굴부분만 떼어내서 Best 모드로 시도해봤습니다.
  - ![Alt text](https://reddol18.github.io/dev5min/images/20231207/image5.png)
  - 와우! 모두 안경을 썼다고 하네요~
- 그렇다면 Fast 모드는 어떨까요?
  - ![Alt text](https://reddol18.github.io/dev5min/images/20231207/image6.png)
  - 마스크를 쓰고 있는 사진이 문제였습니다.
  ```
  arafed woman wearing a mask with a blue face covering her mouth, wearing transparent glass mask, metallic mask around the mouth, full mask, wearing mask, gas mask in ukiyo-e style, ( ( mask ) ), surgical mask covering mouth, medical mask, wearing wooden mask, bag - valve mask, toxic air, dust mask, unsharp mask
  입을 덮고 있는 파란 얼굴의 마스크를 쓴 아라페드 여성, 투명한 유리 마스크 착용, 입 주위의 금속 마스크, 전체 마스크, 마스크 착용, 우키요에 스타일의 방독면, ((마스크)), 입을 덮는 수술용 마스크, 의료 마스크, 나무마스크 착용, 가방-밸브마스크, 유독공기, 먼지마스크, 언샵마스크
  ```
  - 안경을 유리마스크로 표현하는 바람에 glasses가 디텍팅 되지 않았는데요, 이런경우를 대비해서 glass도 감지 단어로 넣어주면 속도와 정확도를 동시에 취할 수 있지 않을까요?
{% include more_tail.html %}

