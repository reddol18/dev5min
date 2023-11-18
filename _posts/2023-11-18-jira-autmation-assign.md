---
layout: post
title: "지라(JIRA)의 자동화 기능을 이용해서 이슈 할당하기"
description: "지라(JIRA)의 자동화 기능을 이용해서 특정 레이블이 달릴 때 내 이슈로 자동 할당되게 해봅시다"
date: 2023-11-18
author: "김민석"
categories: [Others]
tags: [jira,automation,issues,label,assign]
---
- 저희 팀이 사용하는 지라의 프로젝트는 조금 이상합니다.
- 다름이 아니라 "담당자"를 지정해도 그 사람으로 할당이 되지 않는거에요.
- 칸반보드에서 작업자 별로 구분해서 보려면 할당이 되어야 하는데, 그게 매우 힘듭니다.
- 할당되지 않은 상태의 이슈중, 최하단에 있는것만 할당을 할 수 있는 상태입니다.
- 아무래도 버그이거나, 가격플랜상의 제약같은데요...
- 그렇다면 "자동화"를 이용해서 "담당자"를 바꿀때, 해당 트리거를 일으킨 사람에게 할당을 하면 되지 않을까요?
- 지라의 이슈에는 여러가지 필드가 있는데 그 중에 "담당자"도 포함되더라구요.

## 1차시도(실패)
- 먼저 프로젝트 설정의 오토메이션으로 들어간 다음, 자동화 규칙을 하나 만듭니다. 
    - ![Alt text](https://reddol18.github.io/dev5min/images/20231118/image-1.png)
- 그리고 트리거 종류로 "필드 값이 변경됨"을 선택하고, 아래 화면처럼 값을 지정합니다.
    - ![Alt text](https://reddol18.github.io/dev5min/images/20231118/image.png)
- 트리거 발생시 이슈 할당이 일어나게 하고, 대상은 트리거한 사용자로 합니다.
    - ![Alt text](https://reddol18.github.io/dev5min/images/20231118/image-2.png)
- 그런 다음 이슈의 담당자를 지정해 보겠습니다.    
    - ![Alt text](https://reddol18.github.io/dev5min/images/20231118/image-3.png)
- *안타깝게도 안됩니다.* 담당자=할당받는자 개념은 맞는것 같은데, 뭔가 칸반보드 상에 버그가 있는것 같습니다.    

{% include adfit.html %}

## 2차시도
- 이번에는 특정 "레이블"을 달 때, 할당이 되도록 해보겠습니다. 아래와 같은 레이블이 달리면 저에게 자동할당 시키겠습니다.
    - ![Alt text](https://reddol18.github.io/dev5min/images/20231118/image-4.png)
- 이슈페이지로 들어가서 레이블을 달아봤습니다. 담당자는 저로 되어 있지만, 칸반보드상에서는 할당자가 없는 상태였는데요...
    - ![Alt text](https://reddol18.github.io/dev5min/images/20231118/image-5.png)    
- 오! 이제 되네요. 
    - ![Alt text](https://reddol18.github.io/dev5min/images/20231118/image-6.png)
- 버그인지, 가격플랜의 제약인지는 모르겠지만 어쩔수 없이 이름을 자동화를 이용하는 수 밖에 없을것 같네요.