"""
 Created by LRB on 2018/5/7.

"""
from app.libs.error_code import NotFound

__author__ = 'LRB'

"""
 Created by LRB on 2018-3-11.
"""
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy, BaseQuery
from sqlalchemy.ext.associationproxy import _AssociationList
from sqlalchemy import inspect, Column, Integer, SmallInteger, orm
from contextlib import contextmanager


class SQLAlchemy(_SQLAlchemy):
    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e


class Query(BaseQuery):
    def filter_by(self, **kwargs):
        if 'status' not in kwargs.keys():
            kwargs['status'] = 1
        return super(Query, self).filter_by(**kwargs)

    def get_or_404(self, ident):
        rv = self.get(ident)
        if not rv:
            raise NotFound()
        return rv

    def first_or_404(self):
        rv = self.first()
        if not rv:
            raise NotFound()
        return rv


db = SQLAlchemy(query_class=Query)


class Base(db.Model):
    __abstract__ = True
    create_time = Column(db.DateTime, default=datetime.now)
    status = Column(SmallInteger, default=1)
    update_time = Column(db.DateTime , default=datetime.now , onupdate=datetime.now)

    def __init__(self):
        pass
        # self.create_time = datetime.now()
        # self.create_time = int(datetime.now().timestamp())

    def __getitem__(self, item):
        attr = getattr(self, item)
        if len(self.fields)>0 and isinstance(attr, _AssociationList):
            return list(attr)
        return getattr(self, item)

    @property
    def create_datetime(self):
        if self.create_time:
            return datetime.fromtimestamp(self.create_time)
        else:
            return None

    def set_attrs(self, attrs_dict):
        for key, value in attrs_dict.items():
            if hasattr(self, key) and key != 'id':
                setattr(self, key, value)

    def delete(self):
        self.status = 0

    def keys(self):
        return self.fields

    def hide(self, *keys):
        for key in keys:
            self.fields.remove(key)
        return self

    def update_fields(self,*ufields):
        if ufields:
            self.fields = list(ufields)
        return self

    def append(self, *keys):
        for key in keys:
            self.fields.append(key)
        return self



# 如果模型继承 db.model 则可多继承 MixinJSONSerializer 重写 _set_fields 方法 给 _fields 等赋值即可
class MixinJSONSerializer:
    @orm.reconstructor
    def init_on_load(self):
        self._fields = []
        # self._include = []
        self._exclude = []

        self._set_fields()
        self.__prune_fields()

    def _set_fields(self):
         pass

    def __prune_fields(self):
        columns = inspect(self.__class__).columns
        if not self._fields:
            all_columns = set(columns.keys())
            self._fields = list(all_columns - set(self._exclude))

    def hide(self, *args):
        for key in args:
            self._fields.remove(key)
        return self

    def keys(self):
        return self._fields

    def __getitem__(self, key):
        attr = getattr(self, key)
        if len(self._fields) > 0 and isinstance(attr, _AssociationList):
            return list(attr)
        return getattr(self, key)
