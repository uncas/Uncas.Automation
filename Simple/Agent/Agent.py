# https://til.simonwillison.net/llms/python-react-pattern
import re
import httpx

systemPrompt = """
Every time I ask you something you answer with a Thought and either an Action or an Answer.
If you already know the answer, then output a Thought and an Answer; do not output an Action when you already know the answer!
If you do not know the answer, then output a Thought and an Action.
Use Thought to describe your thoughts about the question you have been asked.
Use Action to run one of the actions available to you.
Only answer with Thought, Action, or Answer. Do not answer with Observation or other output.

Your available actions are:

calculate:
e.g. calculate: 4 * 7 / 3
Runs a mathematical calculation and returns the number - uses Python so be sure to use floating point syntax if necessary

wikipedia:
e.g. wikipedia: Django
Returns a summary from searching Wikipedia

simon_blog_search:
e.g. simon_blog_search: Django
Search Simon's blog for that term

get_location:
e.g. get_location: me
Returns the current location for the provided user

get_location_weather:
e.g. get_location_weather: London
Returns the weather for the provided location (London in this example)


Example 1:

Question: What is the capital of France?

You output:

Thought: I already know that Paris is the capital of France.
Answer: Paris is the capital of France


Example 2:

Question: How many people live in France?

You output:

Thought: I should look up France on Wikipedia
Action: wikipedia: France

Then I will perform the wikipedia lookup and give you a result in a format similar to the following:

Observation: France is a country. The capital is Paris. France has a total population of 68.4 million as of January 2024.

Then you can output an answer since the observation contained the necessary information:

Thought: I see, now I know the population of France.
Answer: The population of France is 68.4 million.
""".strip()


action_re = re.compile('^Action: (\w+): (.*)$')

def query(question, max_turns=5):
    from ChatBot import ChatBot
    bot = ChatBot(systemPrompt)
    next_prompt = question
    for _ in range(max_turns):
        result = bot(next_prompt)
        print(" -- Result: ",result)
        actions = [action_re.match(a) for a in result.split('\n') if action_re.match(a)]
        if actions:
            # There is an action to run
            action, action_input = actions[0].groups()
            if action not in known_actions:
                raise Exception("Unknown action: {}: {}".format(action, action_input))
            print(" -- running {} {}".format(action, action_input))
            observation = known_actions[action](action_input)
            print(" -- Observation: ", observation)
            next_prompt = "Observation: {}".format(observation)
        else:
            return


def wikipedia(q):
    import wikipedia
    pages = wikipedia.search(q)
    page = pages[0]
    return wikipedia.summary(page, sentences = 10)

def simon_blog_search(q):
    results = httpx.get("https://datasette.simonwillison.net/simonwillisonblog.json", params={
        "sql": """
        select
          blog_entry.title || ': ' || substr(html_strip_tags(blog_entry.body), 0, 1000) as text,
          blog_entry.created
        from
          blog_entry join blog_entry_fts on blog_entry.rowid = blog_entry_fts.rowid
        where
          blog_entry_fts match escape_fts(:q)
        order by
          blog_entry_fts.rank
        limit
          1""".strip(),
        "_shape": "array",
        "q": q,
    }).json()
    return results[0]["text"]

def get_location(who):
    return "Odder, Denmark"

def get_location_weather(location):
    return "17 Celcius, Raining"

def calculate(what):
    return eval(what)

known_actions = {
    "wikipedia": wikipedia,
    "calculate": calculate,
    "simon_blog_search": simon_blog_search,
    "get_location": get_location,
    "get_location_weather": get_location_weather
}

input = input("Question: ")
query(input)

#print(wikipedia("France"))