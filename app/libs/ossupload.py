from flask import current_app
from  werkzeug.utils import secure_filename
import oss2
import random,datetime

app = current_app


def uploadimage(upfile,filepath=None,filename=None,bucketName = None):

    if upfile is None:
        return
    if filename is None:

        filename = tid_maker() + ".png"
    if bucketName is None:
        bucketName = app.config["OSS"]["bucketname"]

    # 上传到osss
    # 阿里云主账号AccessKey拥有所有API的访问权限，风险很高。强烈建议您创建并使用RAM账号进行API访问或日常运维，请登录 https://ram.console.aliyun.com 创建RAM账号。
    auth = oss2.Auth(app.config["OSS"]["ossid"] , app.config["OSS"]["osskey"])
    # Endpoint以杭州为例，其它Region请按实际情况填写。
    bucket = oss2.Bucket(auth , app.config["OSS"]["domain"] , app.config["OSS"]["bucketname"])
    if filepath:
        filename = filepath + filename
    upfile.seek(0)
    result = bucket.put_object(filename , upfile)
    if result.status == 200:
       return result.resp.response.url


def uploadpdf(upfile,filepath=None,filename=None,bucketName = None):

    if upfile is None:
        return
    if filename is None:
        filename = tid_maker() + ".pdf"
    if filepath is None:
        filepath = 'PDFS/'
    if bucketName is None:
        bucketName = app.config["OSS"]["bucketname"]

    # 上传到osss
    # 阿里云主账号AccessKey拥有所有API的访问权限，风险很高。强烈建议您创建并使用RAM账号进行API访问或日常运维，请登录 https://ram.console.aliyun.com 创建RAM账号。
    auth = oss2.Auth(app.config["OSS"]["ossid"] , app.config["OSS"]["osskey"])
    # Endpoint以杭州为例，其它Region请按实际情况填写。
    bucket = oss2.Bucket(auth , app.config["OSS"]["domain"] , app.config["OSS"]["bucketname"])
    if filepath:
        filename = filepath + filename
    upfile.seek(0)
    result = bucket.put_object(filename , upfile)
    if result.status == 200:
       return result.resp.response.url


def tid_maker():
    return '{0:%Y%m%d%H%M%S%f}'.format(datetime.datetime.now()) + ''.join(
        [str(random.randint(1 , 10)) for i in range(5)])