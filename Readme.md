# Automation scripts

* Python script for running locally:
  * Running on Windows: run.cmd
  * Running on Mac: run.sh

* Clasp folder: Google Apps script for deploying to apps script and running there:
  * Overview: Generates HTML for an overview page of calendar, mail, and Trello tasks.


## TODO

### Bugs

### Feature ideas

- Take the document search result and feed into LLM to generate a good answer to the question.
- Read emails and propose some replies.
- OpenAI:
  - Ask ChatGpt
  - DallE: img2txt, txt2img
- Generate image locally:
  - Via Automatic1111 API: https://github.com/AUTOMATIC1111/stable-diffusion-webui/wiki/API
  - Or: https://analyticsindiamag.com/how-to-generate-an-image-from-text-using-stable-diffusion-on-python/
- Voice
- Use sandbox/LocalGpt/Gpt2.py: Faster than dolly!


#### Intelligent assistant

What are the most important things?
* Working efficiently
* Keeping on track, staying focused
* Maintaining an overview of the "world situation"
* Process things quickly and efficiently

Overview:
* Page that lists important things
* Next things to do from calendar (Google calendar)
* Next things to do from todo lists (Trello, Jira)
* New messages to reply to or register (email, slack, messenger, Aula, Facebook groups)
* My recurring things to practice or work on (Google Sheets)
* Proposed plan for the rest of the day (based on a. fixed appointments in calendar, b. recurring plan, c. todos, d. messages)
* Scheduled tasks for a specific due date.
* Year wheel: Things to be done in a certain week or a certain month, every year
* Allow for travel time, break time, buffer time, and sumpe-tid!

System integrations:
* Trello: Via an API
* Messenger & Facebook Groups: Via an API: https://developers.facebook.com/apps/creation/
* Aula: No API available, but someone did it by scraping HTML: https://helmstedt.dk/2020/05/et-lille-kig-paa-aulas-api/

Todos regarding intelligent assistant:
* Research whether an intelligent scheduler/organizer already exists (that can combine fixed appointments with other tasks or recurring tasks).
  * Paid solutions exist (Chronofy, Zapier), but none that can do what I'm after.
* Research APIs to Trello, Aula, Messenger, Facebook groups
* Sketch a simple proof-of-concept

Solution ideas:
* Proof-of-concept:
  * Coding platform:
    * Python script
      * Cons: Can not be scheduled easily (unless I set it up in Google Cloud?!)
    * Google Apps script
      * Pros: Can be scheduled easily
  * Output:
    * Static html page on the local computer
      * Cons:
        * Only accessible on that computer
    * Table in a Google Sheet
      * Pros:
        * Can be accessed anywhere
        * Easy to output to (at least from Google Apps script)
    * Google calendar
      * Cons: Difficult to keep up to date
  * Features:
    * Version 1:
      * List of calendar events today
      * List of emails
      * List of todo's from Trello
      * List of recurring todo's from sheet
      * How should they be organized:
        * In one list, with a block per hour
        * Indicate type
    * Proposed plan for rest of today + tomorrow
      * Base plan on:
      * Calendar events
      * List of recurring tasks (from Google Sheet)
      * List of prioritized tasks (from Trello)
      * Time to process income mails and other messages

Devils Advocate:
* YAGNI:
  * Isn't this possible using some existing system? No.
  * Do I really have to code all this in order for such an overview / intelligent assistant to work?
  * Do I really need this? Is this really what would bring me value?

* Apps Script: https://script.google.com/home/projects/18ayojSkuvHNVS25vq79gJAlamgv6OL4VcUAtYtFnLXJA52uYn6_vn7fA/edit
* Output widget: https://script.google.com/macros/s/AKfycbzO-LWqM-eQdf2j0YXuovWsceBqo1yVfCSbdjtrRHFsEzYVPRnUkmfuH6tL4Zr7mAM/exec
* Site: https://sites.google.com/view/olelynge-overblik

### DevOps tasks

- Run tests