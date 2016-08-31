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

from urllib2 import Request,urlopen
from xml.dom import minidom as dom

class FreteFacilShippingService:
	def create_deliverable(self,sender,receiver,width,height,length,weight):
		if int(height) < 2: return 'Altura abaixo do mínimo (2cm).'
		if int(width) < 11: return 'Largura abaixo do mínimo (11cm).'
		if int(length) < 16: return 'Profundidade abaixo do mínimo (16cm).'
		deliverable = {
			'sender': sender,
			'receiver': receiver,
			'width': str(width),
			'height': str(height),
			'length': str(length),
			'weight': str(weight),
		}	
		return deliverable

	def build_request(self,d):
		url = 'https://ff.paypal-brasil.com.br/FretesPayPalWS/WSFretesPayPal'
		headers = {
			'Content-Type': 'text/xml; charset=utf-8',
			'SoapAction': '%s/getPreco' % url
		}
		xml = """<soapenv:Envelope xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\" xmlns:shipping=\"https://ff.paypal-brasil.com.br/FretesPayPalWS\">
	        <soapenv:Header />
	          <soapenv:Body>
	            <shipping:getPreco>
	              <cepOrigem>%s</cepOrigem>
	              <cepDestino>%s</cepDestino>
	              <largura>%s</largura>
	              <altura>%s</altura>
	              <profundidade>%s</profundidade>
	              <peso>%s</peso>
	            </shipping:getPreco>
	          </soapenv:Body>
	        </soapenv:Envelope>""" % (d['sender'],d['receiver'],d['width'],d['height'],d['length'],d['weight'])
		return url,headers,xml

	def delivery_value(self,deliverable):
		url,headers,xml = self.build_request(deliverable)
		req = Request(url,xml,headers)
		value = urlopen(req).read()
		val = dom.parseString(value).getElementsByTagName('return')[0].childNodes[0].wholeText
		if '-2.0' in val: return 'Não foi possível calcular o frete.'
		else: return '%.2f' % float(val)