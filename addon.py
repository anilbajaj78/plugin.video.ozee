from BeautifulSoup import BeautifulSoup
import os.path
import sys
import urlparse
import json
import xbmcplugin
from resources.lib import helpers as h


def main_index():
    #h.add_dir(addon_handle, base_url, 'Current Shows', SHOWS_URL, 'CurrentShows')
    #h.add_dir(addon_handle, base_url, 'Archive Shows', SHOWS_URL, 'ArchiveShows')
    h.add_dir(addon_handle, base_url, 'Zee Marathi', "http://www.ozee.com/shows/all/zeemarathi", 'CurrentShows')
    h.add_dir(addon_handle, base_url, 'Zee TV', "http://www.ozee.com/shows/all/zeetv", 'CurrentShows')
    h.add_dir(addon_handle, base_url, '& TV', "http://www.ozee.com/shows/all/andtv", 'CurrentShows')
    h.add_dir(addon_handle, base_url, 'Zindagi', "http://www.ozee.com/shows/all/zindagi", 'CurrentShows')
    h.add_dir(addon_handle, base_url, 'Movies', "http://www.ozee.com/shows/all/Movies", 'CurrentShows')

def current_shows():
    url = h.extract_var(args, 'url')

    soup = BeautifulSoup(h.make_request(url, cookie_file, cookie_jar))

    # XXX: If want sorted
    # import operator
    # shows = {}
    # shows[a_attrs['href']] = a_attrs['title']
    # shows = sorted(shows.items(), key=operator.itemgetter(1))

    # XXX: View mode thumbnail supported in xbmcswift2

    #h2 = soup.findAll('h2')
    
    list = soup.findAll("div", {"class":"thumbnail-with-border-small-title clearfix"})

    for div in list:
        xbmc.log(div.find('a')["href"])
        title = div.find('div').find('span')["title"]
        img_src = div.find('img')["src"]
        h.add_dir(addon_handle, base_url, title, div.find('a')["href"] + "/video", 'show', img_src, img_src)


def archive_shows():
    url = h.extract_var(args, 'url')

    soup = BeautifulSoup(h.make_request(url, cookie_file, cookie_jar))

    h2 = soup.find_all('h2')

    for h2 in soup.find_all('h2'):
        if h2.text == 'Archive Shows':
            for div in h.bs_find_all_with_class(h2.nextSibling, 'div', 'archive-show'):
                a = div.find('a')
                a_attrs = dict(a.attrs)
                h.add_dir(addon_handle, base_url, a_attrs['title'], '%s/video/' % a_attrs['href'], 'show')
            break


def show():
    url = h.extract_var(args, 'url')

    xbmc.log("URL :" + url)
    #url = '%s%s' % (ZEEMARATHI_REFERRER, url)

    soup = BeautifulSoup(h.make_request(url, cookie_file, cookie_jar))

    list = soup.findAll("div", {"class":"col-md-3 col-xs-6 reduce-padding"})
    #nCnt = 0

    for div in list:
        #if nCnt == 8:
        #    break
        #nCnt = nCnt + 1

        #xbmc.log('HREF : " + div.find('a')["href"])
        episode_url = div.find('a')["href"]
        img_src = div.find('img')["src"]
        h.add_dir(addon_handle, base_url, div.find('img')['title'], episode_url, 'episode', img_src, img_src)

#    ul = soup.find('ul', {'class': lambda x: x and 'show-videos-list' in x.split()})
#    for li in ul:
#        div = li.find('div', {'class': lambda x: x and 'video-watch' in x.split()})
#        episode_url = div.find('a')['href']
#        name = li.find('div', {'class': 'video-episode'}).text
#        img_src = 'DefaultFolder.png'
#        img = li.find('img')
#        if img:
#            img_src = img['src']


    pager = soup.find('ul', {'class': lambda x: x and 'pager' in x.split()})
    if pager:
        next_link = pager.find('li', {'class': lambda x: x and 'pager-next' in x.split()})
        if next_link:
            next_url = next_link.find('a')['href']
            if next_url:
                h.add_dir(addon_handle, base_url, 'Next >>', next_url, 'show')


def episode():
    url = h.extract_var(args, 'url')

    name = h.extract_var(args, 'name')

    #xbmc.log("URL : " + url)
	
    soup = BeautifulSoup(h.make_request(url, cookie_file, cookie_jar))
    
    div = soup.find("div", {"id":"episode-detail-page"})

    script = None
    scripts = div.findAll("script")

    for s in scripts:
        if s.text.find('playbackurl = ') != -1:
            script = s
            break
		
    master_m3u8 = script.text.split('playbackurl = ')[1].split('\";')[0][1:]
    xbmc.log("Master : " + master_m3u8)
    #plot = soup.find('p', {'itemprop': 'description'}).text
    #xbmc.log("JSON : " + soup.find('script', {'type': 'application/ld+json'}).text)
    data = json.loads(soup.find('script', {'type': 'application/ld+json'}).text)
	
    thumbnail = data["video"]["thumbnailUrl"]
    plot = data["video"]["description"]
	#name = data["video"]["name"]
    h.add_dir_video(addon_handle, name, master_m3u8, thumbnail, plot)


def not_implemented():
    pass

ZEEMARATHI_REFERRER = 'http://www.ozee.com'
SHOWS_URL = '%s/shows/' % ZEEMARATHI_REFERRER

addon_id = os.path.basename(os.path.dirname(os.path.abspath(__file__)))
cookie_file, cookie_jar = h.init_cookie_jar(addon_id)

base_url = sys.argv[0]
xbmc.log("Base : " + base_url)
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])
mode = args.get('mode', ['', ])[0]
xbmc.log("Mode : " + mode)
if mode == 'CurrentShows':
    current_shows()
elif mode == 'ArchiveShows':
    archive_shows()
elif mode == 'show':
    show()
elif mode == 'episode':
    episode()
elif mode == 'not_implemented':
    current_shows()
else:
    main_index()

xbmcplugin.endOfDirectory(addon_handle)
