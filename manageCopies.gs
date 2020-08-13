//import {permute, cartesianProduct} from './util.gs'
//import {alternatives} from './manageOriginal.gs'
//const alternatives= require('./manageOriginal').alternatives
//const permute = require('./util').permute
function mkCopy() {
  let id = doc.getId();
  let fileName = doc.getName();
  let folder = DriveApp.createFolder(fileName)
  var newFileName;
  for (let i = 1; i <= 10; i++) {
    newFileName = fileName +" ESTILO "+i;
    let file = DriveApp.getFileById(id).makeCopy(newFileName, folder); 
  }
}
function generateAltsPermutations(){
  let altsPermuts={}
  Logger.log(alternatives_s)
  const altsEntries = Object.entries(alternatives_s)
  Logger.log(altsEntries)
  for (const [id, alt] of altsEntries) {
    Logger.log(id, alt)
    altsPermuts[id] = permute(alt)
    Logger.log(altsPermuts[id])
  }
  return altsPermuts
}

