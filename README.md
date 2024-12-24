## 内网文件快速互传

---

## 介绍


> 无需登录、无需注册、速度非常快,在内网测试中上传速度可以达到60M/S,下载速度可以达到恐怖的120M/S.
> 原本是用来互传大文件使用的,在此功能的基础上拓展支持不足1MB的小文件.
> 核心的文件,后端在/app/file/file.py中, 前端在/templates/list.html

---

## 参考

https://github.com/lsm1103/pyupload

---

## 在Docker中部署

> 在项目跟文件目录下操作,确保拥有Python:3.12的镜像

- 构建容器

```shell
docker build -t fastft .
```

- 运行容器

```shell
docker run -itd -p 8080:8080 -p 9001:9001 --name fastft-container fastft
```

- 在容器内启动项目

```shell
# 進入容器
docker exec -it fastft /bin/bash

# 启动supervisor
service supervisor start

# 启动gunicorn
supervisorctl start gunicorn

# 启动nginx
nginx
```

- Supervisor的可視化管理頁面

> 登陸帳號密碼在supervisord.conf文件的下方,可以自行編輯

```shell
# 替換為你的IP地址即可
http:/0.0.0.0:/9001
```
---