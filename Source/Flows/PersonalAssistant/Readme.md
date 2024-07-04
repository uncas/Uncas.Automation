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
- Implement the weather lookup.

Generic ideas:
- Keep the chat thread going, remembering previous messages.

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
