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
with open('Bible.json') as f:
  bibleData = json.load(f)
for book in bibleData:
    if not book in bookData:
        print("ERROR! No abbreviation found for " + book)
        print("Please update Books.json")
    
verses = []
# Load verses.txt containing list of verses
filepath = 'verses.txt'
with open(filepath) as fp:
    line = fp.readline()
    cnt = 1
    while line:
        if (line.strip()):
            splitLine = line.split()
            citation = splitLine.pop()

            book = ' '.join(splitLine).strip()

            try:
                book = books[book]
            except:
                print("ERROR: Book not found: " + book)
            
            chapter = citation.split(":")[0]
            startVerse = citation.split(":")[1].split("-")[0]
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
        with fileinput.FileInput("OA__Facebook_Live.json", inplace=True) as file:
            for line in file:
                print(line.replace('"Verse ' + str(num) + '"', '"' + verse["citation"] + '"'), end='')
    except:
        pass
    
    num += 1


d = date.today()
dateStamp = d.strftime('%Y-%m-%d')

#Optionally, if we replaced the verse headings above, update the date stamp so as not to overwrite the template
try:    
    with fileinput.FileInput("OA__Facebook_Live.json", inplace=True) as file:
        for line in file:
            print(line.replace('OA - Facebook Live', 'OA - Facebook Live - ' + dateStamp))
except:
    pass
