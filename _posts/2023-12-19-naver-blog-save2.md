---
layout: post
title: "네이버 블로그를 백업해보자 - 2편"
description: "파이썬을 이용해서 네이버 블로그에 있는 내용과 이미지를 깃헙 블로그에 보내보겠습니다"
date: 2023-12-19
author: "김민석"
categories: [Data and Api]
tags: [naver,naverblog,blog,backup,githubapi,githubblog]
---
- 지난 시간에는 네이버 블로그에 있는 글과 이미지를 가져오는 방법에 대해서 고민해 봤다면
    - [네이버 블로그를 백업해보자 - 1편](https://reddol18.pe.kr/naver-blog-save)
- 오늘은 가져온 글과 이미지를 GITHUB API를 이용해서 깃헙블로그에 올리는 내용을 살펴보겠습니다.
- 제가 운용하는 깃헙블로그는 깃헙페이지와 jekyll을 이용해서 구축되었습니다.
- GITHUB API를 이용하기 위해서는 사전에 TOKEN을 받아두어야 합니다.
- 긴 말 할 거 없이 코드를 보시죠~

{% include adfit.html %}

```python
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from dotenv import load_dotenv
import os
import json
import base64

# 이미지 파일을 다운로드하는 함수
def download(url, file_name):
    with open(file_name, "wb") as file:
        response = requests.get(url)
        file.write(response.content)

# 블로그로부터 글과 이미지를 가져오는 함수
def get_blog_content(blog_id, post_id, github_img_path, author, category, tags):
    # 블로그에 올라가는 마크다운 헤더를 미리 지정합니다
    mark_downs = ['---',
                  'layout: post',
                  '',
                  '',
                  'date: %s' % datetime.today().strftime('%Y-%m-%d'),
                  'author: "%s"' % author,
                  'categories: [%s]' % category,
                  'tags: [%s]' % tags,
                  '---'
    ]
    post_url = 'https://blog.naver.com/PostView.naver?blogId=%s&logNo=%s&redirect=Dlog&widgetTypeCall=true&directAccess=true'
    html_text = requests.get(post_url % (blog_id, post_id)).text
    soup = BeautifulSoup(html_text, 'html.parser')

    img_file_count = 0
    is_fist = True
    for item in soup.select('span, img'):
        has_text = False
        if item.attrs.get("class"):
            for classItem in item.attrs.get("class"):
                if str(classItem).count("se-f") > 0:
                    has_text = True
                elif str(classItem).count("se-image-resource") > 0:
                    has_text = True
            if has_text:
                if item.name == 'img':
                    # 이미지 파일을 다운로드 합니다
                    img_src = item.attrs.get("data-lazy-src")
                    file_name = "img_file_%s.png" % img_file_count
                    download(img_src, file_name)
                    img_file_count = img_file_count + 1
                    mark_downs.append("![Alt text](%s/%s)<br/>" % (github_img_path, file_name))
                else:
                    if is_fist:
                        # 첫번째 텍스트는 제목이기 때문에
                        mark_downs[2] = 'title: "%s"' % item.text.replace("<!-- -->", "")
                        mark_downs[3] = 'description: "%s"' % item.text.replace("<!-- -->", "")
                        is_fist = False
                    else:
                        mark_downs.append("%s<br/>" % item.text)
    return mark_downs, img_file_count

# 깃헙 API를 이용해서 파일을 업로드하는 함수
def github_api(url, github_owner, email, content, token):
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": "Bearer %s" % token,
        "X-GitHub-Api-Version": "2022-11-28"
    }
    data = {
        "message": "commit",
        "committer": {
            "name": github_owner,
            "email": email
        },
        "content": content
    }
    requests.put(url, data=json.dumps(data), headers=headers)

# 깃헙 API 함수를 호출하기 위한 중간 함수
def add_to_github(post_id, md, img_count, github_owner, email, github_repo, post_path, img_path, github_token):
    github_post_url = "https://api.github.com/repos/%s/%s/contents/%s" % (github_owner, github_repo, post_path)
    github_image_url = "https://api.github.com/repos/%s/%s/contents/%s" % (github_owner, github_repo, img_path)

    # MD File Commit
    post_name = "%s-%s.md" % (datetime.today().strftime('%Y-%m-%d'), post_id)
    md_bytes = '\n'.join(md).encode('utf-8')
    # base64로 변환후에 이것을 다시 ascii text로 바꿉니다
    md_base64 = base64.b64encode(md_bytes)
    github_api("%s/%s" % (github_post_url, post_name), github_owner, email, md_base64.decode('ascii'), github_token)

    # Image Files Commit
    for i in range(img_count):
        img_file_name = "img_file_%s.png" % i
        with open(img_file_name, "rb") as image_file:
            img_base64 = base64.b64encode(image_file.read())
            github_api("%s/%s" % (github_image_url, img_file_name), github_owner, email, img_base64.decode('ascii'), github_token)

# .env 파일로부터 변수들을 가져 옵니다
load_dotenv()
blog_id = os.environ.get("blog_id")
post_id = os.environ.get("post_id")
github_owner = os.environ.get("github_owner")
github_repo = os.environ.get("github_repo")
email = os.environ.get("email")
github_post_path = os.environ.get("github_post_path")
github_img_path = os.environ.get("github_img_path")
author = os.environ.get("author")
tags = os.environ.get("tags")
github_token = os.environ.get("github_token")

today = datetime.today().strftime('%Y%m%d')

full_img_path = "https://%s.github.io/%s/%s/%s" % (github_owner, github_repo, github_img_path, today)

md, img_count = get_blog_content(blog_id, post_id, full_img_path, author, "Lifes", tags)
add_to_github(post_id, md, img_count, github_owner, email, github_repo, github_post_path, "%s/%s" % (github_img_path, today), github_token)
```

- 위 코드를 이용해서 옮겨온 포스팅입니다. 실제 네이버 블로그 주소도 함께 공유합니다.
    - [코콤 CCTV 고장 나서 고친 경험담](https://reddol18.pe.kr/223284817896)
    - [네이버블로그-코콤 CCTV 고장 나서 고친 경험담](https://blog.naver.com/dolja21/223284817896)
- 그런데 위 코드는 최초 생성만 가능합니다. 아직 기능에 한계가 있습니다.
- 다음 시간에는 이미 올라가 있는 파일을 수정하고, 구글서치콘솔에 URL을 등록하여 인덱싱하는 내용을 고민해 보겠습니다.