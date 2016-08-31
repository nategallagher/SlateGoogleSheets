#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# This file is part of Efforia Open Source Initiative.
#
# Copyright (C) 2011-2014 William Oliveira de Lagos <william@efforia.com.br>
#
# Shipping is free software: you can redistribute it and/or modify
# it under the terms of the Lesser GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Shipping is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Shipping. If not, see <http://www.gnu.org/licenses/>.
#

from django.db.models import *
from django.conf import settings
from django.contrib.auth.models import User
from django.template import Context,Template
from django.utils.timezone import now

class DeliverableProperty(Model):
    class Meta:
        verbose_name_plural = "Deliverable Properties"
    sku = CharField(default='',max_length=20)
    height = IntegerField(default=16)
    length = IntegerField(default=16)
    width = IntegerField(default=16)
    weight = FloatField(default=0.1)

class Deliverable(Model):
    name = CharField(default='((',max_length=50)
    user = ForeignKey(User,related_name='+')
    product = IntegerField(default=1)
    mail_code = CharField(default='',max_length=100)
    height = IntegerField(default=1)
    length = IntegerField(default=1)
    width = IntegerField(default=1)
    weight = IntegerField(default=10)
    value = FloatField(default=0.0)
    date = DateTimeField(default=now)
    def token(self): return self.name[:2]
    def name_trimmed(self): return self.name.split(';')[0][1:]
    def month(self): return date.strftime('%b')
