---
layout: post
title: "IPTABLES에 관한 몇 가지 사실들"
description: "IPTABLES에 관한 몇 가지 사실들을 확인해 봤습니다"
date: 2022-07-14
feature_image: /images/default-thumbnail.jpg
author: "김민석"
categories: [Security]
tags: [iptables,rules,max,count]
---
### 정의 가능한 최대 룰의 수

iptables를 아래와 같은 룰들로 정의해서 사용하는데요.
```
-A INPUT -p tcp -m tcp --dport 10021 -j ACCEPT
-A INPUT -p tcp -m tcp --dport 20 -j ACCEPT
-A INPUT -s 211.33.81.233 -j ACCEPT
-A INPUT -s 183.102.23.69 -j ACCEPT
-A INPUT -s 188.165.205.0/255.255.255.0 -j DROP
-A INPUT -s 62.210.167.0/255.255.255.0 -j DROP
```
과연 얼마나 많은 룰을 사용할 수 있는지 궁금했어요. 
그래서 검색을 해봤습니다.

**그 결과 25000개 까지 가능하다고 하네요.**

### 특정 URL을 상대로 룰을 적용할 수 있는가?

불가능한 것으로 보입니다. 어찌보면 당연한 것 입니다.
iptables는 레이어 3~4의 수준에서 관여합니다.
그런데 URL을 지정하는 패킷을 확인하고 관여하는것은 그것보다 더 고수준의 영역 입니다.
