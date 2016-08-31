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

import urllib
from beautifulsoup import BeautifulStoneSoup as BSS

FORMATOS = {
    'PACOTE': 1,
    'ROLO': 2,
}

SERVICOS = {
    'PAC':'41106',
    'SEDEX':'40010',
    'SEDEX10':'40215',
    'SEDEXHOJE':'40290',
    'SEDEXCOBRAR':'40045',
    'ALL': '41106,40010,40215,40290,40045',
}

class CorreiosShippingService(object):
    def __init__(self, cep_origem='80050370'):
        #ceps
        self.cep_origem = cep_origem
        self.cep_destino = None
        
        #servicos
        self.aviso_recebimento = 'N'
        self.valor_declarado = 0
        self.mao_propria = 'N'
        self.servico = 'ALL'

        #medidas
        self.formato = 'PACOTE'
        self.altura = 0
        self.largura = 0
        self.comprimento = 0
        self.diametro = 0
        self.peso = 0.3

        #configs
        self.empresa = '' #id da empresa, quando possui contrato
        self.senha = ''   #senha
        self.tipo = 'xml'
        self.URL = 'http://ws.correios.com.br/calculador/CalcPrecoPrazo.aspx'
        
        self.response = None
        self.hash = {}
        self.results = {}
        self.errors = {}

    def __call__(self, cep_destino=None, servico=None,):
        """
        Call :)
        """
        if cep_destino:
            self.cep_destino = cep_destino

        # pega o codigo do servico p/ envio ao webservice
        if servico and SERVICOS.has_key(servico):
            self.servico = servico
        
        # valida medidas e pesos minimos
        self._validate()

        # prepara o hash para envio
        self._build_hash()

        # envia os parametros e recupera o retorno
        self._request()

        # processa o resultado
        self._parse()


    def _build_hash(self):
        """
        Cria hash com dados instanciados
        """
        h = self.hash
        h['nCdEmpresa'] = self.empresa
        h['sDsSenha'] = self.senha
        h['strRetorno'] = self.tipo
        h['sCdMaoPropria'] = self.mao_propria
        h['nVlValorDeclarado'] = self.valor_declarado
        h['sCdAvisoRecebimento'] = self.aviso_recebimento
        h['nCdFormato'] = FORMATOS[self.formato]
        h['sCepOrigem'] = self.cep_origem
        h['sCepDestino'] = self.cep_destino
        h['nCdServico'] = SERVICOS[self.servico]
        h['nVlAltura'] = self.altura
        h['nVlLargura'] = self.largura
        h['nVlComprimento'] = self.comprimento
        h['nVlDiametro'] = self.diametro
        h['nVlPeso'] = self.peso
        self.hash = h


    def _validate(self):
        """ Valida as medidas (apenas os minimos)
        para calculo
        """

        peso_minimo = 0.3
        if self.formato == 'ROLO':
            comprimento_minimo = 18
            diametro_minimo = 5
            altura_minima = 0
            largura_minima = 0
        else:
            comprimento_minimo = 16
            diametro_minimo = 0
            altura_minima = 2
            largura_minima = 5

        if self.diametro < diametro_minimo:
            self.diametro = diametro_minimo

        if self.altura < altura_minima:
            self.altura = altura_minima

        if self.comprimento < comprimento_minimo:
            self.comprimento = comprimento_minimo

        # altura nao pode ser maior que comprimento
        if self.altura > self.comprimento:
            self.altura = self.comprimento

        if self.largura < largura_minima:
            self.largura = largura_minima

        # largura nao pode ser menor que 11cm quando o comprimento
        # for menor que 25cm (apenas no formato PACOTE)
        if self.formato == 'PACOTE' and self.largura < 11 \
            and self.comprimento < 25:
            self.largura = 11

        if self.peso < peso_minimo:
            self.peso = peso_minimo


    def _request(self):
        """ 
        Realiza a requisicao ao webservice e recupera
        o retorno
        """
        url = '%s?%s' %(self.URL, urllib.urlencode(self.hash))
        self.response = urllib.urlopen(url).read()


    def _parse(self):
        """
        Processa o xml retornado pelo webservice
        utilizando o BeautifulSoup

        Exemplo do retorno:
            <cServico>
                <Codigo>40045</Codigo>
                <Valor>12,10</Valor>
                <PrazoEntrega>1</PrazoEntrega>
                <ValorMaoPropria>0,00</ValorMaoPropria>
                <ValorAvisoRecebimento>0,00</ValorAvisoRecebimento>
                <ValorValorDeclarado>1,00</ValorValorDeclarado>
                <EntregaDomiciliar>S</EntregaDomiciliar>
                <EntregaSabado>S</EntregaSabado>
                <Erro>0</Erro>
                <MsgErro></MsgErro>
            </cServico>
        """
        self.xmltree = BSS(self.response, selfClosingTags=[],
                    convertEntities=BSS.ALL_ENTITIES)

        for result in self.xmltree('cservico'):
            servico_id = result('codigo')[0].contents[0]
            prazo = result('prazoentrega')[0].contents[0]
            valor = result('valor')[0].contents[0]
            erro = result('erro')[0].contents[0]
            servico = [k for k in SERVICOS if SERVICOS[k] == servico_id][0]

            #outras opcoes disponiveis no retorno:
            #valor_mao_propria = result('valormaopropria')[0].contents[0]
            #valor_aviso_recebimento = result('valoravisorecebimento')[0].contents[0]
            #valor_valor_declarado = result('valorvalordeclarado')[0].contents[0]
                        
            if erro != u'0':
                msgerro = result('msgerro')[0].contents[0]
                self.errors[servico] = msgerro
            else:
                self.results[servico] = prazo, valor


    def print_results(self):
        """
        Imprime o resultado no terminal
        """
        if self.results:
            print 'Resultados:'
            for k, v in self.results.iteritems():
                prazo, valor = v
                print '%s - %s dias - R$ %s' %(k, prazo, valor)
        
        if self.errors:
            print 'Erros:'
            for k, v in self.errors.iteritems():
                print '%s - %s' %(k, v)
