import re
import requests
import os
from fpdf import FPDF
from PIL import Image

def check_for_num(tested_string):
    m = re.search(r'\d+$', tested_string)
# if the string ends in digits m will be a Match object, or None otherwise.
    if m is not None:
        print (m.group())
    else:
      print (tested_string)
      return tested_string + 1

global urlList
urlList = []

# recursively download images starting from the root URL
'''def downloadImages(url, level): # the root URL is level 0
    print url
    global urlList
    if url in urlList: # prevent using the same URL again
        return
    urlList.append(url)
    try:
        urlContent = urllib2.urlopen(url).read()
    except:
        return

    soup = BeautifulSoup(''.join(urlContent))
    # find and download all images
    imgTags = soup.findAll('img')
    for imgTag in imgTags:
        imgUrl = imgTag['src']
        try:
            imgData = urllib2.urlopen(imgUrl).read()
            fileName = basename(urlsplit(imgUrl)[2])
            output = open(fileName,'wb')
            output.write(imgData)
            output.close()
        except:
            pass

    # if there are links on the webpage then recursively repeat
    if level > 0:
        linkTags = soup.findAll('a')
        if len(linkTags) > 0:
            for linkTag in linkTags:
                try:
                    linkUrl = linkTag['href']
                    downloadImages(linkUrl, level - 1)
                except:
                    pass
'''

def makePdf(pdfFileName, listPages, dir = ''):
    if (dir):
        dir += "\\"

    cover = Image.open(dir + str(listPages[0]) + ".png")
    width, height = cover.size

    pdf = FPDF(unit = "pt", format = [width, height])

    for page in listPages:
        pdf.add_page()
        pdf.image(dir + str(page) + ".png", 0, 0)

    pdf.output(dir + pdfFileName + ".pdf", "F")

def test_url(url):
    request = requests.get(url)
    if request.status_code == 200:
        url_exists = 1
    else:
        url_exists = 0
    return url_exists


def folder_name():
    filepath = input('Please enter your file path: ')
    try:
        with open(os.path.join(filepath, "files.txt"), "w") as a:
            for path, subdirs, files in os.walk(filepath):
                for filename in files:
                    f = os.path.join(path, filename)
                    a.write(f + os.linesep)
    except:
        print("Could not generate directory listing file.")

def downloadSmall(url, file_name):
    image_url = url
    real_file_name = file_name
    no_zero = file_name[0:1]
    if no_zero == 0 or no_zero == '0':
        real_file_name = real_file_name [1:]
    # URL of the image to be downloaded is defined as image_url
    r = requests.get(image_url)  # create HTTP response object

    # send a HTTP request to the server and save
    # the HTTP response in a response object called r
    with open(real_file_name, 'wb') as f:
        # Saving received content as a png file in
        # binary format

        # write the contents of the response (r.content)
        # to a new file in binary mode.
        f.write(r.content)

def downlodImg(url, file_name):

    file_url = url

    r = requests.get(file_url, stream=True)

    with open(file_name, "wb") as png:
        for chunk in r.iter_content(chunk_size=1024):

            # writing one chunk at a time to pdf file
            if chunk:
                png.write(chunk)



print("Image downloader! Just type the url and bingo-bango you got the mango!")
og_url = raw_input(r"URL:")
pdf_name = raw_input(r"Name output pdf name:")
start_url = og_url[:-6]
count_pages = 1
try:
    for i in range(1,99):
        if i < 10:
            new_num = '0' + str(i)
        else:
            new_num = str(i)
        ending_url = new_num + '.png'
        new_url = start_url + ending_url
        print (new_url)
        if test_url(new_url) == 1:
            try:
                downloadSmall(new_url, ending_url)
            except:
                print('Small file fail for file: ' + ending_url)
                downlodImg(new_url, ending_url)
            count_pages += 1
        else:
            makePdf(pdf_name, range(1, count_pages), os.getcwd())
            break
    print ("Finished without any errors")


except:
    print("Finished with error")
