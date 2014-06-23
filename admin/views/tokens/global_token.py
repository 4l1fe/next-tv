# coding: utf-8
from admin.views.base import BaseModelView
from models.tokens import GlobalToken


class GlobalTokenModelView(BaseModelView):
    model = GlobalToken
    category = u'Токены пользователя'
    name = u'Токен пользователя'

    can_edit = False

    column_list = ('token', 'users', 'created')

    column_labels = dict(token=u'Токен', users=u'Пользователь',
                         created=u'Дата создания')

    form_columns = ('users', )

