from BeautifulSoup import BeautifulSoup
import os.path 
import sys
import urlparse
import json
import xbmcplugin
from resources.lib import helpers as h

currentDisplayCounter = 0

# Version 2.0.0

CHANNEL_BASE_URL = "http://api.android.zeeone.com/mobile/get/shows/channel/"
CHANNEL_EPISODE_URL = "http://api.android.zeeone.com/mobile/get/show_videos/"
CHANNEL_SHOW_URL = "http://api.android.zeeone.com/mobile/get/show_video/"

MOVIE_URL = "http://api.android.zeeone.com/mobile/get/movies/"
MOVIE_SHOW_URL = "http://api.android.zeeone.com/mobile/get/movie/"

MUSIC_URL = "http://api.android.zeeone.com/mobile/get/music/"
MUSIC_SHOW_URL = "http://api.android.zeeone.com/mobile/get/music-detail/"

BASE_URL = ""

Channels = [
    {'Name' : 'Zee TV', 'URL' : CHANNEL_BASE_URL + '/zeetv/0/all', 'icon_src':'http://akamai.vidz.zeecdn.com/ozee/asset/zeetv.jpg', 'Type':'Channel~shows'},
    {'Name' : '&TV', 'URL' : CHANNEL_BASE_URL + '/andtv/0/all', 'icon_src':'http://akamai.vidz.zeecdn.com/ozee/asset/andtv.jpg', 'Type':'Channel~shows'},
    {'Name' : 'Zindagi', 'URL' : CHANNEL_BASE_URL + '/zindagi/0/all', 'icon_src':'http://akamai.vidz.zeecdn.com/ozee/asset/zindagi.jpg', 'Type':'Channel~shows'},
    {'Name' : 'Movies', 'URL' : BASE_URL + '/movies/all', 'icon_src':'', 'Type':'Channel~movies'},
    {'Name' : 'Music', 'URL' : BASE_URL + '/music/all', 'icon_src':'', 'Type':'Channel~music'},
    {'Name' : 'Zee Marathi', 'URL' : CHANNEL_BASE_URL + '/zeemarathi/0/all', 'icon_src':'http://akamai.vidz.zeecdn.com/ozee/asset/marathi.jpg', 'Type':'Channel~shows'}, 
    {'Name' : 'Zee Bangla', 'URL' : CHANNEL_BASE_URL + '/zeebangla/0/all', 'icon_src':'http://akamai.vidz.zeecdn.com/ozee/asset/bangla.jpg', 'Type':'Channel~shows'},
    {'Name' : 'Zee Telugu', 'URL' : CHANNEL_BASE_URL + '/zeetelugu/0/all', 'icon_src':'http://akamai.vidz.zeecdn.com/ozee/asset/telugu.jpg', 'Type':'Channel~shows'},
    {'Name' : 'Zee Tamil', 'URL' : CHANNEL_BASE_URL + '/zeetamil/0/all', 'icon_src':'http://akamai.vidz.zeecdn.com/ozee/asset/tamil.jpg', 'Type':'Channel~shows'},
    {'Name' : 'Zee Kannada', 'URL' : CHANNEL_BASE_URL + '/zeekannada/0/all', 'icon_src':'http://akamai.vidz.zeecdn.com/ozee/asset/kannada.jpg', 'Type':'Channel~shows'},
    ]

MoviesLanguages = [
    {'Language' : 'Hindi', 'URL' : MOVIE_URL + '/0/50/hindi/all/'},
    {'Language' : 'Marathi', 'URL' : MOVIE_URL + '/0/50/marathi/all/'},
    {'Language' : 'Telugu', 'URL' : MOVIE_URL + '/0/50/telugu/all/'},
    {'Language' : 'Tamil', 'URL' : MOVIE_URL + '/0/50/tamil/all/'},
    {'Language' : 'Kannada', 'URL' : MOVIE_URL + '/0/50/kannada/all/'},
    {'Language' : 'Bangla', 'URL' : MOVIE_URL + '/0/50/bangla/all/'}
    ]

