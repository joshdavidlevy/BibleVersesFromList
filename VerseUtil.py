import json
import fileinput
from datetime import date

#Load Books.json
with open('Books.json') as f:
  bookData = json.load(f)
books = {}
for book in bookData:
    books[book] = book
    for abbrev in bookData[book]:
        books[abbrev] = book

#Load Bible.json

bibleData = {}

with open('Bible.json') as json_file:
    data = json.load(json_file)    
    for bookData in data["XMLBIBLE"]["BIBLEBOOK"]:

        book = bookData['_bname']
        bibleData[book] = {}

        if "_cnumber" in bookData["CHAPTER"]:

            chapter = 1
            bibleData[book][chapter] = {}

            for verseData in bookData["CHAPTER"]["VERSE"]:

                if "__text" in verseData:

                    verseNum = verseData["_vnumber"]
                    verseText = " ".join(verseData["__text"].split())

                    bibleData[book][chapter][verseNum] = verseText
                else:
                    pass
        else:

            for chapterData in bookData["CHAPTER"]:
              
                chapter = chapterData['_cnumber']
                bibleData[book][chapter] = {}

                for verseData in chapterData["VERSE"]:

                    if "__text" in verseData:

                        verseNum = verseData["_vnumber"]
                        verseText = " ".join(verseData["__text"].split())

                        bibleData[book][chapter][verseNum] = verseText
                    else:
                        pass


    
verses = []
# Load verses.txt containing list of verses
filepath = 'verses.txt'
with open(filepath) as fp:
    line = fp.readline()
    cnt = 1
    while line:
        if (line.strip()):

            customLine = line.split("|")
            if len(customLine) > 1:
                verses.append({"citation":customLine[0].strip(), "text":customLine[1].strip()})
            else:
            
                splitLine = line.split()
                citation = splitLine.pop()

                book = ' '.join(splitLine).strip()

                try:
                    book = books[book]
                except:
                    print("ERROR: Book not found: " + book)
                
                chapter = citation.split(":")[0]

                startVerse = citation.split(":")[1].replace(",","-").split("-")[0]
                endVerse = None
                try:
                    endVerse = citation.split(":")[1].split("-")[1]
                except:
                    endVerse = startVerse

                for verse in range(int(startVerse), int(endVerse)+1):
                    text = ""
                    try:
                        text = bibleData[book][chapter][str(verse)]
                    except:
                        try:
                            # Single chapter books
                            text = bibleData[book][1][str(verse)]
                        except:
                            print("ERROR: Unable to find " + book + " " + chapter + ":" + str(verse))
                        
                    
                    verses.append({"citation": book + " " + chapter + ":" + str(verse), "text":text})     

        line = fp.readline()
        cnt += 1


# Output files for each verse
num = 1

for verse in verses:
    id = str(num)
    if (num < 10):
        id = "0" + str(num)
    with open("Verse " + id + ".txt", 'w') as file:
        file.write(verse["citation"]+"\n")
        file.write(verse["text"])

    #Optionally, replace the verse source names with their citations in the OBS profile
    try:
        with fileinput.FileInput("OA_-_Facebook_Live.json", inplace=True) as file:
            for line in file:
                print(line.replace('"Verse ' + str(num) + '"', '"' + verse["citation"] + '"'), end='')
    except:
        pass
    
    num += 1


d = date.today()
dateStamp = d.strftime('%Y-%m-%d')

#Optionally, if we replaced the verse headings above, update the date stamp so as not to overwrite the template
try:    
    with fileinput.FileInput("OA_-_Facebook_Live.json", inplace=True) as file:
        for line in file:
            print(line.replace('OA - Facebook Live', 'OA - Facebook Live - ' + dateStamp))
except:
    pass
