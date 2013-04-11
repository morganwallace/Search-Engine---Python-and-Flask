#!/usr/local/bin/python
# use urllib to get the header information for a web page at location url
import urllib2, urllib
import urllib2, urllib, urlparse
import robotparser
from bs4 import BeautifulSoup
from time import sleep
import re
import pickle
from itertools import ifilter
from io import open

def RequestResponse(url):
    try:
        response = urllib2.urlopen(url)
        return response
    except urllib2.URLError, err:
        print u"Error opening url {} .\nError is: {}".format(url, err)


def Relative_URL_Checker(url,originator_url):
    if url[0] == u'/':
        parsed_url = urlparse(url)
        origParsed = urlparse(originator_url)
        hostname = u"http://" + origParsed.netloc
        new_full_url = urlparse.urljoin(hostname, parsed_url.path)
        return new_full_url
    else: 
    	return url
    	
def visible(element):
    if element.parent.name in [u'style', u'script', u'[document]', u'head', u'title']:
        return False
    elif re.match(u'<!--.*-->', unicode(element)):
        return False
    return True

link_queue=[u"http://ischool.berkeley.edu/"] #initiate the list to store a queue of links for the crawl
all_links=[u"http://ischool.berkeley.edu/"] #keeps track of all links, so not crawled more than once
webPageDataDict={}

#extract all the links (a tags) from a web page; print first 10
def GetLinksFromPage(url,ID):
	response = RequestResponse(url)
	if not response: return
	soup = BeautifulSoup(response.readall())
	title=soup.head.title.get_text() #save title
	texts=soup.body.findAll(text=True)#save visible webpage text
	pageText=u"".join(x for x in ifilter(visible,texts)).replace(u"\n",u" ") # remove newline characters
	webPageDataDict[ID]={u"ID":ID,u"Title":title,u"URL":url,u"Text":pageText.encode(u"ascii",u"ignore")} #store page data in dictionary value
	a_tags = soup.find_all(u'a')
	for a in a_tags:
		try:
			link = a[u'href'] #get the url from the link
			link=Relative_URL_Checker(link,url) #ensure links are not relative
			if link not in all_links:  #make sure it's not already crawled
				all_links.append(link) #keep track of links so not crawled twice
				if u"ischool.berkeley.edu" in link: #only crawl on ischool page
					link_queue.append(link) #queue that link to be crawled
		except: pass

def SetRobotsChecker(robot_url):
    rp = robotparser.RobotFileParser()
    rp.set_url(robot_url)
    rp.read()
    return rp # returns True if it is ok to fetch this url, else False

rp=SetRobotsChecker(u"http://ischool.berkeley.edu/robots.txt") #Setup Robot Checker

def OKToCrawl(rp, url):
    return rp.can_fetch(u"*", url)


def crawl(count=0):
	print u"\n\nNow crawling: "+link_queue[0]
	if OKToCrawl(rp,link_queue[0]) is True:
		GetLinksFromPage(link_queue[0],count)
		del link_queue[0]
		print u"total links: "+unicode(len(all_links))
		print u"queue length: "+unicode(len(link_queue))
	sleep(1) #be polite and wait 1 second
	count+=1
	if count<40:
		crawl(count)
	saveData(webPageDataDict,u'webPageDataDictFile.p') #after crawling save the results

inverseIndex={}

def saveData(dataObj,name):
	saveFile=open(name,u'wb')
	pickle.dump(dataObj,saveFile)
	saveFile.close()

def loadData(name):
	webPageDataDictFile=open(name,u'rb')
	dataObj=pickle.load(webPageDataDictFile)
	webPageDataDictFile.close()
	return dataObj


def makeInverseIndex():

	for webpage in webPageDataDict:
		regexPattern=re.compile(u'(/block-inner, /block)|\W') #ensure only words are kept
		pageText=unicode(webPageDataDict[webpage][u"Text"]).lower()
		pageText=re.sub(regexPattern,u" ",pageText)
		for word in pageText.split():
			if word not in inverseIndex.keys():
				inverseIndex[word]={webPageDataDict[webpage][u"ID"]:1} #add word to index for that webpage ID with count of 1
			else: #if the word is already in the index
				if webPageDataDict[webpage][u"ID"] not in inverseIndex[word].keys(): #word in index but not the page
					inverseIndex[word][webPageDataDict[webpage][u"ID"]]=1
				else: #word in index and on page already so add 1 to the count
					inverseIndex[word][webPageDataDict[webpage][u"ID"]]+=1
	print inverseIndex[u"special"]
		

def main():
	### Question #1
	crawl() #remove comment to have script crawl the ischool.berkeley.edu site 
	
	### Question #2
	global webPageDataDict   
	webPageDataDict=loadData(u'webPageDataDictFile.p')
	makeInverseIndex()
	saveData(inverseIndex,u"InverseIndex.p") #save the Inverted Index for use later


if __name__==u"__main__": main()
