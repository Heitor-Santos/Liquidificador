function uuidv4() {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
    var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
    return v.toString(16);
  });
}
function getElementText(el){
  let text
  if(el.isPartial()){
    let startIndex = el.getStartOffset();
    let endIndex = el.getEndOffsetInclusive()+1
    text = el.getElement().asText().getText().substring(startIndex,endIndex).toString()
  }
  else text = el.getElement().asText().getText().toString()
  return text
}
function permute(input){
  var permArr = [], usedChars = [];
  return permuteHelp(input)
  function permuteHelp(input) {
    var i, ch;
    for (i = 0; i < input.length; i++) {
      ch = input.splice(i, 1)[0];
      usedChars.push(ch);
      if (input.length == 0) {
        permArr.push(usedChars.slice());
      }
      permuteHelp(input);
      input.splice(i, 0, ch);
      usedChars.pop();
    }
    return permArr
  };
}
function helpDocExists(){
  try{
     let helpDocId = PropertiesService.getDocumentProperties().getProperty('helpDocId')
     if(helpDocId==null)return false
     return true
  }
  catch(error){
    throw new Error('algo inesperado ocorreu em helpDocExists')
  }
}
function getHelpDocId(){
  try{
    let helpDocId = PropertiesService.getDocumentProperties().getProperty('helpDocId')
    return helpDocId;
  }
  catch(error){
    throw new Error('algo inesperado ocorreu em getHelpDocId')
  }
}
function setHelpDocId(helpDocId){
  try{
    PropertiesService.getDocumentProperties().setProperty('helpDocId', helpDocId)
  }
  catch(error){
    throw new Error('algo inesperado ocorreu em setHelpDocId')
  }
}
function seQuestionIndexes(question, ){
  try{
    PropertiesService.getDocumentProperties().setProperty('helpDocId', helpDocId)
  }
  catch(error){
    throw new Error('algo inesperado ocorreu em setHelpDocId')
  }
}
function deleteHelpDocId(){
  try{
    PropertiesService.getDocumentProperties().deleteProperty('helpDocId')
  }
  catch(error){
    throw new Error('algo inesperado ocorreu em deleteHelpDocId')
  }
}
function setAlternatives(id, alternativesList){
  try{
    let alternatives = PropertiesService.getDocumentProperties().getProperty('alternatives')
    if(alternatives==null)alternatives={}
    alternatives[id] = alternativesList
    PropertiesService.getDocumentProperties().setProperty('alternatives', alternatives)
  }
  catch(error){
    throw new Error('algo inesperado ocorreu em setAlternatives')
  }
}
function cartesianProduct(arr) {
    return arr.reduce(function(a,b){
        return a.map(function(x){
            return b.map(function(y){
                return x.concat([y]);
            })
        }).reduce(function(a,b){ return a.concat(b) },[])
    }, [[]])
}
//module.exports(uuidv4, getElementText, permute, cartesianProduct)


