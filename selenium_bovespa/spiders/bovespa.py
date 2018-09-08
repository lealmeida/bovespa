# -*- coding: utf-8 -*-
import scrapy
import time
import unidecode
from scrapy.loader import ItemLoader
from selenium import webdriver
from scrapy.loader.processors import TakeFirst
from selenium.webdriver.common.keys import Keys
from selenium_bovespa.items import *  # BalancoPatrimonialAtivoItem(), BalancoPatrimonialPassivoItem(), DemonstracaoResultadoItem(), DemonstracaoResultadoAbrangenteItem(), DemonstracaoDoFluxoDeCaixaItem(), DemonstracaoDeValorAdicionadoItem()
from pymongo import MongoClient
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BovespaSpider(scrapy.Spider):
    name = 'bovespa'
    #allowed_domains = ['http://www.bmfbovespa.com.br']
    start_urls = [
        'http://www.bmfbovespa.com.br/pt_br/produtos/listados-a-vista-e-derivativos/renda-variavel/empresas-listadas.htm']
    item = {'DFs Individuais / Balanço Patrimonial Ativo - (Reais Mil)': BalancoPatrimonialAtivoItem(),
            'DFs Consolidadas / Balanço Patrimonial Ativo - (Reais Mil)': BalancoPatrimonialAtivoItem(),
            'DFs Individuais / Balanço Patrimonial Ativo - (Reais)': BalancoPatrimonialAtivoItem(),
            'DFs Consolidadas / Balanço Patrimonial Ativo - (Reais)': BalancoPatrimonialAtivoItem(),
            'DFs Individuais / Balanço Patrimonial Passivo - (Reais Mil)': BalancoPatrimonialPassivoItem(),
            'DFs Consolidadas / Balanço Patrimonial Passivo - (Reais Mil)': BalancoPatrimonialPassivoItem(),
            'DFs Individuais / Balanço Patrimonial Passivo - (Reais)': BalancoPatrimonialPassivoItem(),
            'DFs Consolidadas / Balanço Patrimonial Passivo - (Reais)': BalancoPatrimonialPassivoItem(),
            'DFs Individuais / Demonstração do Resultado - (Reais Mil)': DemonstracaoResultadoItem(),
            'DFs Consolidadas / Demonstração do Resultado - (Reais Mil)': DemonstracaoResultadoItem(),
            'DFs Consolidadas / Demonstração do Resultado - (Reais)': DemonstracaoResultadoItem(),
            'DFs Individuais / Demonstração do Resultado - (Reais)': DemonstracaoResultadoItem(),
            'DFs Individuais / Demonstração do Resultado Abrangente - (Reais Mil)': DemonstracaoResultadoAbrangenteItem(),
            'DFs Consolidadas / Demonstração do Resultado Abrangente - (Reais Mil)': DemonstracaoResultadoAbrangenteItem(),
            'DFs Individuais / Demonstração do Resultado Abrangente - (Reais)': DemonstracaoResultadoAbrangenteItem(),
            'DFs Consolidadas / Demonstração do Resultado Abrangente - (Reais)': DemonstracaoResultadoAbrangenteItem(),
            'DFs Individuais / Demonstração do Fluxo de Caixa - (Reais Mil) - Método Indireto': DemonstracaoDoFluxoDeCaixaItem(),
            'DFs Consolidadas / Demonstração do Fluxo de Caixa - (Reais Mil) - Método Indireto': DemonstracaoDoFluxoDeCaixaItem(),
            'DFs Individuais / Demonstração do Fluxo de Caixa - (Reais) - Método Indireto': DemonstracaoDoFluxoDeCaixaItem(),
            'DFs Consolidadas / Demonstração do Fluxo de Caixa - (Reais) - Método Indireto': DemonstracaoDoFluxoDeCaixaItem(),
            'DFs Consolidadas / Demonstração de Valor Adicionado - (Reais Mil)': DemonstracaoDeValorAdicionadoItem(),
            'DFs Individuais / Demonstração de Valor Adicionado - (Reais Mil)': DemonstracaoDeValorAdicionadoItem(),
            'DFs Consolidadas / Demonstração de Valor Adicionado - (Reais)': DemonstracaoDeValorAdicionadoItem(),
            'DFs Individuais / Demonstração de Valor Adicionado - (Reais)': DemonstracaoDeValorAdicionadoItem()}

    collection_name = {'EmpresaItem': 'empresa',
                       'BalancoPatrimonialAtivoItem': 'balancoPatrimonialAtivo',
                       'BalancoPatrimonialPassivoItem': 'balancoPatrimonialPassivo',
                       'DemonstracaoResultadoItem': 'demonstracaoResultado',
                       'DemonstracaoResultadoAbrangenteItem': 'demonstracaoResultadoAbrangente',
                       'DemonstracaoDoFluxoDeCaixaItem': 'demonstracaoDoFluxoDeCaixa',
                       'DemonstracaoDeValorAdicionadoItem': 'demonstracaoDeValorAdicionado'}
    
    ano = ['2017', '2016', '2015', '2014', '2013', '2012', '2011']

    def parse(self, response):
        codigoCvm = input("Digite o código cvm: ")
        driver = webdriver.Chrome()
        driver.get('http://bvmf.bmfbovespa.com.br/cias-listadas/empresas-listadas/ResumoEmpresaPrincipal.aspx?codigoCvm=%s' % codigoCvm)
        #driver = webdriver.Chrome()
        # driver.get('http://bvmf.bmfbovespa.com.br/cias-listadas/empresas-listadas/ResumoEmpresaPrincipal.aspx?codigoCvm=7617')
        time.sleep(15)

        driver.switch_to.frame(driver.find_element_by_id('ctl00_contentPlaceHolderConteudo_iframeCarregadorPaginaExterna'))
        nome = driver.find_element_by_xpath('//*[@id="accordionDados"]/table/tbody/tr[1]/td[2]')
        codigoNegociacao = driver.find_element_by_xpath('//*[@id="accordionDados"]/table/tbody/tr[2]/td[2]/a[2]')
        cnpj = driver.find_element_by_xpath('//*[@id="accordionDados"]/table/tbody/tr[3]/td[2]')
        atividadePrincipal = driver.find_element_by_xpath('//*[@id="accordionDados"]/table/tbody/tr[4]/td[2]')
        classificacaoSetorial = driver.find_element_by_xpath('//*[@id="accordionDados"]/table/tbody/tr[5]/td[2]')
        site = driver.find_element_by_xpath('//*[@id="accordionDados"]/table/tbody/tr[6]/td[2]/a')

        loader = ItemLoader(EmpresaItem())
        loader.default_output_processor = TakeFirst()
        loader.add_value('nome', nome.text)
        loader.add_value('codigoCvm', codigoCvm)
        loader.add_value('codigoNegociacao', codigoNegociacao.text)
        loader.add_value('cnpj', cnpj.text)
        loader.add_value('atividadePrincipal', atividadePrincipal.text)
        loader.add_value('classificacaoSetorial', classificacaoSetorial.text)
        loader.add_value('site', site.text)
        client = MongoClient('localhost', 27017)
        dataBase = client.bovespa
        collection = dataBase.empresa
        collection.insert_one(loader.load_item())
        client.close()

        time.sleep(5)
        driver.switch_to.default_content()
        self.relatorioFinanceiro(driver, codigoCvm)

    def relatorioFinanceiro(self, driver, codigoCvm):
        relatorioFinanceiro = driver.find_element_by_xpath('//*[@id="ctl00_contentPlaceHolderConteudo_MenuEmpresasListadas1_tabMenuEmpresa_tabRelatoriosFinanceiros"]')
        relatorioFinanceiro.click()
        time.sleep(5)
        select = Select(driver.find_element_by_xpath('//*[@id="ctl00_contentPlaceHolderConteudo_cmbAno"]'))
        for x,option in enumerate(self.ano):
            select = Select(driver.find_element_by_xpath('//*[@id="ctl00_contentPlaceHolderConteudo_cmbAno"]'))
            select.select_by_value(option)
            time.sleep(10)
            self.dadosFinanceiro(driver, codigoCvm)

    def dadosFinanceiro(self, driver, codigoCvm):
        driver.find_element_by_id("ctl00_contentPlaceHolderConteudo_rptDocumentosDFP_ctl00_lnkDocumento").click()
        time.sleep(15)
        window_before = driver.window_handles[0]
        window_after = driver.window_handles[1]
        driver.switch_to_window(window_after)
        select = Select(driver.find_element_by_xpath('//*[@id="cmbQuadro"]'))
        options = select.options
        for index in range(0, len(options)):
            select = Select(driver.find_element_by_xpath('//*[@id="cmbQuadro"]'))
            select.select_by_index(index)
            time.sleep(10)
            self.get_values(driver, codigoCvm)
        driver.close()
        driver.switch_to_window(window_before)

    def get_values(self, driver, codigoCvm):
        driver.switch_to.frame(driver.find_element_by_id('iFrameFormulariosFilho'))
        title = driver.find_element_by_xpath('//*[@id="TituloTabelaSemBorda"]').text.encode('utf8')
        client = MongoClient('localhost', 27017)
        for index, header in enumerate(driver.find_elements_by_xpath('//*[@id="ctl00_cphPopUp_tbDados"]/tbody/tr[1]/td')):
            if (index <= 1):
                continue
            loader = ItemLoader(
                self.item[title.decode('utf8')], selector=header)
            loader.default_output_processor = TakeFirst()
            loader.add_value('ano', '2018')
            loader.add_value('tipo', 'consolidado')
            loader.add_value('codigoCvm', codigoCvm)
            loader.add_value('periodo', header.text[-11:])
            if 'Mil' in driver.find_element_by_xpath('//*[@id="TituloTabelaSemBorda"]').text:
                loader.add_value('multiplicador', 'mil')
            for rown in driver.find_elements_by_xpath('//*[@id="ctl00_cphPopUp_tbDados"]/tbody/tr')[1:]:
                word = rown.find_element_by_xpath('./td[2]').text.strip().title().replace(' ', '')
                loader.add_value(unidecode.unidecode(word[0].lower() + word[1:].replace(',', '').replace('.', '')), rown.find_element_by_xpath('./td[{}]'.format(index + 1)).text.strip())
            collection = self.collection_name[type(
                self.item[title.decode('utf8')]).__name__]
            self.persist(collection, loader.load_item(), client)
            del loader
        client.close
        driver.switch_to.default_content()

    def persist(self, collection, item, client):
        dataBase = client.bovespa
        collection = dataBase[collection]
        collection.insert_one(dict(item))
