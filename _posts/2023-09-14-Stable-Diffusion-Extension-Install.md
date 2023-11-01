---
layout: post
title: "Stable Diffusion WebUI에서 Extension 설치시 오류가 날 때 대처"
description: "파이썬에서 Command를 통해 Git 사용을 할 수 있는 방법과, WebUI실행시 보안관련 옵션 설정하기"
date: 2023-09-14
author: "김민석"
categories: [Others]
tags: [stable diffusion,webui,extension,install]
---
- Stable Diffusion WebUI에서 Extension 설치가 안되는 경우가 있습니다.
- 먼저 아래와 같은 오류메시지가 나타나면서 안될 경우입니다.

```
gitcommandnotfound: cmd('git') not found due to: filenotfounderror('[errno 2] no such file or directory: 'git'')
```

- 이런 경우는 파이썬에서 git 명령어를 사용할 수 없기 때문에 발생합니다.
- ~/.bashrc를 아래와 같이 수정한 다음 (경로 및 인증서 파일은 실제환경에 맞게 변경해주셔야 합니다.)
```
export PATH=$PATH:/usr/bin/git
export GIT_PYTHON_GIT_EXECUTABLE=/usr/bin/git
export GIT_SSH_COMMAND="/usr/bin/ssh -i ~/.ssh/id_rsa"
```
- ``touch ~/.bashrc`` 실행해주신 후에 WebUI 다시 실행해서 설치해 보세요.

{% include adfit2.html %}

- 또한 공인되지 않은 extension의 경우 아래와 같은 옵션을 함께 입력하여 WebUI를 실행해야 합니다.
- ``--enable-insecure-extension-access``
```
python webui.py --listen --xformers --enable-insecure-extension-access
```
