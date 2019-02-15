from app.models.user import User
from app.admin.admin_base import MyModelView


class UserAdmin(MyModelView):
    print()
    action_disallowed_list = ['delete']
    column_display_pk = True
    can_delete = False
    can_create = False

    column_list = [
        'id',
        'email',
        'nickname',
        'auth',
        'phone',
    ]

    column_default_sort = ('id',True)
    column_searchable_list = [
        'id',
        'email',
        'nickname',
        'phone',
    ]

    column_filters = [
        'email',
        'nickname',
        'phone',
    ]

    column_labels = {
        'id': 'id',
        'email': '邮箱',
        'nickname': '昵称',
        'auth': '权限',
        'phone': '电话',
        'status': '状态',

    }

    def __init__(self, session):
        # Just call parent class with predefined model.
        super(UserAdmin, self).__init__(User, session,name='用户管理')