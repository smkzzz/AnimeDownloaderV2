import requests
import json
from bs4 import BeautifulSoup
import time
import os
import pickle
import traceback


class AnimePaheParser():
    def __init__(self, driver):
        self.driver = driver

    def getDetails(self, session):
        api = requests.get(
            f"https://animepahe.com/api?m=release&id={session}&sort=episode_asc&page=1").text
        js = json.loads(api)
        test = requests.get(
            f"https://animepahe.com/anime/{session}")
        ss = BeautifulSoup(test.content, 'html5lib')
        inf = ss.find('div', {'class': 'anime-info'})
        en = ""
        for i in inf.findAll('p'):
            if "English" in i.text:
                en = i.text
        en = en.replace("English: ", "")
        return [js['from'], js['total'], en]

    def getEpisodes(self, session, start, end):

        limit = 30
        page = 1
        while(start / limit > 1):
            page += 1
            limit += 30
        api = requests.get(
            f"https://animepahe.com/api?m=release&id={session}&sort=episode_asc&page={page}")
        data = json.loads(api.text)
        total_page = data['last_page']

        episodes = []
        while(page <= total_page):

            if(len(episodes) > end - start):
                break
            api = requests.get(
                f"https://animepahe.com/api?m=release&id={session}&sort=episode_asc&page={page}")
            episode = json.loads(api.text)
            for e in episode['data']:
                if(len(episodes) > end - start):
                    break
                if(e['episode'] >= start):

                    episodes.append(
                        {'episode': e['episode'], 'session': e['session']})
            page += 1
        return episodes

    def getKwikToken(self):
        self.driver.get("https://kwik.cx/f/mIqErRexBOS8")
        page = self.driver.page_source
        while True:
            try:
                ss = BeautifulSoup(page, 'html5lib')
                token = ss.find('input', {'name': '_token'})['value']
                return token
            except Exception as e:
                print(f"Error getting token {str(e)}")
                self.driver.get("https://kwik.cx/f/mIqErRexBOS8")
                page = self.driver.page_source
                time.sleep(2)

    def getCookie(self):
        driver = self.driver
        while True:
            try:
                kwik = driver.get_cookie('kwik_session')[
                    'value'].replace("%3D", "")

                ppushow = driver.get_cookie(
                    'ppu_show_on_4e5e04716f26fd21bf611637f4fb8a46')['value']
                ppumain = driver.get_cookie(
                    'ppu_main_4e5e04716f26fd21bf611637f4fb8a46')['value']
                ppuexp = driver.get_cookie(
                    'ppu_exp_4e5e04716f26fd21bf611637f4fb8a46')['value']

                cookie = f"srv=s0; ppu_main_4e5e04716f26fd21bf611637f4fb8a46={ppumain}; ppu_exp_4e5e04716f26fd21bf611637f4fb8a46={ppuexp}; ppu_sub_4e5e04716f26fd21bf611637f4fb8a46=2;ppu_show_on_4e5e04716f26fd21bf611637f4fb8a46={ppushow}; kwik_session={kwik}="
                return cookie
            except Exception as e:
                print(traceback.format_exc())
                print(f"\nError getting cookies, retrying...  {str(e)}")
                break

    def getKwikLink(self, link):
        sd = requests.get(link)
        soup = BeautifulSoup(sd.content, 'html5lib')
        link = soup.find('a', {'class': 'redirect'})['href']
        return link

    def getEpisodeLink(self, anime, session, q, au, fs):

        link = None
        content = requests.get(f"https://animepahe.com/play/{anime}/{session}")
        soup = BeautifulSoup(content.content, 'html5lib')

        download_menu = soup.find('div', {'aria-labelledby': 'downloadMenu'})
        qualities = download_menu.findAll('a')
        for e in qualities:
            quality = e.text.replace("&middot; ", "").split(" ")
            fansub = quality[0]
            res = quality[2].replace('p', '')
            size = quality[3]
            link = e['href']
            audio = e.find('span', {'class': 'badge-warning'})
            try:
                audio = audio.text
            except:
                audio = 'jpn'

            if(audio == au and fansub == fs and res == q):

                link = {'quality': res, 'fansub': fansub,
                        'audio': audio, 'disc': ' ', 'kwik_pahewin': link}
                break
        return link

    def getQualities(self, anime, session):
        content = requests.get(f"https://animepahe.com/play/{anime}/{session}")
        soup = BeautifulSoup(content.content, 'html5lib')
        download_menu = soup.find('div', {'aria-labelledby': 'downloadMenu'})
        qualities = download_menu.findAll('a')

        av_qualities = []

        for i, e in enumerate(qualities):
            quality = e.text.replace("&middot; ", "").split(" ")
            fansub = quality[0]
            res = quality[2].replace('p', '')
            size = quality[3]
            audio = e.find('span', {'class': 'badge-warning'})
            try:
                audio = audio.text
            except:
                audio = 'jpn'
            av_qualities.append(
                {'quality': res, 'fansub': fansub, 'audio': audio, 'disc': ' '})
        return av_qualities

    def search(self, anime):
        api = requests.get(
            f"https://animepahe.com/api?m=search&q={anime}").text
        jdata = json.loads(api)
        try:
            data = jdata['data']
            return data
        except:
            return None

    def getDefault(self, session):
        link = None

        q = self.getQualities(session)
        for i in q:
            if(i['quality'] == '720'):
                link = i
                break
            if(link is None and i['quality'] == '360'):
                link = i
            if(link is None and i['quality'] == '1080'):
                link = i
        if(link is None):
            link = q[0]
        return link

    def getLink(self, link, ref, file, token, cookie):
        while True:
            try:
                data = {
                    'file': file,
                    '_token': token,
                }

                headers = {
                    'authority': 'kwik.cx',
                    'referer': ref,
                    'method': 'POST',
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                    'content-type': 'application/x-www-form-urlencoded',
                    'sec-ch-ua': '"Microsoft Edge";v="105", " Not;A Brand";v="99", "Chromium";v="105"',
                    'cookie': cookie,
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.50'
                }

                sd = requests.post(
                    link, data=data, headers=headers, allow_redirects=False)

                we = sd.headers['location'].split('=')
                fn = f"{we[0]}={file}&token={we[2]}={we[3]}"
                return fn
            except Exception as e:
                print(f"Error token error: {e}")
                break
