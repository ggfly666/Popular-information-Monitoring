## 基于scrapy爬虫，使用django和vue3搭建的热门信息监测系统。

### 系统启动
1. 启动mysql服务
```sh
systemctl start mysql
```
2.安装python3的依赖包
```sh
pip install -r requirements.txt
```
3.安装vue3的依赖包
```sh
pnpm install
```
4.在django/setttings.py中配置数据库和发送邮件的设置,以下是一个示例：
```sh
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'xxx',
        'USER': 'xxx',
        'PASSWORD': 'xxx',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
        }
    }
}
```
```sh
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'xxx'
EMAIL_PORT = 25
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_HOST_USER = 'xxx'
EMAIL_HOST_PASSWORD = 'xxx'
```