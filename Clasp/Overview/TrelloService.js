function debugTrelloCards() {
  getTrelloCards().forEach(function(card) {
    Logger.log(card);
  });
}

function getTrelloCardsHtml() {
  return "<ul>" + getTrelloCards().map(function(card) {
    return "<li><a target='_blank' href='" + card.url + "'>" + card.name + "</a></li>";
  }).reduce((previous, current) => previous + "\n" + current, "") + "\n</ul>";
}

function getTrelloCards() {
  const scriptProperties = PropertiesService.getScriptProperties();
  var listId = scriptProperties.getProperty("Trello.ListId");
  var url = 'https://api.trello.com/1/lists/' + listId + "/cards";
  const ignoreLabelId = scriptProperties.getProperty("Trello.IgnoreLabelId");
  return getTrelloStuff(url).filter(card => !card.idLabels.includes(ignoreLabelId));
}

function listTrelloLists() {
  const boardId = PropertiesService.getScriptProperties().getProperty("Trello.BoardId");
  var url = "https://api.trello.com/1/boards/" + boardId + "/lists";
  var lists = getTrelloStuff(url);
  lists.forEach(function(list){
    Logger.log(list.name + ": " + list.id);
  });
}

function listTrelloBoards() {
  var url = "https://api.trello.com/1/members/me/boards";
  var boards = getTrelloStuff(url);
  boards.forEach(function(board){
    Logger.log(board.name + ": " + board.id);
  });
}

function getTrelloStuff(url) {
  const scriptProperties = PropertiesService.getScriptProperties();
  const apiKey = scriptProperties.getProperty("Trello.ApiKey");
  const apiToken = scriptProperties.getProperty("Trello.ApiToken");
  const fullUrl = url + "?key=" + apiKey + '&token=' + apiToken;
  var response = UrlFetchApp.fetch(fullUrl);
  var json = response.getContentText();
  return JSON.parse(json);
}