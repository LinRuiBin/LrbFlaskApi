"""
 Created by LRB on 2018/5/7.
"""
from .app import Flask
__author__ = 'LRB'

_cache = {}

#蓝图 v1
def register_blueprints(app):
    from app.api.v1 import create_blueprint_v1,docApis_v1
    app.register_blueprint(create_blueprint_v1(), url_prefix='/v1')

# 插件初始化
def register_plugin(app):
    create_apidoc(app)
    create_dbdata(app)
    create_admin(app)

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


def create_app():
    app = Flask(__name__,template_folder='templates',)
    app.config.from_object('app.config.setting')
    app.config.from_object('app.config.secure')

    _cache['app'] = app

    register_blueprints(app)
    register_plugin(app)
    return app


# 防止循环引用
def get_app():
    return _cache['app']