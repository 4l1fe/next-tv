# coding: utf-8
from flask.ext.admin.form import fields
from admin.views.base import SqlAlModelView
from models.eshop.items.items_objects import ItemsObjects
from models.comments.constants import OBJECT_TYPES


class ItemsObjectsModelView(SqlAlModelView):
    model = ItemsObjects
    category = u'Магазин'
    name = u'Отношение элементов и объектов'

    column_list = form_columns = ('items', 'obj_type', 'obj_id', 'obj_name',)

    column_labels = dict(
        items=u'Элемент',
        obj_type=u'Тип объекта',
        obj_id=u'Идентификатор объекта',
        obj_name=u'Название объекта',
    )

    form_overrides = dict(
        obj_type=fields.Select2Field,
    )

    column_choices = dict(
        obj_type=OBJECT_TYPES,
    )

    form_args = dict(
        obj_type=dict(
            choices=OBJECT_TYPES,
        ),
    )
