# -*- coding: utf-8 -*-
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys

from core import jsontools as json
from core import scrapertools
from core import servertools
from core.item import Item
from platformcode import config, logger
from core import httptools
from core import tmdb

host = 'http://yuuk.net'

def mainlist(item):
    logger.info()
    itemlist = []
    itemlist.append( Item(channel=item.channel, title="Peliculas" , action="peliculas", url=host))
    itemlist.append( Item(channel=item.channel, title="Categorias" , action="categorias", url=host + "/list-genres/"))
    itemlist.append( Item(channel=item.channel, title="Buscar" , action="search"))
    return itemlist


def search(item, texto):
    logger.info()
    texto = texto.replace(" ", "+")
    item.url = host+ "/?s=%s" % texto
    try:
        return peliculas(item)
    except:
        import sys
        for line in sys.exc_info():
            logger.error("%s" % line)
        return []


def categorias(item):
    logger.info()
    itemlist = []
    data = httptools.downloadpage(item.url).data
    itemlist.append( Item(channel=item.channel, title="Censored" , action="peliculas", url=host + "/category/censored/"))
    itemlist.append( Item(channel=item.channel, title="Uncensored" , action="peliculas", url=host + "/category/uncensored/"))
    patron  = '<li><a href="([^"]+)" title="[^"]+"><span>([^"]+)</span><span>([^"]+)</span></a></li>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    for scrapedurl,scrapedtitle,cantidad in matches:
        scrapedtitle = scrapedtitle + " (" + cantidad + ")"
        scrapedplot = ""
        scrapedthumbnail = ""
        itemlist.append( Item(channel=item.channel, action="peliculas", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )
    return itemlist


def peliculas(item):
    logger.info()
    itemlist = []
    data = httptools.downloadpage(item.url).data
    patron = '<div class="featured-wrap clearfix">.*?<a href="([^"]+)" title="([^"]+)".*?src="([^"]+)".*?>#([^"]+) Full HD JAV</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    for scrapedurl,scrapedtitle,scrapedthumbnail,calidad in matches:
        scrapedplot = ""
        scrapedtitle = "[COLOR red]" + calidad + "[/COLOR] " + scrapedtitle
        itemlist.append( Item(channel=item.channel, action="findvideos", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )
    next_page_url = scrapertools.find_single_match(data,'<li><a rel=\'nofollow\' href=\'([^\']+)\' class=\'inactive\'>Next')
    if next_page_url!="":
        next_page_url = urlparse.urljoin(item.url,next_page_url)
        itemlist.append( Item(channel=item.channel , action="peliculas" , title="Página Siguiente >>" , text_color="blue", url=next_page_url , folder=True) )

    return itemlist

