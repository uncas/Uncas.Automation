# Personal assistant

This folder contains the script for an AI assistant that can do various actions based on the user's input.

The assistant can perform the following actions:
- Check mail (gmail)
- Create mail drafts (gmail)
- Retrieve Jira issues
- Create Jira issues
- Search documents (currently hard-coded to my locally cached documents)
- Search arXiv.org
- Get the news (from Danish news site https://www.dr.dk/nyheder)
- Get the current location (based on IP address)
- Get the weather at a given location
- Find out where a certain movie can be streamed (currently hard-coded to Denmark and my streaming providers)

The assistant can reason about how to do a sequence of actions, for example if I ask about the weather it will first find my location and then find the weather at that location. (See example conversation + more in the Examples section below.)


## Examples

### Example 1: Weather

When I ask:
````
How is the weather?
````
Then it performs the following function calls:
````
Calling function getLocation
Calling function getCurrentWeather with {'countryCode': 'DK', 'city': 'Hørning'}
````
And replies:
````
The current weather in Hørning, Denmark is as follows:
- Temperature: 18.96°C
- Weather: Broken clouds
- Wind: 
  - Speed: 1.34 m/s
  - Gust: 3.58 m/s
  - Direction: 245°
- Cloud Coverage: 68%

Here is the forecast for today:
- 09:00: Temperature 18.96°C, Broken clouds, Moderate wind
- 12:00: Temperature 19.55°C, Light rain, Moderate wind (44% rain probability)
- 15:00: Temperature 19.85°C, Light rain, Moderate wind (95% rain probability)
- 18:00: Temperature 18.53°C, Light rain, Light wind (57% rain probability)
- 21:00: Temperature 13.33°C, Light rain, Light wind (13% rain probability)

If you need more details or a forecast for a specific time, feel free to ask!
````


### Example 2: Check mail and create tasks

When I ask:
````
Check mail and create tasks with suggested steps based on the mails.
````
It makes the following operations:
````
Calling function readEmail
Calling function createJiraIssue with {'summary': 'Discuss OKR presentation with team', 'description': 'Schedule a meeting to discuss the OKR presentation.'}
Calling function createJiraIssue with {'summary': 'Summer canteen arrangements', 'description': "Ensure that the summer canteen schedule is coordinated for the upcoming weeks based on Jane's email."}
````
And replies:
````
Tasks have been created based on the emails:
1. Task: Discuss OKR presentation with team
   Description: Schedule a meeting to discuss the OKR presentation.

2. Task: Summer canteen arrangements
   Description: Ensure that the summer canteen schedule is coordinated for the upcoming weeks based on Jane's email.

You can track these tasks with the given Jira issue keys:
1. Task: Discuss OKR presentation with team
   Jira Issue Key: EXAMPLE-404

2. Task: Summer canteen arrangements
   Jira Issue Key: EXAMPLE-405
````


### Example 3: Work-related questions or instructions that it can handle

- `Summarize my mail inbox.`
- `Check mail and create tasks with steps based on the mails.`
- `Write a mail to my-colleagues@example.com about how the OKR process works.`
- `Create a task for me to fix the bug in the home page.`
- `How are we using OKRs in our company?`
- `Summarize the most recent research about AI Agents.`
- `What are the most recent tech-related news?`


### Example 4: Other questions or instructions that it can handle

- `Write a mail to my-studying-son@example.com about how the photosynthesis works.`
- `Where can I watch The Godfather?`
- `How is the weather?`
- `Suggest some fun outdoor activities that suits the current weather.`
- `What do I need to wear today?`


### Example 5: Questions or instructions that it can *not* handle

- `Suggest some fun outdoor activities.` (For some reason it cannot figure out to call the functions to get my current location and the current weather.)
- `Find latest research about biology` followed up by `Can you summarize more information about article 2?` (Results in an error because it calls the DR news details method with a URL from an arXiv article.)



## How to use it

If you have already performed the first-time configuration below,
then you can run the AI assistant by:
- Open a terminal window in the root folder of the repository.
- Run this in the terminal:
  - Mac: `./run.sh`
  - Windows: `run.cmd`


### First-time Configuration

Requirements:

- Git ([install Git](https://git-scm.com/))
- Python ([install Python](https://www.python.org/downloads/))
- Clone this repository, for example by running this in a terminal:

      git clone https://github.com/uncas/Uncas.Automation.git

Depending on which functionality you are going to use, you will need to define various environment variables:

- Create a `.env` file in the root of the repository.
- Add the following environment variables (or only the ones you will need):
````
# Required for the AI Assistant to run:
OPENAI_API_KEY=INSERT_YOUR_VALUE_HERE # From https://platform.openai.com/api-keys

# If using Jira:
ATLASSIAN_API_TOKEN=INSERT_YOUR_VALUE_HERE # From https://id.atlassian.com/manage-profile/security/api-tokens
ATLASSIAN_USER=INSERT_YOUR_VALUE_HERE # From https://id.atlassian.com/manage-profile/profile-and-visibility
JIRA_SERVER=INSERT_YOUR_VALUE_HERE # For example https://example-jira.atlassian.net
JIRA_PROJECT=INSERT_YOUR_VALUE_HERE # For example SITEOPS

# If querying for weather:
OpenWeatherMap_Api_Key=INSERT_YOUR_VALUE_HERE # From https://home.openweathermap.org/api_keys

# If querying for movies:
THEMOVIEDB_API_KEY=INSERT_YOUR_VALUE_HERE # From https://www.themoviedb.org/settings/api
THEMOVIEDB_ACCESS_TOKEN=INSERT_YOUR_VALUE_HERE # From https://www.themoviedb.org/settings/api
````

For the Google integration (gmail, docs):
- Enable Google API ([read about how](https://developers.google.com/docs/api/quickstart/python)).
- Save Google credentials file as `Config/GoogleCredentials.json` (i.e. in the `Config` folder which is a sub folder of the root folder of the repository).


## How it works

This script leverages Open AI functions to enable the LLM to decide on different actions to take.

[Read about function calling](https://platform.openai.com/docs/guides/function-calling)


## Inspiration

Inspired by the section about "Build Apps with LangChain" in the AI Engineering course on Scrimba:
https://v2.scrimba.com/the-ai-engineer-path-c02v


## TODOs & Draft notes & thoughts

Completing ongoing work:
- Implement sync of documentation (currently it only uses documents that I downloaded in a separate thread).

Improving functionality:
- Properly extract email body for all kinds of messages (currently some are missing).

Generic ideas:
- Fetching docs, mail, calendar from different Google accounts.
- Unit testing.

Work-related Use case ideas:
- Get calendar events
- Create calendar event
- Prepare meetings for the following week... (research + people styles)

Private time / Leisure time Use case ideas:
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
- Taking input and saving to journal
- Based on conversation, suggest tasks to be added to Trello, or information to be added to tasks in Trello.

- Finde events (for eksempel jeg sad og skulle finde friluftsspil på Moesgaard, Ragnarok eller Snedronningen, men det var ikke muligt for mig at finde det)
- At skrive noget til assistenten og så få det tilføjet til dagbog eller idé-bank eller regn-log eller lignende...


### Things that I typically do manually

- Check my calendar for the day (work + family)
- Check the weather for the day
- Check email (work + private)
- Check slack (work)
- Registering rain fall in my garden
- Checking the climate / typical weather in holiday target locations
- Researching holiday options
- Find a picture of someone at some specific place (or at a specific age). Could search google photos!
- Categorize pictures...
