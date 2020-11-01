#!/usr/bin/env python
# coding: utf-8

# ## 获取access_token

# In[47]:


import requests
import time
import pytz
import datetime

api_url = 'https://microsoftgraph.chinacloudapi.cn'

def get_categories():
    blogs = get_blog_list()
    categories = {
        '学习':[],
        'project':[],
        'technology':[],
    }
    for blog in blogs:
        if blog.get('name')=="about.md":
            continue
        blog_info = blog.get('name').split('-')
        if not len(blog_info) == 2:
            blog_info.append("无分类")
        if not categories.get(blog_info[1]):
            categories[blog_info[1]] = []
        categories[blog_info[1]].append(blog)
    return categories

def u2i(utc_time_str, utc_format='%Y-%m-%dT%H:%M:%SZ'):
    local_tz = pytz.timezone('Asia/Chongqing')
    local_format = "%Y-%m-%d %H:%M"
    utc_dt = datetime.datetime.strptime(utc_time_str, utc_format)
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
    time_str = local_dt.strftime(local_format)
    return int(time.mktime(time.strptime(time_str, local_format)))

def get_token():
    url = "https://login.partner.microsoftonline.cn/common/oauth2/v2.0/token"

    payload = 'client_id=b15f63f5-8b72-48b5-af69-8cab7579bff7&client_secret=0IIuZ1Kcq_YI3NrkZFwsniEo%7EBoP%7E8_M22&grant_type=refresh_token&redirect_uri=https%3A//scfonedrive.github.io&refresh_token=0.AAAAZEYM4jUDwUaAQzwbd_rERfVjX7Fyi7VIr2mMq3V5v_cBAP4.AQABAAAAAAAA2xsa-zUZSpZL3C5ZKV2zvScNi70IRBPqdTCIk_BEAKERWAQG29aVh3CP1aw-hwMa_2vPpPwpnooVlBB1ZQoLqrDXuEsWYgMvkfOl4p1ARCoPNmZyXLUGPj04d-bQyYL425a9E4zrUaLaMBxFxMpRjiOG4C_ddBS1shvDcIuFKkTY0C8JXxNikhYb6k6uBlQwUOHI0zU0x705tuHU2yC1vpEVu7aOsBNF0xt8ZBXtwTONyDhq8V3svrIzSxvYGSSsMvMx40sDSc1d6pdv7kJfmHCZsVf55illaR15-Zuo-U5sRNRTje_R5BUGQlUFIV5C3Kp0WwdxAJBlRYGNvcJ6n1-9_In6nlM5k1sYowItfaiJ93UKeVAZIiYmAhAXPdEZyomfgpB89unANTKL0it68ztmGkufZ4yMy6BBUk9FRIbRbn8AtIoh7C4BkzQomidmrvhi2V3WSux-1fNZBohvZ0Ix3CCNspeS4ZgMAMQgGO6HePIAHSs8tjUV7wSdLP6SM57o-xgOfoYaotIMEv9vPULaI3BDvqHWMY93Ykjyjd323RzgFMKpr4ZFYH5xPNC8qALNz-mGUrnAoUHE22FDmFnliXItRN4qgqfwCRw_3n-hvjWdokgT7jPW3go18y8868kneJ-qzzz3ugmOD5y3DxUVokDEplX8RqnPLSdMzOLxj88TAbQfj7LT4L6LvLjc2AheZAA4jUHaPdohnmSAt9RyCJny3-zl7dmZ9gL4E9ZG9Cpwd-BW3Av4uUXUYo58Mquy2n46mGWG0qUwD_bB3MQBSpnp78b1i4Q0BqiYNcG9qxMhuHb3ew8EqOpP4cO16r0K4aZ_3i79-5E9Lmu8aWJytRzquGZty1UZ5GUeC4pS5CWGd6Wcmlg7uTKrxVvqz5AGbpUCIZ3BNNOjZaRTIAA&scope=https%3A//microsoftgraph.chinacloudapi.cn/Files.ReadWrite.All%20offline_access'
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Cookie': 'x-ms-gateway-slice=productionb; stsservicecookie=estschina; fpc=AiP8Kz9rLHhMhgo0CoT6U9uHbAEGAQAAAFgfKtcOAAAAC6LoOwIAAAANICrXDgAAABKK-CcBAAAAyCAq1w4AAAA'
    }

    response = requests.request("POST", url, headers=headers, data = payload)
    access_token = response.json()['access_token']
    return access_token


def get_blog_list():
    access_token = get_token()
    payload = {}
    
    url = api_url + "/v1.0/me/drive/root/children/blog/children"
    headers = {
      'Authorization': 'Bearer '+access_token
    }
    response = requests.request("GET", url, headers=headers, data = payload)
    result = response.json()
    blogs = sorted(result.get('value'), key=lambda k:u2i(k.get('createdDateTime')), reverse=True)
    return blogs

def admin_get_list(path):
    access_token = get_token()
    payload = {}
    url = api_url + "/v1.0/me/drive/root/children/blog"+path+"/children"
    headers = {
      'Authorization': 'Bearer '+access_token
    }
    response = requests.request("GET", url, headers=headers, data = payload)
    result = response.json()
    return result.get('value')

def show_blogs():
    result = get_blog_list()
    blogs = result.get('value')
    for blog in blogs:
        print('标题：'+blog.get('name')+' 创建时间：'+blog.get('createdDateTime')+' 最后编辑于：'+blog.get('lastModifiedDateTime'))

def get_blog_link(name):
    base_url = api_url + '/v1.0/me/drive/root:/blog/'
    url = base_url + name + '/blog.md'
    access_token = get_token()
    headers = {
      'Authorization': 'Bearer '+access_token
    }
    response = requests.request("GET", url, headers=headers)
    blog_link = response.json().get('@microsoft.graph.downloadUrl')
    return blog_link

def get_item(title, item):
    base_url = api_url + '/v1.0/me/drive/root:/blog/'
    url = base_url + title + '/' + item
    access_token = get_token()
    headers = {
      'Authorization': 'Bearer '+access_token
    }
    response = requests.request("GET", url, headers=headers)
    item_link = response.json().get('@microsoft.graph.downloadUrl')
    return item_link

# In[63]:


from urllib import request
import markdown
import content
def get_blog_content(name):
    blog_link = get_blog_link(name)
    html = content.create(blog_link)
    return html

def get_about():
    base_url = api_url + '/v1.0/me/drive/root:/blog/'
    url = base_url + 'about.md'
    access_token = get_token()
    headers = {
      'Authorization': 'Bearer '+access_token
    }
    response = requests.request("GET", url, headers=headers)
    link = response.json().get('@microsoft.graph.downloadUrl')
    text = request.urlopen(link).read().decode("utf8")
    html = markdown.markdown(text)
    return html
