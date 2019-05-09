from app import app
import os

#蓝图 v1
def register_blueprints(app):
    from app.api.v1 import create_blueprint_v1,docApis_v1
    from app.api.upload.Ueditor import route_upload
    from app.web.web import web_route

    app.register_blueprint(create_blueprint_v1(), url_prefix='/v1')
    app.register_blueprint(route_upload,url_prefix = "/upload")
    app.register_blueprint(web_route , url_prefix="/")

# 插件初始化
def register_plugin(app):
    create_apidoc(app)
    # create_dbdata(app)  #在创建app的时候注册db 这里不用
    create_admin(app)
    createUserManager(app)

    from flask_bootstrap import Bootstrap
    Bootstrap(app=app)

# 自动生成文档 /docs/api/ debug模式下显示
def create_apidoc(app):
    from flask_docs import ApiDoc
    from app.api.v1 import docApis_v1

    docapis = list(set([] + docApis_v1))
    app.config['API_DOC_MEMBER'] = docapis
    app.config['RESTFUL_API_DOC_EXCLUDE'] = []
    ApiDoc(app)

#数据库
def create_dbdata(app):
    from app.models.base import db
    db.init_app(app)
    with app.app_context():
        db.create_all()


#自动管理平台
def create_admin(app):
    from app.admin import init_admin
    from flask_babelex import Babel

    init_admin(app)
    Babel(app)


#usermanager
def createUserManager(app):

    from app.libs.UrlManager import UrlManager

    app.add_template_global(UrlManager.buildStaticUrl , 'buildStaticUrl')
    app.add_template_global(UrlManager.buildUrl , 'buildUrl')
    app.add_template_global(UrlManager.buildImageUrl , 'buildImageUrl')


def registerModules():
    register_blueprints(app)
    register_plugin(app)


registerModules()