import os 
import json
import requests
import re
import base64
from bs4 import BeautifulSoup
#http://mangalifewin.takeshobo.co.jp/rensai/yo-jolife/yo-jo-001/20361/
WEBPAGE = "http://mangalifewin.takeshobo.co.jp/rensai/yo-jolife/"
MAINPAGE = "http://mangalifewin.takeshobo.co.jp/rensai/yo-jolife/"
CHAPTER_NAME = "yo-jo-"
#"001/"

SAVE_FOLDER = "images"

user_agent = {
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:70.0) Gecko/20100101 Firefox/70.0"
}


def main():
	if not os.path.exists(SAVE_FOLDER):
		os.mkdir(SAVE_FOLDER)
	find_image_pages()

def find_image_pages():
	global soup

	searchurl = MAINPAGE
	response = requests.get(searchurl,headers=user_agent)
	html = response.text
	soup = BeautifulSoup(html,"html.parser")

	results = soup.findAll("a",{'href': re.compile(r'^http://mangalifewin.takeshobo.co.jp/rensai/yo-jolife/*')})
	print(len(results))
	# print(type(results))


	# Get all next page links from main page
	image_data = [(a["href"],get_chapter(a["title"])) for a in results]
	print(len(image_data))


	# Save in a file
	# view = open("view.txt","w", encoding="utf-8")
	# print("Writing to file...")
	# view.write(str(image_data))
	# view.close()
	# print("done")

	for i in range(len(image_data)):
		get_image_details(image_data[i])
		# results = soup.findAll("a",{'href': re.compile(r'^http://mangalifewin.takeshobo.co.jp/rensai/yo-jolife/*')})


	# Download first chapter, first image


def get_chapter(string):
    m = re.match(r"\[(\d+)-(\d+)\]", string)
    return m.group(1)

def get_image_details(image_data):
	# Get img_data
	# Get name of image
	href = image_data[0]
	chapter_num = image_data[1]

	print("Sending request...")
	content = requests.request("GET",href)
	print("done")
	soup = BeautifulSoup(content.text,"html.parser")

	# img_data
	image_list = soup.findAll("img",{"alt":"comic","width":"640","height":"800"})
	img_data = image_list[0]["src"]

	# img name
	image_tag_list = soup.findAll("h3",{"class":"articleTitle"})
	image_name = image_tag_list[0].text
	print(image_name)
	
	# print(img_data)
	download_image(img_data,image_name,chapter_num)



def download_image(img_data,name,chapter_num):
	# Separate the metadata from the image data
	head, data = img_data.split(',', 1)

	# Get the file extension (gif, jpeg, png)
	file_ext = head.split(';')[0].split('/')[1]

	# Decode the image data
	plain_data = base64.b64decode(data)

	# Check if folder exists, create if it doen't
	if not os.path.exists("{}/{}".format(SAVE_FOLDER,chapter_num)):
		os.mkdir("{}/{}".format(SAVE_FOLDER,chapter_num))

	# Write the image to a file
	with open('{}/{}/{}.'.format(SAVE_FOLDER,chapter_num,name) + file_ext, 'wb') as f:
		f.write(plain_data)


if __name__ == '__main__':
	main()