MusicLanguages = [
    {'Language' : 'Hindi', 'URL' : MUSIC_URL + '/0/50/hindi/null/'},
    {'Language' : 'Marathi', 'URL' : MUSIC_URL + '/0/50/marathi/null/'},
    {'Language' : 'Telugu', 'URL' : MUSIC_URL + '/0/50/telugu/null/'},
    {'Language' : 'Tamil', 'URL' : MUSIC_URL + '/0/50/tamil/null/'},
    {'Language' : 'Kannada', 'URL' : MUSIC_URL + '/0/50/kannada/null/'},
    {'Language' : 'Bangla', 'URL' : MUSIC_URL + '/0/50/bangla/null/'}
    ]

#Channels = json.loads(ChannelJSON)
#MoviesLanguages = json.loads(MoviesJSON)

# Serials
# By Mode : , Main_Branch, Defined Mode : Channel
# By Mode : Channel, show_serial, Defined Mode : episode

def main_branch():
    xbmc.log("Main_Branch")
    for Channel in Channels:
        xbmc.log(Channel['Name'])
        h.add_dir(addon_handle, base_url, Channel["Name"], Channel["URL"], Channel["Type"], Channel["icon_src"], Channel["icon_src"])

def shows_serials():
    xbmc.log("Show_Serials")
    url = h.extract_var(args, 'url')
    xbmc.log("URL : " + url) 
    if param1 == "shows":
        JSONObjs = json.loads(h.make_request(url, cookie_file, cookie_jar))
        for JSONObj in JSONObjs:
            title = JSONObj["title"]
            img_src = JSONObj["listing_image_small"]
            h.add_dir(addon_handle, base_url, title, JSONObj["slug"], "episodemenu", img_src, img_src)
    elif param1 == "music":
        for Music in MusicLanguages:
            xbmc.log(Music["URL"])
            h.add_dir(addon_handle, base_url, Music["Language"], Music["URL"], "Music~0")
    else:
        for Movie in MoviesLanguages:
            xbmc.log(Movie["URL"])
            h.add_dir(addon_handle, base_url, Movie["Language"], Movie["URL"], "Movies~0")
    
def shows_movies():
    xbmc.log("Shows_Movies")
    url = h.extract_var(args, 'url')
    xbmc.log("URL : " + url) 
    if mode == "Movies":
        JSONObjs = json.loads(h.make_request(url, cookie_file, cookie_jar))
    else:
        JSONObjs = json.loads(h.make_request(url, cookie_file, cookie_jar))

    for JSONObj in JSONObjs:
        title = JSONObj["title"]
        if mode == "Movies":
            img_src = JSONObj["image_medium"]
            h.add_dir(addon_handle, base_url, title, JSONObj["slug"], "Show_Movies", img_src, img_src)
        else:
            img_src = JSONObj["listing_image_medium"]
            h.add_dir(addon_handle, base_url, title, JSONObj["slug"], "Show_Music", img_src, img_src)

    currentDisplayCounter = int(param1)
    if len(JSONObjs) >= 50 :
        currentDisplayCounter = currentDisplayCounter + 50
        h.add_dir(addon_handle, base_url, 'Next >>', h.extract_var(args, 'url'), mode + '~' + param1 + '~' + str(currentDisplayCounter), img_src, img_src)
    elif len(JSONObjs) < 50 :
        currentDisplayCounter = -1

def show_music():
    xbmc.log("Function : Show_Music")

    url = h.extract_var(args, 'url')
    
    name = h.extract_var(args, 'name')

    JSONObj = json.loads(h.make_request(MUSIC_SHOW_URL + url, cookie_file, cookie_jar))

    thumbnail = JSONObj["listing_image_small"]
    plot = JSONObj["description"]
    h.add_dir_video(addon_handle, JSONObj["title"], JSONObj["playback_url"], thumbnail, plot)

