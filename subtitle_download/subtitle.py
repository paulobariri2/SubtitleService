import requests
from bs4 import BeautifulSoup
import json
import os
import configparser
import zipfile

LOGIN_URL = "http://legendas.tv/login"
SEARCH_URL = "http://legendas.tv/busca/"
TITLE_URL = "http://legendas.tv/legenda/busca/-/1/-/0/"
DOWNLOAD_URL = "http://legendas.tv/downloadarquivo/"

headers = {
	"User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3"
}

proxies = {
	"http":os.environ.get('PROXY_HTTP'),
	"https":os.environ.get('PROXY_HTTPS')
}

payload = {
        'data[User][username]':os.environ.get('USERNAME'),
        'data[User][password]':os.environ.get('PASSWORD'),
        'data[lembrar]':'on',
        '_method':'POST'
}


def checkForSubtitles(searchstring, season, lastdate, spanname, tvshowname=None):
	nametosearch = searchstring
	if tvshowname:
		nametosearch = tvshowname

	with requests.session() as session:
		loginLegendasTV(session)
		seasonid = retrieveSeasonUrl(searchstring, spanname, season, session)
		release2subidmap = searchForNewSubtitles(seasonid, nametosearch, season, lastdate, session)
		subfile = downloadFile(release2subidmap['Law_and_Order_SVU_S21E05_At_Midnight_in_Manhattan_1080p_AMZN_WEB_DL_DDP5_1_H_264_NTb'], session)
		saveFile(subfile, 'Law_and_Order_SVU_S21E05_At_Midnight_in_Manhattan_1080p_AMZN_WEB_DL_DDP5_1_H_264_NTb.zip')


def loginLegendasTV(session):
        resp = session.post(LOGIN_URL, data=payload, headers=headers, proxies=proxies)
        print("Login status: " + str(resp.status_code))
	

def retrieveSeasonUrl(searchstring, spanname, season, session):
	print("Searching for " + spanname + " S" + season + " link.")
	resp = session.get(SEARCH_URL+searchstring, headers=headers, proxies=proxies)
	print("Search status: " + str(resp.status_code))
	soup = BeautifulSoup(resp.content, 'html.parser')
	seasonlink = None
	for a in soup.find_all('a'):
		if (spanname in a.text) and (season in a.text):
			seasonlink = a
			break
	seasonid = None
	if seasonlink:
		seasonid = a['data-filme']
	return seasonid


def searchForNewSubtitles(seasonid, searchstring, season, lastdate, session):
	print("Searching for " + searchstring + " S" + season + " subtitles.")
	resp = session.get(TITLE_URL+seasonid, headers=headers, proxies=proxies)
	print("Search status: " + str(resp.status_code))
	soup = BeautifulSoup(resp.content, 'html.parser')
	sublinks = []
	for a in soup.find_all('a'):
		if (searchstring in a.text) and ( ('S'+season) in a.text):
			sublinks.append(a)

	release2subidmap = {}
	for a in sublinks:
		link = a['href']
		subinfo = link.split("/")
		subid = subinfo[2]
		release = subinfo[4]
		release2subidmap[release] = subid

	return release2subidmap

def downloadFile(subid, session):
        print("Downloading subtitle - id=" + subid)
        resp = session.get(DOWNLOAD_URL+subid, data=payload, headers=headers, proxies=proxies)
        print("Download status: " + str(resp.status_code))
        return resp.content

def saveFile(content, filename):
    print("Saving subtitle as " + filename)
    with open(filename, 'wb') as file:
        file.write(content)
    return os.path.abspath(os.path.abspath(filename))

def searchForTitles(title):
    print("Searching for " + title + " titles.")
    resp = requests.get(SEARCH_URL+title, headers=headers, proxies=proxies)
    print("Search status: " + str(resp.status_code))
    soup = BeautifulSoup(resp.content, 'html.parser')
    titles = []
    for span in soup.find_all('span'):
        parent = span.find_parents("a")
        if len(parent) == 0:
            continue
        a = parent[0]
        data = {}
        data['image'] = a.img['src']
        data['id'] = a['data-filme']
        data['span'] = span.text
        data['text'] = a.p.text
        titles.append(data)
    return titles

def mapHtmlSubtitle2DictSubtitle(elements):
    subtitles = []
    for e in elements:
        sub = {}
        sub['number'] = e.find_all('span')[0].text
        sub['class'] = e.get('class')[0] if e.get('class') else ""

        for p in e.find_all('p'):
            if p.get('class') and p['class'][0] == 'data':
                sub['data'] = p.text
                sub['uploader'] = p.find_all('a')[0].text
            else:
                a = p.find_all('a')[0]
                sub['url'] = a['href']
                sub['name'] = a.text
                sub['id'] = a['href'].split('/')[2]
                
        subtitles.append(sub)
    return subtitles

def retrieveTitleSubtitles(titleId):
    print("Searching for subtitles: " + TITLE_URL + titleId)
    resp = requests.get(TITLE_URL+titleId, headers=headers, proxies=proxies)
    print("Search status: " + str(resp.status_code))
    soup = BeautifulSoup(resp.content, 'html.parser')
    
    gallery = soup.findAll('div', {'class':'gallery clearfix list_element'})
    if (not gallery) or len(gallery) == 0:
        print("REAISE ERROR")
        return None

    subtitles = []
    for child in gallery[0].children:
        dictSubtitle = mapHtmlSubtitle2DictSubtitle(child.children)
        subtitles += dictSubtitle
    
    return subtitles

def retrieveZipFileInfo(zipPath):
    zipSubs = []
    with zipfile.ZipFile(zipPath) as zip:
        for f in zip.namelist():
            if f.endswith('.srt'):
                zipSubs.append(f)
    return zipSubs

def downloadSubtitle(subId, outputName):
    zipFile = outputName + ".zip"
    with requests.session() as session:
        loginLegendasTV(session)
        subfile = downloadFile(subId, session)
        absZipPath = saveFile(subfile, zipFile)
    resp = {}
    resp['fileName'] = zipFile
    resp['fileLocation'] = os.path.abspath(os.getcwd())
    resp['subtitleId'] = subId

    zipSubs = retrieveZipFileInfo(absZipPath)
    resp['subtitles'] = zipSubs
    return resp

if __name__ == "__main__":
    print('Starting')
    checkForSubtitles("SVU", "21", "", "Law & Order: SVU")
    #searchForTitles("Missao impossivel")
