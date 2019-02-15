from flask_admin import BaseView,helpers, expose
from flask import url_for
class GiftAdmin(BaseView):
    @expose('/', methods=['GET', 'POST'])
    def index(self):
        return self.render('admin/custorm_gitf.html',hello='admin 传参')

    def __init__(self):
        # Just call parent class with predefined model.
        super(GiftAdmin, self).__init__(name='礼物管理(自定义界面示范)')