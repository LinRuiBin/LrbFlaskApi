from flask import Blueprint

from flask import request,jsonify,json
import re
import oss2

from app import get_app
app = get_app()

route_upload = Blueprint('upload_page', __name__)

@route_upload.route("/ueditor",methods = [ "GET","POST" ])
def ueditor():
    req = request.values
    action = req['action'] if 'action' in req else ''
    if action == "config":
        root_path = app.root_path
        config_path = "{0}/static/plugins/ueditor/upload_config.json".format(root_path)
        with open(config_path , encoding="utf-8") as fp:
            try:
                config_data = json.loads(re.sub(r'\/\*.*\*/' , '' , fp.read()))
            except:
                config_data = {}
        return jsonify(config_data)

    if action == "uploadimage":
        return ueditor_uploadImage()


def ueditor_uploadImage():
    req = request
    resp = {'state': 'SUCCESS' , 'url': '' , 'title': '' , 'original': ''}
    file_target = request.files
    upfile = file_target['upfile'] if 'upfile' in file_target else None
    if upfile is None:
        resp['state'] = "上传失败"
        return jsonify(resp)

    # 上传到osss
    # 阿里云主账号AccessKey拥有所有API的访问权限，风险很高。强烈建议您创建并使用RAM账号进行API访问或日常运维，请登录 https://ram.console.aliyun.com 创建RAM账号。
    auth = oss2.Auth(app.config["OSS"]["ossid"] , app.config["OSS"]["osskey"])
    # Endpoint以杭州为例，其它Region请按实际情况填写。
    bucket = oss2.Bucket(auth , app.config["OSS"]["domain"] , app.config["OSS"]["bucketname"])
    filename = "book_image/" + upfile.filename
    upfile.seek(0)
    result = bucket.put_object(filename , upfile)
    if result.status == 200:
        resp['url'] = result.resp.response.url

    return jsonify(resp)


