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

def listSubjects():
	subjectList = []
	x = requests.get("https://open.umn.edu/opentextbooks/subjects.json")
	y = json.loads(x.text)

	for item in y["data"]:
		print(item["name"])

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

	while count < total:
		urls.append("https://open.umn.edu/opentextbooks/textbooks.json?page="+str(count))
		count = count+1

	async with aiohttp.ClientSession() as session:
		for u in urls:
			print(u)
			html = fetchUrl(session, u)
			bookList = bookList + getTitle(json.loads(await html))
	if (len(sys.argv) > 1):
		bookList = list(filter(lambda book: (sys.argv[1]) in book["subjects"], bookList))
	bookList.sort(key=lambda book: len(book["subjects"]), reverse=True)
	bookList.sort(key=lambda book: book["subjects"])
	for b in bookList:
		print(str(b["subjects"]) +" | "+ b["title"])


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
			listSubjects()
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
