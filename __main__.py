import asyncio
import aiohttp
import requests
import json
import sys

# def getPage(pageNum):
# 	url = "https://open.umn.edu/opentextbooks/textbooks.json?page="+str(pageNum)
# 	return requests.get(url)

async def fetchUrl(session, url):
	async with session.get(url) as response:
		return await response.text()

async def fetchAllData(pages):
	dataVal = []
	count = 1
	async with aiohttp.ClientSession() as session:
		while count < pages:
			print(str(int((count/pages)*100))+"%", end="\r")
			html = fetchUrl(session, "https://open.umn.edu/opentextbooks/textbooks.json?page="+str(count))
			resp = json.loads(await html)
			dataVal = dataVal + resp["data"]
			count = count + 1
	return dataVal

async def listSubjects():
	subjectList = []
	x = requests.get("https://open.umn.edu/opentextbooks/textbooks.json")
	y = json.loads(x.text)

	total = int(y["links"]["total_pages"])

	data = await fetchAllData(total)
	func = lambda book: book["subjects"]

	for item in data:
		for subj in func(item):
			if subj["name"] not in subjectList:
				subjectList.append(subj["name"])
	subjectList.sort()
	for item in subjectList:
		print(item)

def printBook(book):
	text = f""
	text += book["title"]+"\n"
	text += str([subject["name"] for subject in book["subjects"]]) +"\n"
	text += str([forma["format"]+":"+forma["url"] for forma in book["formats"]]) +"\n"
	text += book["url"]+"\n"
	print(text)

async def printList(subject=None):
	print("started")
	bookList = []

	x = requests.get("https://open.umn.edu/opentextbooks/textbooks.json")
	y = json.loads(x.text)

	count = 1
	total = int(y["links"]["total_pages"])

	urls = []
	payloads = []
	data = []

	bookList = await fetchAllData(total)
	print(len(sys.argv))
	for book in bookList:
		subjects = list(set(map(lambda subj: subj["name"].lower(), book["subjects"])))
		if subject != None:
			if sys.argv[1].lower() not in subjects:
				bookList.remove(book)

	for i in bookList:
		printBook(i)


def getTitle(resp):
	retVal = []
	for i in resp["data"]:
		newVal = {"title": "", "subjects": []}
		newVal["title"] = i["title"]
		for s in i["subjects"]:
			newVal["subjects"].append(s["name"])
		newVal["subjects"].sort()
		retVal.append(newVal)
	return retVal

async def main(argv):
	if len(argv) == 0:
		await printList();
	else:
		if argv[0].lower() == "list":
			await listSubjects()
		else:
			await printList(argv[0])

if __name__ == '__main__':
	loop = asyncio.get_event_loop()
	loop.run_until_complete(main(sys.argv[1:]))


	# 	count = count + 1
	# asyncio.gather(getPage([for item in urls]))
	# payloads.append(await asyncio.create_task(getPage(count)))

	# for key, item in payloads:
	# 	print(await item["title"])



	# print(len(payloads))
	# for key, item in payloads:
	# 	await item
	# 	print(key, item)
	# 	z = json.loads(item.text)
	# 	for item in z["data"]:
	# 		bookList.append(item["title"])
	# 		print(item["title"])
