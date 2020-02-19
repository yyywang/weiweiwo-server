"""
  Created by Wesley on 2019/7/23.
"""
from contextlib import contextmanager
from sqlalchemy import Column, Integer, SmallInteger, orm, inspect
from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy, BaseQuery
from datetime import datetime

from app.libs.error_code import NotFound


class SQLAlchemy(_SQLAlchemy):
    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as ex:
            db.session.rollback()
            raise ex

class Query(BaseQuery):
    def filter_by(self, **kwargs):
        if 'status' not in kwargs.keys():
            kwargs['status'] = 1
        return super(Query, self).filter_by(**kwargs)

    def get_or_404(self, ident, description=None):
        rv = self.get(ident)
        if not rv:
            raise NotFound(msg=description)
        return rv

    def first_or_404(self, description=None):
        rv = self.first()
        if not rv:
            raise NotFound(msg=description)
        return rv

db = SQLAlchemy(query_class=Query)

class Base(db.Model):
    __abstract__ = True
    status = Column(SmallInteger, default=1)
    create_time = Column(Integer)

    def __init__(self):
        self.create_time = int(datetime.now().timestamp())

    def set_attrs(self, attrs_dict):
        for key, value in attrs_dict.items():
            if hasattr(self, key) and key != 'id':
                setattr(self, key, value)

    @property
    def create_datetime(self):
        if self.create_time:
            return datetime.fromtimestamp(self.create_time)
        else:
            return None

    def delete(self):
        self.status = 0


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
        """序列化时剔除字段"""
        for key in args:
            self._fields.remove(key)
        return self

    def append(self, *keys):
        """序列化时追加字段"""
        for key in keys:
            self._fields.append(key)
        return self

    def keys(self):
        return self._fields

    def __getitem__(self, key):
        return getattr(self, key)