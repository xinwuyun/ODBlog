# -*- coding: utf-8 -*-
import re
import json
import markdown
from urllib import request

pattern = '#+\s'

heading = {
    'heading1': 0,
    'heading2': -1,
    'heading3': -1,
    'heading4': -1,
    'heading5': -1,
    'heading6': -1
}

htmlHead = u'''
<!DOCTYPE html>
<html lang="zh-CN">
<title>wzr's blog</title>
<link href="https://s0.pstatp.com/cdn/expire-1-M/dplayer/1.25.0/DPlayer.min.css" rel="stylesheet">
<script src="https://s0.pstatp.com/cdn/expire-1-M/dplayer/1.25.0/DPlayer.min.js"></script>
<script src="https://s0.pstatp.com/cdn/expire-1-M/hls.js/0.12.4/hls.light.min.js"></script>
<script src="https://s0.pstatp.com/cdn/expire-1-M/flv.js/1.5.0/flv.min.js"></script>
<!--Dplayer-->
<head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<script src="https://apps.bdimg.com/libs/jquery/2.1.4/jquery.min.js"></script>
<script src="/static/js/index.js"></script>
<link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" rel="stylesheet">
<link rel="icon" type="image/jpg" sizes="144x144" href="/static/iamge/touxiang.jpg"/>
<!-- Main styles -->
<link href="/static/css/index.css" rel="stylesheet">   
</head>
    
	<div class="banner">
	  <div class="container">欢迎光临我的博客</div>
	</div>
    
    <div class="container docs-container">
      <div class="row">
        <div class="col-md-3">
          <div class="sidebar hidden-print affix" role="complementary">
            <div id="navigation">
				<ul class="nav sidenav" id="parentnode">
				</ul>
		      </div>
          </div>
        </div>
		
        <div class="col-md-9" role="main">
          <header class="navbar navbar-inverse navbar-fixed-top docs-nav" role="banner">
		  <div class="container">
			 <nav class="collapse navbar-collapse bs-navbar-collapse" role="navigation">
			  <ul class="nav navbar-nav">
				<li class="active">
				  <a href="/">STYX BLOG</a>
                </li>
                <li class="active">
                  <a href="/archives">归档</a>
                </li>
                <li class="active">
				  <a href="/categories">分类</a>
                <li class="active">
                  <a href="/about">关于</a>
                </li>
			  </ul>
			</nav>
			
		  </div>
		 </header>

		<div class="panel docs-content">
  

			<div class="docs-section">
'''

endHtml = u'''
</div>
		  </div>
      </div>
		
    </div>
  </div>
 '''

htmlTail = u'''
<h3 style="text-align:center;">© 2020 STYX WANG</h3>
<script>
    const dp = new DPlayer({
        container: document.getElementById('dplayer'),
        video:{
            url:document.getElementById('dplayer').getAttribute('src')
        }
    });
</script>
</body>
</html>
 '''


def formatHeading():
    heading['heading1'] = 0
    heading['heading2'] = -1
    heading['heading3'] = -1
    heading['heading4'] = -1
    heading['heading5'] = -1
    heading['heading6'] = -1


def updateHeading(current, headId):
    for i in range(1, 6):
        if len(current) == i:
            heading['heading%r' % i] = headId


def getMenu(link):
    titles = []
    global heading
    headId = 1
    current = None
    preCurrent = '$'
    parentID = 0
    f = request.urlopen(link)
    for i in f.readlines():
        title = {}
        if not re.match(pattern, i.decode().strip(' \t\n')):
            continue
        i = i.decode().strip(' \t\n')
        current = i.split(' ')[0]
        # 当前标题级别比前一个小，则当前标题的父类标题是上一个的headId
        # 注释：#越多级别越小
        # 不论大多少个级别，只要父类级别大就是它的父类
        if len(current) > len(preCurrent):
            parentID = headId - 1
            # 更新当前级别父类
            updateHeading(current, parentID)
        # 当前级别比父类级别大，则去heading中寻找记录过的父类级别
        # 注释：#越少级别越大
        elif len(current) < len(preCurrent):
            length = len(current)
            # 当在文中出现一级标题的时候还原所有父类级别到初始值
            if length == 1:
                formatHeading()
                # 给当父类结果类赋值
                parentID = 0
            else:
                getVal = heading['heading%r' % length]
                # 如果有记录过该级别的父类项
                if getVal != -1:
                    parentID = getVal
                # 改级别项没有记录则依次向上找父类，指导找到一级标题
                else:
                    for j in range(length, 1, -1):
                        tempVal = heading['heading%r' % j]
                        if tempVal != -1:
                            parentID = tempVal
                            break
        titleName = i[len(current):].strip(' \t\n')
        title['titleName'] = titleName
        title['titleID'] = headId
        title['parentID'] = parentID
        titles.append(title)
        # print(headId, current, parentID)
        preCurrent = current
        headId += 1
    # print(titles)
    return titles

def addAnchorMark(titles, content):
    anchorHtml = u''
    for i in content.split('\n'):
        for title in titles:
            old = '>' + title['titleName'] + '<'
            new = " class='docs-heading'><span class='anchor-target' id='a_" + str(title['titleID']) + "' ></span><a href='#a_" + str(title['titleID']) + "'  name='a_" + str(title['titleID']) + "' class='anchor glyphicon glyphicon-link' ></a>" + title['titleName'] + "<"
            old = old.replace("\r", "")
            i = i.replace(old, new)
        anchorHtml += i+'\n'
    return anchorHtml


def convertHtml(link, json):
    text = request.urlopen(link).read().decode('utf8')
    html = markdown.markdown(text)
    htmlJson = u"<input style='display: none' id='jsonContent' value='" + json + "'></input>"
    content = htmlHead + html + endHtml + htmlJson + htmlTail
    return content

def create(link):
    menu = getMenu(link)
    # markdown转html（生成html）
    content = convertHtml(link, json.dumps(menu))
    # 给html加锚标记
    html = addAnchorMark(menu, content)
    return html
