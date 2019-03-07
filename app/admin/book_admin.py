from app.models.book import Book
from app.admin.admin_base import MyModelView
from jinja2 import Markup

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
     'summary',
     'image'
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

    def __init__(self, session):
        # Just call parent class with predefined model.
        super(BookAdmin, self).__init__(Book, session,name='书籍管理')