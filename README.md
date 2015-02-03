# django-fly-blog
 这是一个基于django1.5的博客，开发环境为linux+python+sublime3
 
 例子: http://www.younfor.com
 
 
##功能

1. Bootstrap前端界面，多终端自动适应
2. Django自带后台+DjangoSuit风格
3. 支持文章管理，分类管理，标签，自定义页面
4. 支持博客参数自定义配置
5. 支持侧边栏插件自定义html
6. 集成Ueditor百度富文本编辑器，代码高亮
7. 支持七牛云存储
8. 支持新浪sae


##安装方法:

1. 所需要的包在flyblog/site-packages里面


        git clone git@github.com:younfor/django-fly-blog.git
        cd django-fly-blog/flyblog/site-packages
        sudo cp -r * /你的系统的site-packages或者dist-packages路径
        
　　或者在线安装
　　
    
      sudo pip install django-suit
      sudo pip install DjangoUeditor

2. 如果是sae已经配置好了，只需要在setting里面
      
　　　　　　　　sae=True

　　发布前记得

　　　　　　　　python manage.py collectstatic
　　　　　　　　
　　其他参数自行配置

3. 侧边栏小工具使用方法:新建侧边栏的时候，内容里面填右边推荐的
    
        recented_post,hot_post特定字段即可

4. 联系ＱＱ361106306

5. 版权声明，本项目开源，也借鉴了大多类似的博客源码.
