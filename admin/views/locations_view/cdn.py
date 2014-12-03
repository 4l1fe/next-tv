# coding: utf-8

from wtforms.fields import StringField

from admin.views.base import SqlAlModelView
from models.cdn import CDN


class CdnModelView(SqlAlModelView):
    model = CDN
    category = u'Справочники'
    name = u'CDN'

    named_filter_urls = True

    column_filters = (
        'name', 'has_mobile', 'has_auth',
    )

    column_labels = dict(
        name=u'Название',
        description=u'Описание',
        cdn_type=u'Тип',
        url=u'URL адресс',
        has_mobile=u'Для мобильных устройств',
        has_auth=u'Необходима авторизация',
        location_regxp=u'Регулярное вырожожение для локации',
    )

    column_list = (
        'name', 'has_mobile', 'has_auth', 'cdn_type',
        'url', 'location_regxp', 'description',
    )

    form_columns = (
        'name', 'has_mobile', 'has_auth', 'cdn_type',
        'url', 'location_regxp', 'description',
    )

    form_excluded_columns = ('extras', 'media_locations', )

    form_overrides = dict(
        name=StringField,
    )