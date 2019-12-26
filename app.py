# -*- coding: utf-8 -*-
from itertools import permutations
from itertools import product
from itertools import islice
from random import shuffle
from docx import Document
import docx2txt
import zipfile
import re
z = zipfile.ZipFile("AC 1 ano III unid - História.docx")

#print list of valid attributes for ZipFile object
#print dir(z)

#print all files in zip archive
all_files = z.namelist()
#print all_files

#get all files in word/media/ directory
images = filter(lambda x: x.startswith('word/media/'), all_files)
j=0
for i in images:
    image1 = z.open(i).read()
    z.extract(i, r'Images')
    j=j+1
#Extract file


#text = docx2txt.process("Cópia de MP2 - 2018.2.docx", 'Images') 
doc = Document('AC 1 ano III unid - História.docx')
j=0
countPara=0
countImg=0
countAlt=0
countQuest=0
currDesc=[]
quests=[]
currAlts=[]
mapa={}
paras = doc.paragraphs
for para in paras:
    if 'graphicData' in para._p.xml:
        currDesc.append((1,countImg))
        countImg= countImg + 1
    elif re.match(r'^[A-za-z][).-]', para.text):
        currAlts.append((countPara,countAlt))
        #currDesc.append((0,countPara))
        countAlt= countAlt+1
        if countPara==len(paras)-1 or not re.match(r'^[A-za-z][).-]', paras[countPara+1].text):
           quests.append(currAlts)
           mapa[tuple(currAlts)]=currDesc
           currDesc=[]
           currAlts=[]
    else: currDesc.append((0,countPara))
    countPara = countPara + 1
mixOptions=[]
mixQuest=[]
permQuest=[]
finalQuest=[]
for i in quests: mixOptions.append(permutations(i))
mixQuest = islice(product(*mixOptions),10,100,10)
listMixQuest=[]
itemMixQuest=[]
for i in mixQuest:
    for j in i:
        itemMixQuest.append(list(j))
    listMixQuest.append(itemMixQuest)
    itemMixQuest=[] 
for i in listMixQuest:
    for j in i:
        shuffle(j)
for i in listMixQuest: shuffle(i)
countExam=0
for typeExam in listMixQuest:
    newExam = Document('AC 1 ano III unid - História.docx')
    newParas = newExam.paragraphs
    countPara=0
    for para in newParas:
        para.text=''
    for question in typeExam:
        currDesc = mapa[tuple(sorted(question))]
        print(question)
        print(currDesc)
        for i in currDesc:
            print(i)
            if i[0]==1:
                run = newParas[countPara].add_run()
                run.add_picture('Images/'+str(images[i[1]]))
            else:
                #print(i[1])
                #print(paras[i[1]].text)
                newParas[countPara].text = paras[i[1]].text
                print(newParas[countPara].text)
            countPara+=1
        for alt in question:
            newParas[countPara].text = paras[alt[0]].text
            print(newParas[countPara].text)
            countPara+=1
    newExam.save('demo'+str(countExam)+'.docx')
    countExam+=1



