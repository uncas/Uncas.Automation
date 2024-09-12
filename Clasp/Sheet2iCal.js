/*Creating a web server in Google Sheets to output data from a named range in iCalendar (iCal) format involves using Google Apps Script. Here's how you can do it:
Create the Google Apps Script Project:
Open your Google Sheet.
Go to Extensions > Apps Script.
Write the Script:
Replace any existing code in the script editor with the following:
*/

function doGet() {
	return ContentService.createTextOutput(getICalData())
	  .setMimeType(ContentService.MimeType.ICAL);
  }
  
  function getICalData() {
	// Replace 'NamedRange' with your actual named range
	var sheet = SpreadsheetApp.getActiveSpreadsheet().getRangeByName('NamedRange');
	var data = sheet.getValues();
  
	var icalString = "BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:-//Your Organization//NONSGML v1.0//EN\n";
  
	for (var i = 0; i < data.length; i++) {
	  var date = new Date(data[i][0]); // Assuming the date is in the first column
	  var description = data[i][1]; // Assuming the activity is in the second column
  
	  // Format the date for iCal (YYYYMMDD)
	  var formattedDate = Utilities.formatDate(date, Session.getScriptTimeZone(), 'yyyyMMdd');
  
	  icalString += "BEGIN:VEVENT\n";
	  icalString += "DTSTART;VALUE=DATE:" + formattedDate + "\n";
	  icalString += "DTEND;VALUE=DATE:" + formattedDate + "\n";
	  icalString += "SUMMARY:" + description + "\n";
	  icalString += "END:VEVENT\n";
	}
  
	icalString += "END:VCALENDAR";
  
	return icalString;
  }