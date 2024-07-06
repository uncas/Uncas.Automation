# Personal assistant

## Background

Inspired by the section about "Build Apps with LangChain" in the AI Engineering course on Scrimba:
https://v2.scrimba.com/the-ai-engineer-path-c02v


## Use cases

The following are some examples of questions that are supported:

Generic:
- Get my current location. (Based on IP address.)

Work-related:
- Questions that query documentation. (Based on retrieval of Google documents, embedding and searching.)

Private time / Leisure time:
- Where can I watch a certain movie? (Based on lookup in the movie db's API.)
- Get the latest news. (Based on lookup in RSS feed from dr.dk.)
- What is the current weather? (Fake implementation. Not yet implemented an API lookup.)


## TODOs

Completing ongoing work:
- Implement sync of documentation.

Generic ideas:
- Keep the chat thread going, remembering previous messages.
- Let the agent ask me for input, if the agent is in doubt about some questions.
- Fetching docs, mail, calendar from different Google accounts.
- Unit testing

Work-related Use case ideas:
- Prepare meetings for the following week... (research + people styles)

Private time / Leisure time Use case ideas:
- Get news in Denmark/other places (dr.dk API / RSS feeds).
- Find movies available on my streaming services.
  - Bonus 1: Only movies that I have not yet seen.
  - Bonus 2: Filtering by: New movies, Genre, Language, Actors, Directors.
  - Bonus 2: Highlight movies that might match my favorite movies.

Resource ideas (to improve the data that the assistant can use):
- Include the personal "about me" google doc I have
- Include my company readme

Misc notes & random thoughts, that are not yet sorted:
- Some idea about stuff specific to the local machine.
- For each start: A session starts, with the messages saved to a json file.
- A HTML page that can list the sessions, viewing the conversations.
- Get books
- Read mail
- Send mail (pending confirmation or a draft mail)
- Taking input and saving to garden journal or storing in other journals
- Based on conversation, suggest tasks to be added to Trello, or information to be added to tasks in Trello.


- Finde events (for eksempel jeg sad og skulle finde friluftsspil på Moesgaard, Ragnarok eller Snedronningen, men det var ikke muligt for mig at finde det)
- At skrive noget til assistenten og så få det tilføjet til dagbog eller idé-bank eller regn-log eller lignende...


## Things that I typically do manually

- Check my calendar for the day (work + family)
- Check the weather for the day
- Check email (work + private)
- Check slack (work)
- Registering rain fall in my garden
- Checking the climate / typical weather in holiday target locations
- Researching holiday options