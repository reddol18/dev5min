---
layout: post
title: "IntelliJ Idea Remote Development 사용시 멀티 프로젝트를 위한 모듈 설정"
description: "Project 설정시에 여러개의 Modules을 지정하는 방법을 소개합니다"
date: 2024-01-08
feature_image: https://reddol18.github.io/dev5min/images/20240108/image.png
author: "김민석"
categories: [Others]
tags: [intellij,jetbrains,project_structure,modules,problem,multi_module,multi_project]
---
예전에 인텔리제이 원격개발 환경에서 프로젝트에 모듈을 지정하는 방법에 대해서 소개한 바가 있습니다.
- [IntelliJ Idea Remote Development 사용시 프로젝트 모듈 설정이 안될 때](https://reddol18.pe.kr/IntelliJ-Remote-Modules-Problem)

이때는 1개의 모듈을 사용하는 경우를 소개한 것 인데요. 필요에 따라서는 하나의 프로젝트 환경에 여러개의 모듈을 사용하는 경우가 있을 수 있죠?
아래 그림처럼 말이에요~
![Alt text](https://reddol18.github.io/dev5min/images/20240108/image.png)

방법은 간단합니다. 먼저 1개의 모듈일 때 처럼, 추가하려는 모듈의 폴더에 들어가서 아래 작업을 수행해 주세요.

{% include adfit2.html %}

### 먼저 .idea 폴더 내에 [프로젝트명].iml 파일을 만들고 아래와 같이 기입합니다. 파이썬 프로젝트 일 때의 예제에요.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<module type="PYTHON_MODULE" version="4">
  <component name="NewModuleRootManager" inherit-compiler-output="true">
    <exclude-output />
    <content url="file://$MODULE_DIR$" />
    <orderEntry type="inheritedJdk" />
    <orderEntry type="sourceFolder" forTests="false" />
  </component>
</module>
```

그런다음 최초에 지정되어 있던 모듈의 폴더에서 아래처럼 내용을 수정합니다.

### 최초에 지정된 모듈의 .idea 폴더의 modules.xml을 수정합니다.

{% include more_front.html %}

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project version="4">
    <component name="ProjectModuleManager">
        <modules>
            <module fileurl="file://$PROJECT_DIR$/.idea/[프로젝트1명].iml" filepath="$PROJECT_DIR$/.idea/[프로젝트1명].iml" />
            <module fileurl="file://[프로젝트2경로]/.idea/[프로젝트2명].iml" filepath="[프로젝트2경로]/.idea/[프로젝트2명].iml" />
        </modules>
    </component>
</project>
```

프로젝트2경로는 절대경로로 해도되고, 프로젝트1의 경로에 맞춰서 상대경로로 해도됩니다.        

{% include more_tail.html %}