# About this project
**Flask实现的基于[Microsoft Graph](https://docs.microsoft.com/zh-cn/graph/)(OneDrive API)的个人博客，能够实现本地文件映射为博文，电脑端随时创建，随时修改，随时同步，只需一个`Ctrl+s`。可以非常方便地编辑博客。**
![](https://img.one/image/5f95052ad308e.jpg)

+ 图片方案：`http://blog.zr.codes/<title>/<image>`
    
    只需把图片放至文章相应目录，`markdown`中写：
    
    - `![](image.jpg)` （写这个只能在博客和本地看到）
    - 或`![](http://blog.zr.codes/title/image.jpg)`（通用，使用前保证图片已经通过OneDrive同步）

+ 视频播放
    集成`DPlayer`，将想插入的视频文件防止博客对应目录，在`md`文件中写一行标签即可
    `<div id="dplayer" src="1.mp4"></div>`
    
    **[视频图片测试](http://blog.zr.codes/blog/视频图片测试-project/)**

# 运行环境
## **无服务器运行**
借由[serverless-components/tencent-flask](https://github.com/serverless-components/tencent-flask)项目部署于腾讯云函数（SCF-ap-Hongkong）
