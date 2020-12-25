# -*- coding: utf-8 -*-

from core import support
host = 'https://1337x.to'
#logger.info('--------------------------------------------' + host)
headers = [['Referer', host]]

@support.menu
def mainlist(item):

    menu = [
        ('4K {film}', ['/sort-category-search/ita%204K/Movies/time/desc/1/', 'peliculas', [0, 'movie', True], 'undefined']),
        ('UHD {film}', ['/sort-category-search/ita%201080/Movies/time/desc/1/', 'peliculas', [0, 'movie', True], 'undefined']),
        ('Cerca Film... {submenu} {film}', ['/category-search/', 'search', ['search', 'movie', True], 'movie']),
        ('Serie TV', ['/sort-category-search/ita/TV/time/desc/1/', 'peliculas', [0 , 'tvshow', True], 'tvshow']),
        ('Cerca Serie TV.. {submenu}', ['/sort-category-search/', 'search', ['search', 'tvshow',True], 'tvshow'])
    ]

    return locals()

	

def search(item, text):
    support.info(item, text)
    if 'tvshow' in item.args:
        item.url += text + " ita/TV/time/desc/1/"
    else:
        item.url += text + " ita/Movies/1/"
    

    try:
        return peliculas(item)
    # Cattura la eccezione così non interrompe la ricerca globle se il canale si rompe!
    except:
        import sys
        for line in sys.exc_info():
            support.logger.error("search except: %s" % line)
        return []
				
@support.scrape
def peliculas(item):

    sceneTitle = item.args[2]
    patron =r'(?P<url>/torrent/.*?)".*?>(?P<title>.*?)<.*?seeds.*?>(?P<seed>.*?)<.*?leeches.*?>.*?<.*?size.*?>(?P<size>.*?)<'
    patronNext= r"""pagination.*?active.*?href.*?href=[?:"|'](.*?)[?:"|']>\d<"""
#    item.url = host + item.url
    return locals()

def findvideos(item):
    if item.contentType == 'tvshow': item.contentType = 'episode'
    Videolibrary = False
    return support.server(item, support.match(item.url, patron=r'(magnet[^"]+)"').match, Videolibrary=Videolibrary,AutoPlay=False)
