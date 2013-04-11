#!/usr/local/bin/python
# use urllib to get the header information for a web page at location url
import urllib.request
import urllib.parse
import urllib.robotparser
from bs4 import BeautifulSoup
from time import sleep
import re
from ast import literal_eval
# import pickle

def RequestResponse(url):
    try:
        response = urllib.request.urlopen(url)
        return response
    except urllib.error.URLError as err:
        print("Error opening url {} .\nError is: {}".format(url, err))


def Relative_URL_Checker(url,originator_url):
    if url[0] == '/':
        parsed_url = urlparse(url)
        origParsed = urlparse(originator_url)
        hostname = "http://" + origParsed.netloc
        new_full_url = urllib.parse.urljoin(hostname, parsed_url.path)
        return new_full_url
    else: 
    	return url
    	
def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', str(element)):
        return False
    return True

link_queue=["http://ischool.berkeley.edu/"] #initiate the list to store a queue of links for the crawl
all_links=["http://ischool.berkeley.edu/"] #keeps track of all links, so not crawled more than once
webPageDataDict={}

#extract all the links (a tags) from a web page; print first 10
def GetLinksFromPage(url,ID):
	response = RequestResponse(url)
	if not response: return
	soup = BeautifulSoup(response.readall())
	title=soup.head.title.get_text() #save title
	texts=soup.body.findAll(text=True)#save visible webpage text
	pageText="".join(x for x in filter(visible,texts)).replace("\n"," ") # remove newline characters
	webPageDataDict[ID]={"ID":ID,"Title":title,"URL":url,"Text":pageText.encode("ascii","ignore")} #store page data in dictionary value
	a_tags = soup.find_all('a')
	for a in a_tags:
		try:
			link = a['href'] #get the url from the link
			link=Relative_URL_Checker(link,url) #ensure links are not relative
			if link not in all_links:  #make sure it's not already crawled
				all_links.append(link) #keep track of links so not crawled twice
				if "ischool.berkeley.edu" in link: #only crawl on ischool page
					link_queue.append(link) #queue that link to be crawled
		except: pass

def SetRobotsChecker(robot_url):
    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(robot_url)
    rp.read()
    return rp # returns True if it is ok to fetch this url, else False

rp=SetRobotsChecker("http://ischool.berkeley.edu/robots.txt") #Setup Robot Checker

def OKToCrawl(rp, url):
    return rp.can_fetch("*", url)


def crawl(count=0):
	print("\n\nNow crawling: "+link_queue[0])
	if OKToCrawl(rp,link_queue[0]) is True:
		GetLinksFromPage(link_queue[0],count)
		del link_queue[0]
		print("total links: "+str(len(all_links)))
		print("queue length: "+str(len(link_queue)))
	sleep(1) #be polite and wait 1 second
	count+=1
	if count<40:
		crawl(count)
	saveData(webPageDataDict,'webPageDataDictFile.txt') #after crawling save the results

inverseIndex={}

def saveData(dataObj,name):
	saveFile=open(name,'w')
	saveFile.write(dataObj)
	saveFile.close()

def loadData(name):
	loadFile=open(name,'r')
	dataObj=literal_eval(loadFile.read())
	loadFile.close()
	return dataObj


def makeInverseIndex():

	for webpage in webPageDataDict:
		regexPattern=re.compile('(/block-inner, /block)|\W') #ensure only words are kept
		pageText=str(webPageDataDict[webpage]["Text"]).lower()
		pageText=re.sub(regexPattern," ",pageText)
		for word in pageText.split():
			if word not in inverseIndex.keys():
				inverseIndex[word]={webPageDataDict[webpage]["ID"]:1} #add word to index for that webpage ID with count of 1
			else: #if the word is already in the index
				if webPageDataDict[webpage]["ID"] not in inverseIndex[word].keys(): #word in index but not the page
					inverseIndex[word][webPageDataDict[webpage]["ID"]]=1
				else: #word in index and on page already so add 1 to the count
					inverseIndex[word][webPageDataDict[webpage]["ID"]]+=1
	print(inverseIndex["special"])
		

def main():
	### Question #1
	crawl() #remove comment to have script crawl the ischool.berkeley.edu site 
	
	### Question #2
	global webPageDataDict   
	webPageDataDict=loadData('webPageDataDictFile.txt')
	makeInverseIndex()
	saveData(inverseIndex,"InverseIndex.txt") #save the Inverted Index for use later


if __name__=="__main__": main()
