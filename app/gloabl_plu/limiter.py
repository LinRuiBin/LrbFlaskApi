from flask import request

from flask_limiter import Limiter

from app import limiter


# @limiter.request_filter这个装饰器只是将一个函数标记为将要测试速率限制的请求的过滤器。如果任何请求过滤器返回True，
# 则不会对该请求执行速率限制。此机制可用于创建自定义白名单。

@limiter.request_filter #ip白名单
def ip_whitelist():
    return request.remote_addr == "127.0.0.1"


@limiter.request_filter
def header_whitelist(): #请求头白名单
    return request.headers.get("X-Internal", "") == "true"
