function debug_getChecklistThingsToDoToday() {
	Logger.log(getChecklistThingsToDoTodayHtml(PropertiesService.getScriptProperties().getProperty("Checklist.SheetId")));
}
  
function debug_getSheetValues() {
	Logger.log(getChecklist(PropertiesService.getScriptProperties().getProperty("Checklist.SheetId")));
}
  
function getChecklistThingsToDoTodayHtml(checklistSheetId) {
	return "<ul>" + getChecklistThingsToDoToday(checklistSheetId).map(function(thing) {
	  return "<li>" + thing.title + "</li>";
	}).reduce((previous, current) => previous + "\n" + current, "") + "\n</ul>";
}
  
function getChecklistThingsToDoToday(checklistSheetId) {
	const checklist = getChecklist(checklistSheetId);
	let today = new Date().getDay(); // Sunday = 0, Monday = 1, etc...
	if (today == 0) today = 7;
	const updated = checklist[1].slice(1).map((value, index) => [value,index]).filter(x => x[0])[0][1]; // Monday = 1, ... Sunday = 7
	const items = checklist.slice(2);
	const progress = items.map(item => {
	  const title = item[0];
	  const target = item[1];
	  const doneToday = item[today + 1] ? 1 : 0;
	  const actual = item.slice(2).filter(x => x).length;
	  if (target == 0) return null;
  
	  const progress = actual / target;
	  return {title: title, target: target, actual: actual, progress: progress, doneToday: doneToday};
	}).filter(item => item && item.progress < 1 && !item.doneToday).sort((a,b) => a.progress - b.progress);
	return progress;
}
  
function getChecklist(checklistSheetId) {
	return getSheetValues(checklistSheetId, "Checklist");
}
  
function getSheetValues(spreadsheetId, sheetName) {
	const spreadsheet = SpreadsheetApp.openById(spreadsheetId);
	const sheet = spreadsheet.getSheetByName(sheetName);
	return sheet.getDataRange().getValues();
}
  