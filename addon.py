from BeautifulSoup import BeautifulSoup
import os.path
import sys
import urlparse
import json
import xbmcplugin
from resources.lib import helpers as h

def main_branch():
    h.add_dir(addon_handle, base_url, 'Zee Marathi', "http://www.ozee.com/shows/all/zeemarathi", 'Channel')
    h.add_dir(addon_handle, base_url, 'Zee TV', "http://www.ozee.com/shows/all/zeetv", 'Channel')
    h.add_dir(addon_handle, base_url, '& TV', "http://www.ozee.com/shows/all/andtv", 'Channel')
    h.add_dir(addon_handle, base_url, 'Zindagi', "http://www.ozee.com/shows/all/zindagi", 'Channel')
    h.add_dir(addon_handle, base_url, 'Movies', "http://www.ozee.com/movies/all", 'Movies')

def shows_serials():
    url = h.extract_var(args, 'url')

    soup = BeautifulSoup(h.make_request(url, cookie_file, cookie_jar))
    
    list = soup.findAll("div", {"class":"thumbnail-with-border-small-title clearfix"})

    for div in list:
        xbmc.log(div.find('a')["href"])
        title = div.find('div').find('span')["title"]
        img_src = div.find('img')["src"]
        h.add_dir(addon_handle, base_url, title, div.find('a')["href"] + "/video", 'episode', img_src, img_src)

    pager = soup.find('ul', {'class': lambda x: x and 'pagination' in x.split()})
    if pager is not None:
        strPage = url.split("?page=")
        if len(strPage) == 2:
            nextPage = int(strPage[1]) + 1
        else:
            nextPage = 2
        for pg in pager:
            if (hasattr(pg, "text")) and (pg.text == str(nextPage)):
                nextUrl = strPage[0] + "?page=" + str(nextPage)
                h.add_dir(addon_handle, base_url, 'Next >>', nextUrl, 'Movies')
                break
        h.add_dir(addon_handle, base_url, '<< Home >>', "", '')


def shows_movies():
    url = h.extract_var(args, 'url')
    xbmc.log("Movies URL : " + url)
    soup = BeautifulSoup(h.make_request(url, cookie_file, cookie_jar))
    
    list = soup.findAll("div", {"class":"thumbnail-with-border-small-title clearfix"})

    for div in list:
        title = div.find('div').find('span')["title"]
        img_src = div.find('img')["src"]
        h.add_dir(addon_handle, base_url, title, div.find('a')["href"], 'play', img_src, img_src)

    pager = soup.find('ul', {'class': lambda x: x and 'pagination' in x.split()})
    
    if pager is not None:
        strPage = url.split("?page=")
        if len(strPage) == 2:
            nextPage = int(strPage[1]) + 1
        else:
            nextPage = 2
        for pg in pager:
            if (hasattr(pg, "text")) and (pg.text == str(nextPage)):
                nextUrl = strPage[0] + "?page=" + str(nextPage)
                h.add_dir(addon_handle, base_url, 'Next >>', nextUrl, 'Movies')
                break
        h.add_dir(addon_handle, base_url, '<< Home >>', "", '')


def episode():
    url = h.extract_var(args, 'url')

    soup = BeautifulSoup(h.make_request(url, cookie_file, cookie_jar))

    list = soup.findAll("div", {"class":"col-md-3 col-xs-6 reduce-padding"})

    for div in list:
        episode_url = div.find('a')["href"]
        img_src = div.find('img')["src"]
        h.add_dir(addon_handle, base_url, div.find('img')['title'], episode_url, 'show', img_src, img_src)
'''
    pager = soup.find('ul', {'class': lambda x: x and 'pagination' in x.split()})
    
    if pager is not None:
        strPage = url.split("?page=")
        if len(strPage) == 2:
            nextPage = int(strPage[1]) + 1
        else:
            nextPage = 2
        for pg in pager:
            if (hasattr(pg, "text")) and (pg.text == str(nextPage)):
                nextUrl = strPage[0] + "?page=" + str(nextPage)
                h.add_dir(addon_handle, base_url, 'Next >>', nextUrl, 'Movies')
                break
        h.add_dir(addon_handle, base_url, '<< Home >>', "", '')
'''
def play_movie():
    url = h.extract_var(args, 'url')

    xbmc.log("URL : " + url)
    name = h.extract_var(args, 'name')
	
    soup = BeautifulSoup(h.make_request(url, cookie_file, cookie_jar))
    
    div = soup.find("div", {"id":"movie-container"})

    script = None
    scripts = div.findAll("script")

    for s in scripts:
        if s.text.find('playbackurl = ') != -1:
            script = s
            break
		
    master_m3u8 = script.text.split('playbackurl = ')[1].split('\";')[0][1:]

    data = json.loads(soup.find('script', {'type': 'application/ld+json'}).text)
    thumbnail = data["image"]
    plot = data["description"]
    h.add_dir_video(addon_handle, name, master_m3u8, thumbnail, plot)

def show():
    url = h.extract_var(args, 'url')

    xbmc.log("URL : " + url)
    name = h.extract_var(args, 'name')
	
    soup = BeautifulSoup(h.make_request(url, cookie_file, cookie_jar))
    
    div = soup.find("div", {"id":"episode-detail-page"})

    script = None
    scripts = div.findAll("script")

    for s in scripts:
        if s.text.find('playbackurl = ') != -1:
            script = s
            break
		
    master_m3u8 = script.text.split('playbackurl = ')[1].split('\";')[0][1:]

    data = json.loads(soup.find('script', {'type': 'application/ld+json'}).text)
	
    thumbnail = data["video"]["thumbnailUrl"]
    plot = data["video"]["description"]
    h.add_dir_video(addon_handle, name, master_m3u8, thumbnail, plot)


def not_implemented():
    pass

addon_id = os.path.basename(os.path.dirname(os.path.abspath(__file__)))
cookie_file, cookie_jar = h.init_cookie_jar(addon_id)

base_url = sys.argv[0]

addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])
mode = args.get('mode', ['', ])[0]

if mode == 'Channel':
    shows_serials()
elif mode == 'Movies':
    shows_movies()
elif mode == 'show':
    show()
elif mode == 'play':
    play_movie()
elif mode == 'episode':
    episode()
elif mode == 'not_implemented':
    current_shows()
else:
    main_branch()

xbmcplugin.endOfDirectory(addon_handle)
