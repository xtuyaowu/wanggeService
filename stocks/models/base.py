# -*- coding: utf-8 -*-
"""
-------------------------------------------------

@File    : base.py

Description : 基础类

@Author :       pchaos

date：          18-6-5
-------------------------------------------------
Change Activity:
               18-6-5:
@Contact : p19992003#gmail.com                   
-------------------------------------------------
"""
__author__ = 'pchaos'

from django.db import models
from django.db import transaction
import pandas as pd
import datetime

class StockBase(models.Model):
    """ StockBase为所有model的基类，提供共用的类函数

    """
    @classmethod
    def saveModel2File(cls, filename=None, dropPk=True):
        if not filename:
            filename = '{}_{}.pkl.gz'.format(cls.__name__, datetime.datetime.now().date())
        from django.forms import model_to_dict
        aobjs = [model_to_dict(aobj) for aobj in cls.objects.all()]
        df = pd.DataFrame(aobjs)
        cls.dropDataframePK(df, dropPk)
        df.to_pickle(filename)
        return filename

    @classmethod
    def loadModelFromFile(cls, filename=None, dropPk=True):
        if filename:
            df = pd.read_pickle(filename)
            cls.dropDataframePK(df, dropPk)
            entries = df.to_dict('records')
            with transaction.atomic():
                for v in entries:
                    cls.objects.get_or_create(**v)
        else:
            print('文件名为空，请传正确的文件名！')

    @staticmethod
    def dropDataframePK(df, dropPk):
        """ 删除无明确意义的主键字段.
        如果是有业务逻辑意义的主键不能删除

        :param df:
        :param dropPk:
        :return:
        """
        if dropPk:
            pkname = 'id'
            if pkname in list(df.columns):
                #  主键在保存的dataFrame中
                df.drop(pkname, axis=1, inplace=True)

    class Meta:
        abstract = True