def show_movies():
    xbmc.log("Function : Show_Movies")

    url = h.extract_var(args, 'url')
    
    name = h.extract_var(args, 'name')

    JSONObj = json.loads(h.make_request(MOVIE_SHOW_URL + url, cookie_file, cookie_jar))

    thumbnail = JSONObj["details"]["listing_image_small"]
    plot = JSONObj["details"]["seo_description"]
    h.add_dir_video(addon_handle, JSONObj["details"]["title"], JSONObj["playback_url"], thumbnail, plot)

def shows_serials_menu():
    xbmc.log("Show_Serials_Menu")
    url = h.extract_var(args, 'url')
    xbmc.log("Serial URL : " + url)
    h.add_dir(addon_handle, base_url, "Newest", url, 'episode~new~' + str(currentDisplayCounter))
    h.add_dir(addon_handle, base_url, "Oldest", url, 'episode~old~' + str(currentDisplayCounter))

def episode():
    xbmc.log("Eposide")
    url = h.extract_var(args, 'url')
    xbmc.log("Eposide URL 1 : " + url)
    
    currentDisplayCounter = int(param2)

    if param1 == "old":
        url = CHANNEL_EPISODE_URL + url + "/" + str(currentDisplayCounter) + "/50/oldest/"
    else:
        url = CHANNEL_EPISODE_URL + url + "/" + str(currentDisplayCounter) + "/50/newest/"

    xbmc.log("Episode URL 2 : " + url)

    JSONObjs = json.loads(h.make_request(url, cookie_file, cookie_jar))

    for JSONObj in JSONObjs:
        title = JSONObj["video_title"]
        img_src = JSONObj["video_image"]

        h.add_dir(addon_handle, base_url, title, JSONObj["slug"], 'show', img_src, img_src)
    if len(JSONObjs) >= 50 :
        currentDisplayCounter = currentDisplayCounter + 50
        h.add_dir(addon_handle, base_url, 'Next >>', h.extract_var(args, 'url'), 'episode~' + param1 + '~' + str(currentDisplayCounter), img_src, img_src)
    elif len(JSONObjs) < 50 :
        currentDisplayCounter = -1


def show():
    xbmc.log("Function : Show")

    url = h.extract_var(args, 'url')
    
    xbmc.log("URL : " + CHANNEL_SHOW_URL + url)
    name = h.extract_var(args, 'name')

    JSONObj = json.loads(h.make_request(CHANNEL_SHOW_URL + url, cookie_file, cookie_jar))

    thumbnail = JSONObj["listing_image_small"]
    plot = JSONObj["description"]
    h.add_dir_video(addon_handle, JSONObj["title"], JSONObj["playback_url"], thumbnail, plot)


def not_implemented():
    pass

addon_id = os.path.basename(os.path.dirname(os.path.abspath(__file__)))
cookie_file, cookie_jar = h.init_cookie_jar(addon_id)

base_url = sys.argv[0]

addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])
params = args.get('mode', ['', ])[0].split("~")


param1 = ""
param2 = ""

mode = params[0]

if len(params) >= 2:
    param1 = params[1]
if len(params) >= 3:
    param2 = params[2]

xbmc.log("Mode : " + mode)

if mode == 'Channel':
    shows_serials()
elif mode == 'episodemenu':
    shows_serials_menu()
elif mode == 'Movies':
    shows_movies()
elif mode == 'Music':
    shows_movies()
elif mode == 'show':
    show()
elif mode == 'play':
    play_movie()
elif mode == 'episode':
    episode()
elif mode == 'Show_Movies':
    show_movies()
elif mode == 'Show_Music':
    show_music()
elif mode == 'MovieLanguage':
    movie_branch()
elif mode == 'not_implemented':
    current_shows()
else:
    main_branch()

xbmcplugin.endOfDirectory(addon_handle)
