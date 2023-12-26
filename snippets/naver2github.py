import requests
from bs4 import BeautifulSoup
from datetime import datetime
from dotenv import load_dotenv
import os
import json
import base64
from oauth2client.service_account import ServiceAccountCredentials
import httplib2

def download(url, file_name):
    with open(file_name, "wb") as file:
        response = requests.get(url)
        file.write(response.content)

def update_google_search_console_url_index(url):
    SCOPES = [ "https://www.googleapis.com/auth/indexing" ]
    ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish"

    # service_account_file.json is the private key that you created for your service account.
    JSON_KEY_FILE = "##your_account_file##.json"

    credentials = ServiceAccountCredentials.from_json_keyfile_name(JSON_KEY_FILE, scopes=SCOPES)
    headers = {'Content-Type': 'application/json'}
    http = credentials.authorize(httplib2.Http())

    # Define contents here as a JSON string.
    # This example shows a simple update request.
    # Other types of requests are described in the next step.

    content = """{
      \"url\": \"%s\",
      \"type\": \"URL_UPDATED\"
    }""" % url

    response, content = http.request(ENDPOINT, method="POST", body=content, headers=headers)
    print(response)
    print(content)

def get_github_sha(url, token):
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": "Bearer %s" % token,
        "X-GitHub-Api-Version": "2022-11-28"
    }
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        return r.json().get("sha")
    return False

def get_blog_content(blog_id, post_id, reg_date, github_img_path, author, category, tags):
    mark_downs = ['---',
                  'layout: post',
                  '',
                  '',
                  'date: %s' % reg_date,
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
                    img_src = item.attrs.get("data-lazy-src")
                    if img_src is None:
                        img_src = item.attrs.get("src")
                    file_name = "img_file_%s.png" % img_file_count
                    download(img_src, file_name)
                    img_file_count = img_file_count + 1
                    mark_downs.append("![Alt text](%s/%s)<br/>" % (github_img_path, file_name))

                else:
                    if is_fist:
                        mark_downs[2] = 'title: "%s"' % item.text.replace("<!-- -->", "")
                        mark_downs[3] = 'description: "%s"' % item.text.replace("<!-- -->", "")
                        is_fist = False
                    else:
                        children = item.findAll(recursive=False)
                        anchor_children = False
                        for child in children:
                            if child.name == "a":
                                anchor_children = child
                        if anchor_children is not False:
                            mark_downs.append("[%s](%s)<br/>" % (anchor_children.text, anchor_children.attrs.get("href")))
                        else:
                            mark_downs.append("%s<br/>" % item.text)
    return mark_downs, img_file_count

def put_github_file(url, github_owner, email, content, token):
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": "Bearer %s" % token,
        "X-GitHub-Api-Version": "2022-11-28"
    }
    sha = get_github_sha(url, token)
    if sha == False:
        ## No sha means No File
        data = {
            "message": "commit",
            "branch": "##your_branch##",
            "committer": {
                "name": github_owner,
                "email": email
            },
            "content": content
        }
        requests.put(url, data=json.dumps(data), headers=headers)
    else:
        ## Update File
        data = {
            "message": "commit",
            "branch": "##your_branch##",
            "sha": sha,
            "committer": {
                "name": github_owner,
                "email": email
            },
            "content": content
        }
        requests.put(url, data=json.dumps(data), headers=headers)

def add_to_github(reg_date, post_id, md, img_count, github_owner, email, github_repo, post_path, img_path, github_token):
    github_post_url = "https://api.github.com/repos/%s/%s/contents/%s" % (github_owner, github_repo, post_path)
    github_image_url = "https://api.github.com/repos/%s/%s/contents/%s" % (github_owner, github_repo, img_path)

    # MD File Commit
    post_name = "%s-%s.md" % (reg_date, post_id)
    md_bytes = '\n'.join(md).encode('utf-8')
    md_base64 = base64.b64encode(md_bytes)
    put_github_file("%s/%s" % (github_post_url, post_name), github_owner, email, md_base64.decode('ascii'), github_token)

    # Image Files Commit
    for i in range(img_count):
        img_file_name = "img_file_%s.png" % i
        with open(img_file_name, "rb") as image_file:
            img_base64 = base64.b64encode(image_file.read())
            put_github_file("%s/%s" % (github_image_url, img_file_name), github_owner, email, img_base64.decode('ascii'), github_token)


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
site_url = os.environ.get("site_url")

today = datetime.today().strftime('%Y%m%d')

full_img_path = "https://%s.github.io/%s/%s/%s" % (github_owner, github_repo, github_img_path, today)

reg_date = datetime.today().strftime('%Y-%m-%d')
#reg_date = "2023-12-18"

md, img_count = get_blog_content(blog_id, post_id, reg_date, full_img_path, author, "Lifes", tags)

add_to_github(reg_date, post_id, md, img_count, github_owner, email, github_repo, github_post_path, "%s/%s" % (github_img_path, today), github_token)
update_google_search_console_url_index("%s/%s" % (site_url, post_id))
