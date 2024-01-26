function debug() {
  Logger.log(getHtml());
}

function doGet() {
  return HtmlService.createHtmlOutput(getHtml());
}

function getHtml() {
  return Array.from(getHtmlParts()).reduce((previous, current) => previous + "\n\n" + current, "");
}

function* getHtmlParts() {
  yield getCalendarHtml();
  yield getChecklistThingsToDoTodayHtml();
  yield getTrelloCardsHtml();
  yield getInboxHtml();
  yield "<p>Opdateret " + Utilities.formatDate(new Date(), CalendarApp.getTimeZone(), "HH:mm:ss") + ".</p>";
}

function getCalendarHtml() {
  const events = getCalendar();
  if (events.length == 0) return "";

  const timeZone = CalendarApp.getTimeZone();
  return "<h3>Kalender</h3><ul>" + events.map(function(event) {
    const start = Utilities.formatDate(event.startTime, timeZone, "HH:mm")
    const end = Utilities.formatDate(event.endTime, timeZone, "HH:mm")
    return "<li>" + start + "-" + end + ": " + event.title + "</li>";
  }).reduce((previous, current) => previous + "\n" + current, "") + "\n</ul>";
}

function getCalendar() {
  const now = new Date();
  const tomorrow = new Date();
  tomorrow.setDate(tomorrow.getDate() + 1);
  const events = CalendarApp.getEvents(now, tomorrow);
  return events.map(function(event) {
    return {title: event.getTitle(), startTime: event.getStartTime(), endTime: event.getEndTime()};
  });
}

function getInboxHtml() {
  const inboxThreads = getInboxThreads();
  if (inboxThreads.length == 0) return "";

  return "<h3>Indbakke</h3><ul>" + inboxThreads.map(function(thread){
    const url = "https://mail.google.com/mail/u/0/#inbox/" + thread.messageId;
    return "<li><a target='_blank' href='" + url + "'>" + thread.subject + "</a></li>";
  }).reduce((previous, current) => previous + "\n" + current, "") + "\n</ul>";
}

function getInboxThreads() {
  const threads = GmailApp.getInboxThreads();
  return threads.map(function(thread){
    const firstMessage = thread.getMessages()[0];
    const subject = firstMessage.getSubject();
    const id = firstMessage.getId();
    return {subject: subject, messageId: id};
  });
}