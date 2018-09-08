# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

from scrapy.loader.processors import Join
from scrapy.item import BaseItem


class EmpresaItem(dict, BaseItem):
    pass


class BalancoPatrimonialAtivoItem(dict, BaseItem):
    pass


class BalancoPatrimonialPassivoItem(dict, BaseItem):
    pass


class DemonstracaoResultadoItem(dict, BaseItem):
    pass



class DemonstracaoResultadoAbrangenteItem(dict, BaseItem):
    pass



class DemonstracaoDoFluxoDeCaixaItem(dict, BaseItem):
    pass



class DemonstracaoDeValorAdicionadoItem(dict, BaseItem):
    pass