"""
celery -A app.celery beat
celery -A app.celery worker
"""

from celery.schedules import crontab


broker_url = "redis://localhost:6379/1"   # 使用redis存储任务队列
result_backend = "redis://localhost:6379/1"  # 使用redis存储结果

task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
timezone = "Asia/Shanghai"  # 时区设置
worker_hijack_root_logger = True  # celery默认开启自己的日志，可关闭自定义日志，不关闭自定义日志输出为空
result_expires = 60 * 60 * 24  # 存储结果过期时间（默认1天）

# 导入任务所在文件
imports = [
    "app.celery.tasks",  # 导入py文件
]

# 需要执行任务的配置
beat_schedule = {
    "test1": {
        "task": "app.celery.tasks.tetstCelery",  #执行的函数
        "schedule": crontab(minute=0, hour="*/6"),   # every minute 每分钟执行
        "args": ()  # # 任务函数参数
    },
}

"""
"schedule": crontab（）与crontab的语法基本一致
"schedule": crontab(minute="*/10",  # 每十分钟执行
"schedule": crontab(minute="*/1"),   # 每分钟执行
"schedule": crontab(minute=0, hour="*/1"),    # 每小时执行
--------------------- 
作者：Shyllin 
来源：CSDN 
原文：https://blog.csdn.net/Shyllin/article/details/80940643 
版权声明：本文为博主原创文章，转载请附上博文链接！

"""