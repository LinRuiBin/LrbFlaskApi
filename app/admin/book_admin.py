from app.models.book import Book
from app.admin.admin_base import MyModelView
from jinja2 import Markup
from wtforms import fields, widgets

class CKTextAreaWidget(widgets.TextArea):
    def __call__(self, field, **kwargs):
        # add WYSIWYG class to existing classes
        kwargs.setdefault('id', 'editor')
        existing_classes = kwargs.pop('class', '') or kwargs.pop('class_', '')
        kwargs['class'] = '{} {}'.format(existing_classes,"editor")
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)


class CKTextAreaField(fields.TextAreaField):
     widget = CKTextAreaWidget()



class BookAdmin(MyModelView):

    column_display_pk = True
    column_list = [
     'id',
     'title',
     'author',
     'binding',
     'publisher',
     'price',
     'pages',
     'pubdate',
     'isbn',
     'image'
     'summary',
    ]

    column_default_sort = ('id',True)
    column_searchable_list = [
        'title',
        'author',
        'publisher',
        'isbn',
    ]

    column_filters = [
        'title',
        'author',
        'publisher',
        'isbn',
    ]

    column_labels = {
     'id':'id',
     'title':'书名',
     'author':'作者',
     'binding':'binding',
     'publisher':'出版社',
     'price':'价格',
     'pages':'页数',
     'pubdate':'出版日期',
     'isbn':'编号牌',
     'summary':'摘要',
     'image':'图片',
    }

    def _list_image(view, context, model, name):
        if not model.image:
            return ''
        return Markup('<img src="%s" height="100" width="80" >' % model.image)

    column_formatters = {
        'image': _list_image
    }

    form_overrides = {
        'summary': CKTextAreaField
    }
    create_template = 'admin/create_book.html'

    def __init__(self, session):
        # Just call parent class with predefined model.
        super(BookAdmin, self).__init__(Book, session,name='书籍管理')