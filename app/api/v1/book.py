"""
 Created by LRB on 2018/5/7.

"""
from sqlalchemy import or_

from app.libs.redprint import Redprint
from app.models.book import Book
from app.validators.forms import BookSearchForm
from flask import jsonify,request
from app.libs.token_auth import auth
from app.libs.paginate import iPagination
from app.libs.error_code import SuccessReponse
from app import get_app

__author__ = 'LRB'

api = Redprint('book')

app = get_app()


@api.route('/search')
def search():
    """
    搜索书籍
    模糊搜索 标题 出版社
    :param q
    :return:
    """
    form = BookSearchForm().validate_for_api()
    q = '%' + form.q.data + '%'
    # book = Book()
    # 元类 ORM
    books = Book.query.filter(
        or_(Book.title.like(q), Book.publisher.like(q))).all()
    books = [book.hide('summary') for book in books]
    return jsonify(books)


@api.route('/<isbn>/detail')
@auth.login_required
def detail(isbn):
    book = Book.query.filter_by(isbn=isbn).first_or_404()
    return jsonify(book)


@api.route('/', methods=['GET'])
def books():

    req = request.values
    page = int(req['p']) if ('p' in req and req['p']) else 1
    query = Book.query

    page_params = {
        'total': query.count(),
        'page_size': app.config['PAGE_SIZE'],
        'page': page,
        'display': app.config['PAGE_DISPLAY'],
        'url': request.full_path.replace("&p={}".format(page), "")
    }

    pages = iPagination( page_params )
    pages.pop('range')
    offset = ( page - 1 ) * app.config['PAGE_SIZE']
    list = query.order_by(Book.id).offset(offset).limit(app.config['PAGE_SIZE']).all()
    list = [book.update_fields('id','title', 'image','summary') for book in list]
    data = list
    return SuccessReponse(data=data,msg="获取成功")


