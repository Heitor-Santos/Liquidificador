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
endHeader= False
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
    else: 
        testPara= para.text.encode('utf-8')
        if re.match(r'^(QUESTÃO|questão)( 01|1)',testPara)or re.match(r'^(01|1)[).-]', testPara):
            print(endHeader)
            if(endHeader==False):
                endHeader=True
                print("1 QUESTAO")
                header=currDesc
                print(header)
                print(para.text)
                currDesc=[]
                print(header)
        currDesc.append((0,countPara))
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
    for i in header:
        if i[0]==1:
            run = newParas[countPara].add_run()
            run.add_picture('Images/'+str(images[i[1]]))
        else:
            #print(i[1])
            #print(paras[i[1]].text)
            newParas[countPara].text = paras[i[1]].text
            print(newParas[countPara].text)
            print(countPara)
        countPara+=1
    for question in typeExam:
        currDesc = mapa[tuple(sorted(question))]
        #print(question)
        #print(currDesc)
        for i in currDesc:
            #print(i)
            if i[0]==1:
                run = newParas[countPara].add_run()
                run.add_picture('Images/'+str(images[i[1]]))
            else:
                #print(i[1])
                #print(paras[i[1]].text)
                newParas[countPara].text = paras[i[1]].text
                #print(newParas[countPara].text)
            countPara+=1
        indexAlt=0
        for alt in question:
            newAlt= unicode(paras[alt[0]].text.encode('utf-8'), "utf-8")
            newAlt = chr(indexAlt+65) + newAlt[1:]
            #print(newAlt)
            newParas[countPara].text = newAlt
            #print(newParas[countPara].text)
            countPara+=1
            indexAlt+=1
    newExam.save('demo'+str(countExam)+'.docx')
    countExam+=1
    #print(chr(65))



