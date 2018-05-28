# -*- coding: utf-8 -*-
"""
-------------------------------------------------

@File    : test_BK.py

Description :

@Author :       pchaos

tradedate：          18-5-9
-------------------------------------------------
Change Activity:
               18-5-9:
@Contact : p19992003#gmail.com                   
-------------------------------------------------
"""
from django.test import TestCase
from stocks.models import Block


__author__ = 'pchaos'


class TestBK(TestCase):
    def setUp(self):
        Block.initBlock()

    def test_TDX(self):
        """
        默认已经初始化板块名称：通达信 同花顺 自定义 其他
        """
        bkname = '通达信'
        bk = Block.objects.all().filter(name=bkname)
        self.assertTrue(bk is not None and bk[0].name == bkname, '未找到板块:{}'.format(bkname))
        bk = Block.objects.get(name=bkname)
        self.assertTrue(bk is not None and bk.name == bkname, '未找到板块:{}'.format(bkname))
        # 测试没有此板块，抛出异常
        bkname = '没有此板块'
        # self.assertRaises(TypeError, BK.objects.get(name=bkname), '未找到板块:{}'.format(bkname))
        with self.assertRaises(Exception) as context:
            bk = Block.objects.get(name=bkname)
        self.assertTrue('query does not exist.' in str(context.exception), '{}'.format(context.exception))