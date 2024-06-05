---
layout: post
title: "파이선에서 다른 가상환경을 이용하는 스크립트를 실행하기"
description: "os.system으로는 안되지만 이걸로는 됩니다!"
date: 2024-05-17
author: "김민석"
categories: [others]
tags: [python,anaconda,conda,conda_in_python]
---
- 종종 다른 의존성 라이브러리를 사용하는 파이선 코드를 또 다른 파이선 코드 내부에서 실행해야 하는 경우가 있습니다.
- 다음과 같은 상황을 가정해 봅시다.
  - a.py라는 파이선 프로그램은 ``conda activate a_config``로 가상환경을 지정하고 실행했습니다.
  - 이때 ``conda activate b_config``로 가상환경을 지정하고 실행해야 하는 b.py를, a.py 내부에서 실행시키고 싶습니다.
  - 어떻게 해야 할까요? 아래 코드를 참고하시면 됩니다.
- 먼저 b.py를 실행시키는 쉘스크립트 b.sh를 만듭니다.
- 경로는 사용하시는 값으로 지정하셔야 합니다! b.sh는 b.py가 있는 경로에 만들겠습니다.

```sh
#!/bin/bash
PATH=$PATH:${conda가 설치된 경로}/anaconda3/envs/b_config/bin
cd ${b.py가 존재하는 경로}
python b.py
```

{% include adfit2.html %}    

- 그리고 나서 a.py에서 아래처럼 b.sh를 실행해 주세요.

```python
import subprocess

try:
    b_path = "b.py가 있는 경로"
    conda_path = "b_config가 설치된 경로"
    python_version = "b_config가 사용하는 파이선 버전 ex:python3.10"
    os.chdir(b_path)
    new_env = {
        "PATH": b_path,
        "PYTHONPATH": "%s/lib/%s/site-packages" % (conda_path python_version),
    }
    subprocess.run(["b.sh", 필요한 인자값들...], env=new_env)    
except Exception as e:
    print(e)
```

- 인자값들이 필요하면 쉼표로 구분하면서 이어 넣으면 됩니다.