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
feedback='1A-2B-3C-4A-5D-6E-7E-7A-9A-10A-11B-12C-13D-14E-15C'
answers={}
feedback=feedback.split('-')
treatFeedback=[]
for i in feedback:
    treatFeedback.append(i[len(i)-1]) 
#for i in treatFeedback:
    #print(i)
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
           answers[tuple(currAlts)]=treatFeedback[countQuest]
           #print(answers[tuple(currAlts)])
           currDesc=[]
           currAlts=[]
           countQuest+=1
    else: 
        testPara= para.text.encode('utf-8')
        if re.match(r'^(QUESTÃO|questão)( 01|1)',testPara)or re.match(r'^(01|1)[).-]', testPara):
            #print(endHeader)
            if(endHeader==False):
                endHeader=True
                #print("1 QUESTAO")
                header=currDesc
                #print(header)
                #print(para.text)
                currDesc=[]
                #print(header)
                if re.match(r'^(QUESTÃO|questão)( 01)',testPara):
                    #print("tem q ser 1")
                    typeDescQuest=0
                elif re.match(r'^(QUESTÃO|questão)( 1)',testPara):
                    typeDescQuest=1
                elif re.match(r'^(01)', testPara):
                    if re.match(r'(01)[)]',testPara): typeDescQuest=2
                    elif re.match(r'(01)[.]',testPara): typeDescQuest=3
                    elif re.match(r'(01)[-]',testPara): typeDescQuest=4
                else:
                    if re.match(r'(1)[)]',testPara): typeDescQuest=5
                    elif re.match(r'(1)[.]',testPara): typeDescQuest=6
                    elif re.match(r'(1)[-]',testPara): typeDescQuest=7      
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
    countQuestion=1
    newFeedback=''
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
            #print(newParas[countPara].text)
            #print(countPara)
        countPara+=1
    for question in typeExam:
        currDesc = mapa[tuple(sorted(question))]
        indexAns = ord(answers[tuple(sorted(question))])-65
        ans=sorted(question)[indexAns]
        newIndexAns = question.index(ans)
        newFeedback+=str(countQuestion)+"-"+chr(newIndexAns+65)+" "
        #print(question)
        #print(currDesc)
        for i in currDesc:
            #print(i)
            if i[0]==1:
                run = newParas[countPara].add_run()
                run.add_picture('Images/'+str(images[i[1]]))
            else:
                #print(i[1])
                newDesc = paras[i[1]].text.encode('utf-8')
                #print(paras[i[1]].text)
                if re.match(r'^(QUESTÃO|questão)', newDesc):
                    #print("ENTROOOOU" + str(countQuestion))
                    if typeDescQuest==0:
                        newDesc= newDesc[0:8]+ " "+str(countQuestion).zfill(2)+newDesc[11:]
                    else:
                        if re.match(r'[0-9]', newDesc[10]):
                            newDesc= newDesc[0:8]+ " "+str(countQuestion).zfill(2)+newDesc[11:]
                        else:
                            newDesc= newDesc[0:8]+ " "+str(countQuestion)+newDesc[10:]
                    #print(newDesc)
                elif re.match(r'^[0-9][0-9][).-]', paras[i[1]].text):
                    if re.match(r'^[0-9][0-9][)]', paras[i[1]].text) and typeDescQuest==2:
                        newDesc= str(countQuestion).zfill(2)+newDesc[2:]
                    elif re.match(r'^[0-9][0-9][.]', paras[i[1]].text) and typeDescQuest==3:
                        newDesc= str(countQuestion).zfill(2)+newDesc[2:]
                    elif re.match(r'^[0-9][0-9][-]', paras[i[1]].text) and typeDescQuest==4:
                        newDesc= str(countQuestion).zfill(2)+newDesc[2:]
                elif re.match(r'^[0-9][).-]', paras[i[1]].text):
                    if re.match(r'^[0-9][)]', paras[i[1]].text) and typeDescQuest==5:
                        newDesc= str(countQuestion).zfill(2)+newDesc[1:]
                    elif re.match(r'^[0-9][.]', paras[i[1]].text) and typeDescQuest==6:
                        newDesc= str(countQuestion).zfill(2)+newDesc[1:]
                    elif re.match(r'^[0-9][-]', paras[i[1]].text) and typeDescQuest==7:
                        newDesc= str(countQuestion).zfill(2)+newDesc[1:]
                newDesc = unicode(newDesc, "utf-8")
                newParas[countPara].text = newDesc
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
        countQuestion+=1
    print(newFeedback)
    newExam.save('demo'+str(countExam)+'.docx')
    countExam+=1
    #print(chr(65))



