#!/usr/local/bin/python

from ast import literal_eval

def test():
	return "test"


def loadData(name):
	loadData=open(name,'r')
	dataObj=literal_eval(loadData.read())
	loadData.close()
	return dataObj
	
inverse_index=loadData("InverseIndex.txt")
page_data=loadData('webPageDataDictFile.txt')


def make_snippet(search_word, text):
	try:
		snippet="..."+text[text.index(search_word)-20:index(search_word)]++"<strong>"+search_word+"</strong>"+text[text.index(search_word)+len(search_word):text.index(search_word)+20]+"..."
	except: 
		snippet=""
	return snippet


# For every word in the query find the most relevant pages
def get_results(query):
	results=[]
	for word in query.split(" "):
		if word in inverse_index:
			print(word,"is in the index")
			for siteID in inverse_index[word].keys():
# 				print(siteID)
				title=page_data[siteID]['Title']
				url=page_data[siteID]['URL']
				snippet=make_snippet(word,str(page_data[siteID]['Text']))
				hits=inverse_index[word][siteID]
				siteInfoDict={"title":title,"url":url,"snippet":snippet,"hits":hits}
				if len(results)==0:
					results.append(siteInfoDict)
				else:
					for i in range(len(results)):
						if hits>results[i]['hits']:
							results.insert(i,siteInfoDict)
		else:
			return None
	return results
	
def main():
	query=input("search: ")
	print(get_results(query)[0]['hits'])

	
	
if __name__=="__main__": main()
