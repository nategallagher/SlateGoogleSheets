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

from django.http import HttpResponse as response
from django.core.mail import send_mail

def send_invoice(request):
	send_mail('Subject here', 'Here is the message.','contato@efforia.com.br',
    ['william.lagos1@gmail.com'], fail_silently=False)
	return response('E-mail sended.')