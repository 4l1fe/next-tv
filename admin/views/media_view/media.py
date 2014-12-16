# coding: utf-8

from flask.ext.admin.form import fields

from admin.filters import ChoiceEqualFilter, MediaUnitFilter
from admin.fields import CKTextAreaField
from admin.views.base import SqlAlModelView
from admin.templates import media_link_formatter

from models.media.media import Media
from models.media.constants import APP_MEDIA_TYPE, APP_MEDIA_LIST


class MediaModelView(SqlAlModelView):
    model = Media
    category = u'Медиа-объекты'
    name = u'Медиа'

    named_filter_urls = True

    column_list = (
        'title', 'type_', 'access_type', 'release_date',
        'duration', 'owner', 'access', 'poster',
        'views_cnt', 'allow_mobile', 'allow_smarttv',
        'allow_external', 'allow_anon', 'link', 'created',
    )

    column_filters = (
        'title', ChoiceEqualFilter(Media.type_, u'Тип', APP_MEDIA_TYPE),
        ChoiceEqualFilter(Media.access_type, u'Тип доступа', APP_MEDIA_LIST),
        'release_date', 'allow_mobile', 'allow_smarttv',
        'allow_external', 'allow_anon', MediaUnitFilter(Media.id, u'Media Unit'),
    )

    column_choices = dict(
        type_=APP_MEDIA_TYPE,
        access_type=APP_MEDIA_LIST,
    )

    column_labels = dict(
        title=u'Заголовок', link=u'',
        title_orig=u'Оригинальное название',
        allow_mobile=u'Доступны на моб.телефонах',
        allow_smarttv=u'Доступны на Smart TV',
        allow_external=u'Доступны внешние ссылки',
        allow_anon=u'Доступна анонимность',
        views_cnt=u'Количество просмотров',
        release_date=u'Дата выхода', poster=u'Постер',
        duration=u'Продолжительность', owner=u'Владелец',
        created=u'Дата создания', type_=u'Тип',
        access=u'Доступ', access_type=u'Тип доступа',
        description=u'Описание',
    )

    column_formatters = {
        'link': media_link_formatter
    }

    form_columns = (
        'title', 'title_orig', 'release_date', 'poster',
        'duration', 'owner', 'type_', 'access',
        'access_type', 'allow_mobile', 'allow_smarttv',
        'allow_external', 'allow_anon', 'description',
    )

    form_overrides = dict(
        type_=fields.Select2Field,
        access_type=fields.Select2Field,
        description=CKTextAreaField,
    )

    form_args = dict(
        type_=dict(
            choices=APP_MEDIA_TYPE,
        ),
        access_type=dict(
            choices=APP_MEDIA_LIST,
        ),
    )

    form_ajax_refs = dict(
        owner={
            'fields': ('firstname', 'lastname',),
        },
    )
