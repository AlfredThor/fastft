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

## 常规方式启动

> 常规方式启动非常的方便,克隆该项目后安装requirements.txt中的包,直接运行main.py即可

```shell
# 克隆项目  
git clone https://github.com/AlfredThor/fastft.git

# 进入项目的目录
cd fastft

# 安装所需的包
pip install -r requirements.txt

# 运行项目
python main.py
```

---

## 在Docker中部署

> 在项目跟文件目录下操作,确保拥有Python:3.12的镜像

- 克隆倉庫並進入到操作目錄并构建容器

```shell
# 克隆项目  
git clone https://github.com/AlfredThor/fastft.git

# 进入项目的目录
cd fastft

# 构建镜像
docker build -t fastft .
```

- 启动容器并进入容器内操作

```shell
# 启动一个容器设置8080和9001两个端口映射 并将容器名命名为fastft-container
docker run -itd -p 8080:8080 -p 9001:9001 --name fastft-container fastft

# 進入容器
docker exec -it fastft-container /bin/bash

# 启动supervisor
service supervisor start

# 查看gunicorn是否启动,一般会随着supervisor自行启动
supervisorctl status gunicorn

# 启动nginx
nginx
```
- 启动失败如何排查问题

> 确保在容器内,查看/fastft/log文件夹,分别有gunicorn、nginx、supervisor文件,如果你不知道问题出在
> 哪里那么排查顺序是: supervisor -> gunicorn -> nginx supervisor文件夹中只有一个文件直接查
> 看即可,gunicorn和nginx中都有error.log文件,确保依次查看

- Supervisor可視化管理頁面

> 登陸帳號密碼在supervisord.conf文件的下方,可以自行編輯

```shell
# 替換為你的IP地址即可
http:/0.0.0.0:/9001
```

---