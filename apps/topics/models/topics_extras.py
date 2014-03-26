# coding: utf-8

from django.db import models
from apps.mediacontent.models import MediaContents


#############################################################################################################
# Модель Расширения Тем
class TopicsExtras(models.Model):

    media_content = models.ForeignKey(MediaContents,verbose_name = u"Медиа контент")
    topic = models.ForeignKey('Topics', verbose_name = u'Тема')
    description = models.TextField(verbose_name = u'Описание')
    etype = models.IntegerField(verbose_name = u'Тип')


    def __unicode__(self):
        return u'[{}] {} {}'.format(self.pk, self.media_content.name,self.topic.name)

    class Meta:
        # Имя таблицы в БД
        db_table = 'topics_extras'
        app_label = 'topics'
        verbose_name = u'Дополнительный материал Темы'
        verbose_name_plural = u'Дополнительные материалы Тем'

