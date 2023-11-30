---
layout: post
title: "Interrogator를 이용해서 게임그래픽을 만들 수 있다??"
description: "clip-interrogator와 stable diffusion을 이용해서 간단한 게임그래픽 이미지를 만들어 보겠습니다"
date: 2023-11-24
author: "김민석"
categories: [ComputerVision]
tags: [clip-interrogator,stable-diffusion,game-graphic-generation]
---
- 이미지를 지정하면, 그것을 텍스트로 설명해주는 생성형 AI 기술인 clip-interrogator
- https://github.com/pharmapsychotic/clip-interrogator
- 이것과 Stable Diffusion을 이용하면 정말 어려운 작업을 손쉽게 수행할 수 있는데요.
- 특히 clip-interrogator은 Stable Diffusion Extension으로도 사용할 수 있기 때문에, 아주 간단하게 쓸 수 있어요.
- 한 번 실험삼아 해볼까요? 오늘 생성형 이미지로 재현할 사진은 바로 아래 이미지 입니다.
  - ![Alt text](https://reddol18.github.io/dev5min/images/20231130/image.png)
  - 1호선 빌런으로 유명한, 자르X84세
  - 이런 기상천외한 복장을 입은 사람의 사진을 SD가 재현할 수 있을까요?
- Interrogator에게 해설을 요청합니다
    - 아래와 같은 text가 출력됩니다.
    ```
    arafed man dressed in a gold costume on a subway train, kpop amino, with an armor and a crown, korean traditional palace, the last photo ever taken, mallsoft, anno 1404, samurai, north korean slasher, 2045, bossfight
    ```
- 이걸 이제 SD에 prompt로 입력하구요.
- 컨트롤넷을 이용해서 유사도를 높이고, ADetailer를 이용해서 얼굴이 일그러지지 않도록 해보겠습니다.
- 그러자 아래와 같은 이미지들이 만들어 집니다.
  - ![Alt text](https://reddol18.github.io/dev5min/images/20231130/image2.png)
  - 어떤가요? 비슷한가요??
  
 {% include adfit.html %}

### 게임그래픽도 가능할까??
- 이번에는 레트로 2D RPG 게임화면을 Interrogator에게 설명해보라고 했습니다.
    ```
    a close up of a map of a park, 2d  sprites asset sheet, pokemon style, trees reflecting on the lake, friendly guy and small creature, stable diffusion ai, next to a red barn, pixelart, pathway, midwest countryside, perfectly shaded, travelers, website banner
    ``` 
- 이번에는 이런 Prompt를 만들어내는군요. 여기에 ``(top view:1.3), (2d game map:1.3), (2d sprite:1.3),seen from above the sky,(2d rpg game map:1.3)``를 추가해서 조금 더 완성도를 높여 봤습니다.    
- 2D 게임 그래픽을 만들거기 때문에, negative prompt에 ``3d, quarter view``를 입력했습니다.
- 그러자 아래와 같은 이미지들이 만들어집니다.
  - ![Alt text](https://reddol18.github.io/dev5min/images/20231130/image3.png)
  - 이 이미지를 잘 가공하면 그래픽 디자이너 없이 게임도 만들 수 있겠어요~