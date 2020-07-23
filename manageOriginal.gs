/**
 * Creates a menu entry in the Google Docs UI when the document is opened.
 * This method is only used by the regular add-on, and is never called by
 * the mobile add-on version.
 *
 * @param {object} e The event parameter for a simple onOpen trigger. To
 *     determine which authorization mode (ScriptApp.AuthMode) the trigger is
 *     running in, inspect e.authMode.
 */
function onOpen(e) {
  DocumentApp.getUi().createAddonMenu()
      .addItem('Start', 'showSidebar')
      .addToUi();
  
}

/**
 * Runs when the add-on is installed.
 * This method is only used by the regular add-on, and is never called by
 * the mobile add-on version.
 *
 * @param {object} e The event parameter for a simple onInstall trigger. To
 *     determine which authorization mode (ScriptApp.AuthMode) the trigger is
 *     running in, inspect e.authMode. (In practice, onInstall triggers always
 *     run in AuthMode.FULL, but onOpen triggers may be AuthMode.LIMITED or
 *     AuthMode.NONE.)
 */
function onInstall(e) {
  onOpen(e);
}
/**
 * Opens a sidebar in the document containing the add-on's user interface.
 * This method is only used by the regular add-on, and is never called by
 * the mobile add-on version.
 */
function showSidebar() {
  var ui = HtmlService.createHtmlOutputFromFile('liquidificador').setTitle('Liquidificador');
  DocumentApp.getUi().showSidebar(ui);
}

function removeAlternatives(altFormat, currQuestion){
  let currAlts= []
  let toExclude=[]
  const formatOptions ={
    "LATIN_UPPER": DocumentApp.GlyphType.LATIN_UPPER,
    "LATIN_LOWER": DocumentApp.GlyphType.LATIN_LOWER,
    "ROMAN_UPPER": DocumentApp.GlyphType.ROMAN_UPPER,
    "ROMAN_LOWER": DocumentApp.GlyphType.ROMAN_LOWER
  }
  currQuestion["value"].map((el)=>{
     const elType = el.getElement().getType()
     const elText = getElementText(el)
     if(elType==DocumentApp.ElementType.LIST_ITEM && el.getElement().getGlyphType()==formatOptions[altFormat]){
       currAlts.push(elText)
       toExclude.push(el)
     }
  }) 
  Logger.log(currQuestion["id"]+" "+ currAlts)
  setAlternatives(currQuestion["id"], currAlts)
  currQuestion["value"] =  currQuestion["value"].filter((el)=>!toExclude.includes(el))
  return currQuestion["value"];
}
function addQuestionOnHelpDoc(helpDoc, currQuestion){
  let numElementsOnDocHelp =0
  currQuestion["value"].map((el)=>{
     const elType = el.getElement().getType()
     const elContent = el.getElement().copy() 
     switch(elType){
       case DocumentApp.ElementType.HORIZONTAL_RULE:
         helpDoc.getBody().appendHorizontalRule(elContent)
         numElementsOnDocHelp++
         break
       case DocumentApp.ElementType.INLINE_IMAGE:
         helpDoc.getBody().appendImage(elContent)
         numElementsOnDocHelp++
         break
       case DocumentApp.ElementType.PAGE_BREAK:
         helpDoc.getBody().appendPageBreak(elContent) 
         numElementsOnDocHelp++
         break
       case DocumentApp.ElementType.PARAGRAPH:
         helpDoc.getBody().appendParagraph(elContent) 
         numElementsOnDocHelp++
         break
       case DocumentApp.ElementType.TABLE:
         helpDoc.getBody().appendTable(elContent) 
         numElementsOnDocHelp++
         break
     }
  })
  let firstEl = helpDoc.getBody().getChild(1)
  let elType = firstEl.getType()
     let elContent = firstEl.copy() 
     Logger.log(elContent.asText().getText())
     Logger.log(elType)
     switch(elType){
       case DocumentApp.ElementType.HORIZONTAL_RULE:
         helpDoc.getBody().appendHorizontalRule(elContent)
         break
       case DocumentApp.ElementType.INLINE_IMAGE:
         helpDoc.getBody().appendImage(elContent)
         break
       case DocumentApp.ElementType.PAGE_BREAK:
         helpDoc.getBody().appendPageBreak(elContent) 
         break
       case DocumentApp.ElementType.PARAGRAPH:
         helpDoc.getBody().appendParagraph(elContent) 
         break
       case DocumentApp.ElementType.TABLE:
         helpDoc.getBody().appendTable(elContent) 
         break
     }
  lastEl = helpDoc.getBody().getChild(numElementsOnDocHelp)
  elType = lastEl.getType()
  elContent = lastEl.copy()
  Logger.log(elContent.asText().getText())
  Logger.log(elType)
     switch(elType){
       case DocumentApp.ElementType.HORIZONTAL_RULE:
         helpDoc.getBody().appendHorizontalRule(elContent)
         numElementsOnDocHelp++
         break
       case DocumentApp.ElementType.INLINE_IMAGE:
         helpDoc.getBody().appendImage(elContent)
         numElementsOnDocHelp++
         break
       case DocumentApp.ElementType.PAGE_BREAK:
         helpDoc.getBody().appendPageBreak(elContent) 
         numElementsOnDocHelp++
         break
       case DocumentApp.ElementType.PARAGRAPH:
         helpDoc.getBody().appendParagraph(elContent) 
         numElementsOnDocHelp++
         break
       case DocumentApp.ElementType.TABLE:
         helpDoc.getBody().appendTable(elContent) 
         numElementsOnDocHelp++
         break
     }
}
function addQuest(questRe, altFormat){
  const doc = DocumentApp.getActiveDocument()
  let helpDoc
  //PropertiesService.getDocumentProperties().deleteAllProperties()
  const helpDocName = "ARQUIVO DE AUXÍLIO "+doc.getName()
  if (helpDocExists()){
    helpDoc = DocumentApp.openById(getHelpDocId()) 
  }
  else{
    helpDoc = DocumentApp.create(helpDocName)
    setHelpDocId(helpDoc.getId())
  }
  const selection = doc.getSelection()
  let currQuestionElements;
  let firstElement;
  let questionBeginning;
  try{
    if(selection!=null){
      currQuestionElements = selection.getRangeElements()
      firstElement = currQuestionElements[0].getElement()
      if(firstElement.getType()!= DocumentApp.ElementType.TEXT){
        if((firstElement.getType()== DocumentApp.ElementType.PARAGRAPH && getElementText(currQuestionElements[0]))=="" ||
          firstElement.getType()!= DocumentApp.ElementType.PARAGRAPH){
            throw new Error('A questão deve começar com texto')
          }
      }
      let currQuestion={"value":currQuestionElements,"id":uuidv4()}
      currQuestion["value"]=removeAlternatives(altFormat, currQuestion)
      addQuestionOnHelpDoc(helpDoc, currQuestion)
      questionBeginning = getElementText(currQuestion["value"][0]).substr(0,50)+'...';
      return ({"value":questionBeginning,"id": currQuestion["id"]});
    }
    else throw new Error('Nenhuma questão selecionada')
  }
  catch(error){
    throw new Error(error)
  }
}

function delQuest(idsToDelete){
  try{
    Logger.log("oi")
    //questions_s = questions_s.filter((quest)=>!idsToDelete.includes(quest["id"]))
  }
  catch(error){
    throw new Error(error)
  }
}





