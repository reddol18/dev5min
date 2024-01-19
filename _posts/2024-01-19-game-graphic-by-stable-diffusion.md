---
layout: post
title: "Stable Diffusion으로 게임 그래픽 만들기"
description: "그래픽 디자인 재능이 없어도 AI를 이용해서 게임 그래픽을 만드는 방법을 소개해 봅니다."
date: 2024-01-19
author: "김민석"
categories: [Computer Vision]
tags: [stable_diffusion,sd,ai,game_graphic]
---
### 게임 그래픽 제작을 AI가 할 수 있다고?

- 예전에 이 블로그에 clip-interrogator를 이용해서 게임그래픽도 만들 수 있겠다고 소개한 적이 있었죠.
- [Interrogator를 이용해서 게임그래픽을 만들 수 있다??](https://reddol18.pe.kr/interrogator-with-sd)<br/>
- ![AI그린 게임그래픽](https://reddol18.github.io/dev5min/images/20231130/image3.png)
- 그런데 이렇게 만든 이미지의 문제점이 타일단위로 잘라내기 어렵다는 점이었는데요.
- 물론 잘 나온 이미지는 굳이 타일로 자르지 않고 그대로 써도 되겠지만
- 생성형 AI 특성상 만들어지는 이미지를 통제하기가 쉬운것은 아닙니다.

### 그런데 그래픽 유닛을 만들수 있어요!

- 그런데 이미 많은 사람들이 AI를 이용해서 게임그래픽을 만드는 시도를 하고 있었더라구요.
- 아래 사이트에 많은 리소스들이 공개되어 있습니다.
- [OPENART AI 게임그래픽](https://openart.ai/discovery/sd-1005771838019870740)
- 그래서 저도 한 번 시도해봤어요.
- 모델은 3개를 썼는데요
  - 제가 직접 제작한 수묵화 스타일의 모델
  - 만화 스타일의 모델
  - 그리고 실사 스타일의 모델
- 쿼터뷰 시점의 리소스와 탑뷰 시점의 리소스를 만들어 봤습니다.  

### 쿼터뷰 시점 리소스

- 수묵화 모델
  - [성채이미지](https://reddol18.github.io/dev5min/images/20240119/kpaint.png)
  - [건축물이미지](https://reddol18.github.io/dev5min/images/20240119/kpaint2.png)

- 만화 모델
  - [성채이미지](https://reddol18.github.io/dev5min/images/20240119/cartoon1.png)
  - [건축물이미지](https://reddol18.github.io/dev5min/images/20240119/cartoon2.png)

- 실사 모델
  - [성채이미지](https://reddol18.github.io/dev5min/images/20240119/real1.png)
  - [건축물이미지](https://reddol18.github.io/dev5min/images/20240119/real2.png)

- 성채 이미지의 경우엔 조금씩 모델의 특징을 따라가는 것으로 보입니다.
  - 사용한 프롬프트는 다음과 같습니다.
  - ``set of isometric game tiles, containing a wizard's tower, enemies'hideouts and several resources, colored lineart from resource gathering game``
  - 수묵화 모델은 색표현이 상당히 플랫한 반면, 만화 모델은 다소 화려하네요.
  - 실사의 경우엔 조금더 디테일이 살아 있습니다.
- 하지만 건축물이미지의 경우엔 3가지 모델에서 큰 차이를 확인하기가 어렵습니다.
  - 사용한 프롬프트 입니다.
  - ``isometric view, detailed, medieval tavern and a castle, asset on grey background``
  - 그나저나 건축물은 결과물이 엄청나네요. 프로가 그린거 뺨치는 품질입니다.

{% include adfit.html %}

### 탑뷰 시점 리소스

- 수묵화 모델
  - [타일팔레트](https://reddol18.github.io/dev5min/images/20240119/kpaint_tile.png)
  - [나무스프라이트1](https://reddol18.github.io/dev5min/images/20240119/kpaint_tree.png)
  - [나무스프라이트2](https://reddol18.github.io/dev5min/images/20240119/kpaint_tree2.png)
  - [나무스프라이트3](https://reddol18.github.io/dev5min/images/20240119/kpaint_tree3.png)

- 만화 모델
  - [타일팔레트1](https://reddol18.github.io/dev5min/images/20240119/cartoon_tile.png)
  - [타일팔레트2](https://reddol18.github.io/dev5min/images/20240119/cartoon_tile2.png)
  - [나무스프라이트1](https://reddol18.github.io/dev5min/images/20240119/cartoon_tree.png)
  - [나무스프라이트2](https://reddol18.github.io/dev5min/images/20240119/cartoon_tree2.png)

- 실사 모델
  - [타일팔레트1](https://reddol18.github.io/dev5min/images/20240119/real_tile.png)
  - [타일팔레트2](https://reddol18.github.io/dev5min/images/20240119/real_tile2.png)
  - [나무스프라이트1](https://reddol18.github.io/dev5min/images/20240119/real_tree.png)
  - [나무스프라이트2](https://reddol18.github.io/dev5min/images/20240119/real_tree2.png)
  - [나무스프라이트3](https://reddol18.github.io/dev5min/images/20240119/real_tree3.png)

- 타일의 경우엔 3가지 모델에서 조금씩 다르지만 쓸만한 결과물들을 얻었습니다.
  - 사용한 프롬프트들은 다음과 같습니다.
  - ``game tiles 16x16, grass, night and day``
  - ``grass texture, pixel art game asset``
  - 잘 응용하면 흙길, 돌길, 물과 같은 타일도 만들수 있을겁니다.
- 나무의 경우가 참 흥미롭습니다.
  - 사용한 프롬프트들 입니다.
  - ``a video game sprite sheet of fantasy forest trees``
  - ``game assets of plants and tree``
  - 나무같은 경우가 참 표현하기 어렵겠단 생각이 들었었는데, 이렇게 멋진 리소스가 만들어지네요.

### 앞으로의 목표

- 이왕 이렇게 된거 게임한번 만들어 봐야 겠죠??
- 먼저 필요한 그래픽 리소스들을 다 확보해 보도록 하겠습니다.
- NPC들의 대사의 경우에도 AI를 이용하면 재미있을것 같으니 그 쪽도 한 번 연구해 보겠습니다.