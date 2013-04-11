import pickle

def convert(pickled_file):
	loadFile=open(pickled_file,"rb")
	data=pickle.load(loadFile)
	loadFile.close()
	#Begin Save process as TXT file
	saveFile=open(pickled_file[:-2]+".txt","w")
	saveFile.write(str(data))
	saveFile.close()

convert("webPageDataDictFile.p")
convert("InverseIndex.p")