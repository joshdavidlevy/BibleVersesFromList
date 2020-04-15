import json

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
            print("Line {}: {}".format(cnt, line.strip()))

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
            print(book, chapter, startVerse, endVerse)

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

    num += 1
