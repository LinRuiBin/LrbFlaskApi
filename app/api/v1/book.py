"""
 Created by LRB on 2018/5/7.

"""
from sqlalchemy import or_

from app.libs.redprint import Redprint
from app.models.book import Book
from app.validators.forms import BookSearchForm
from flask import jsonify
from app.libs.token_auth import auth

__author__ = 'LRB'

api = Redprint('book')


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
