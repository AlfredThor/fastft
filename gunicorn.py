debug = False
daemon = False
bind = '0.0.0.0:8003'  # 绑定ip和端口号
backlog = 512       # 监听队列
timeout = 180      # 超时
# worker_class = 'gevent' #使用gevent模式，还可以使用sync 模式，默认的是sync模式
worker_class = 'uvicorn.workers.UvicornWorker'

workers = 2    # 进程数
threads = 4 #指定每个进程开启的线程数
loglevel = 'debug'  # 日志级别，这个日志级别指的是错误日志的级别，而访问日志的级别无法设置
access_log_format = '%(t)s %(p)s %(h)s "%(r)s" %(s)s %(L)s %(b)s %(f)s" "%(a)s"'    # 设置gunicorn访问日志格式，错误日志无法设置
chdir = '/fastft'

accesslog = "/fastft/log/gunicorn/success.log"      # 访问日志文件
errorlog = "/fastft/log/gunicorn/error.log"        # 错误日志文件
