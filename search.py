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
	# if text.index(search_word)>=20 and len(text)-text.index(search_word)>20:
	try: 
		pre="..."+text[text.index(search_word)-30:text.index(search_word)]
		post=text[text.index(search_word)+len(search_word):text.index(search_word)+30]+"..."
		snippet=pre+search_word+post
	except:
		try:
			search_word=search_word.title()
			pre="..."+text[text.index(search_word)-20:text.index(search_word)]
			theWord=search_word
			post=text[text.index(search_word)+len(search_word):text.index(search_word)+20]+"..."
			snippet=pre+theWord+post
		except: return ""
	# elif len(text)-text.index(search_word)>20
# 		return ""
	return snippet


# For every word in the query find the most relevant pages
def get_results(query):
	results=[]
	
	for word in query.split(" "):
		if word in inverse_index:
# 			print(word,"is in the index")
			for siteID in inverse_index[word].keys():
# 				print(inverse_index[word])
				title=page_data[siteID]['Title']
				url=page_data[siteID]['URL']
# 				print(page_data[siteID]['URL'])
				snippet=make_snippet(word,str(page_data[siteID]['Text']))
				hits=inverse_index[word][siteID]
				siteInfoDict={"title":title,"url":url,"snippet":snippet,"hits":hits}
				#rank the results
				if len(results)==0:  results.append(siteInfoDict)
				else:
					if hits<results[-1]['hits']:results.append(siteInfoDict) #if hits is lowest then append
					else:
						for site in results:
							if hits>=site['hits']:
								results.insert(results.index(site),siteInfoDict)
								break

		else:
			return None
	return results
	
def main():
	myResults = get_results("data")
# 	for i in myResults:
# # 		print (i['hits'])

	
	
if __name__=="__main__": main()
