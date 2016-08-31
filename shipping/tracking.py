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


import re,urllib2
from beautifulsoup import BeautifulSoup

class EncomendaRepository(object):
        
    def __init__(self):
        from scraping import CorreiosWebsiteScraper
        self.correios_website_scraper = CorreiosWebsiteScraper()
    
    def get(self, numero):
        return self.correios_website_scraper.get_encomenda_info(numero)

class Encomenda(object):
    
    def __init__(self, numero):
        self.numero = numero
        self.status = []
    
    def adicionar_status(self, status):
        self.status.append(status)
        self.status.sort(lambda x, y: 1 if x.data > y.data else -1)
    
    def ultimo_status_disponivel(self):
        return self.status[len(self.status) - 1] if len(self.status) > 0 else None

    def primeiro_status_disponivel(self):
        return self.status[0] if len(self.status) > 0 else None

class Status(object):
    
    def __init__(self, **kwargs):
        self.data = kwargs.get('data')
        self.local = kwargs.get('local')
        self.situacao = kwargs.get('situacao')
        self.detalhes = kwargs.get('detalhes')

class Correios:
    def __init__(self): pass

class CorreiosWebsiteScraper(object):
    
    def __init__(self, http_client=urllib2):
        self.url = 'http://websro.correios.com.br/sro_bin/txect01$.QueryList?P_ITEMCODE=&P_LINGUA=001&P_TESTE=&P_TIPO=001&P_COD_UNI='
        self.http_client = http_client
        
    def get_encomenda_info(self, numero):
        request = self.http_client.urlopen('%s%s' % (self.url, numero))
        html = request.read()
        request.close()
        if html:
            encomenda = Encomenda(numero)
            [encomenda.adicionar_status(status) for status in self._get_all_status_from_html(html)]
            return encomenda
    
    def _get_all_status_from_html(self, html):
        html_info = re.search('.*(<table.*</TABLE>).*', html, re.S)
	try:
	        table = html_info.group(1)
	except AttributeError,e:
		return [-1]
        
        soup = BeautifulSoup(table)
        
        status = []
        count = 0
        for tr in soup.table:
            if count > 4 and str(tr).strip() != '':
                if re.match(r'\d{2}\/\d{2}\/\d{4} \d{2}:\d{2}', tr.contents[0].string):
                    status.append(
                            Status(data=unicode(tr.contents[0].string),
                                    local=unicode(tr.contents[1].string),
                                    situacao=unicode(tr.contents[2].font.string))
                    )
                else:
                    status[len(status) - 1].detalhes = unicode(tr.contents[0].string)
                    
            count = count + 1
        
        return status
