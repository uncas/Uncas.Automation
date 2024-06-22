# https://til.simonwillison.net/llms/python-react-pattern
import re
import httpx

prompt = """
You run in a loop of Thought, Action, PAUSE, Observation.
At the end of the loop you output an Answer
Use Thought to describe your thoughts about the question you have been asked.
Use Action to run one of the actions available to you - then return PAUSE.
Observation will be the result of running those actions.

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
Returns your current location

get_weather:
e.g. get_weather: London
Returns the weather for that location

Always look things up on Wikipedia if you have the opportunity to do so.

Example session:

Question: What is the capital of France?
Thought: I should look up France on Wikipedia
Action: wikipedia: France
PAUSE

You will be called again with this:

Observation: France is a country. The capital is Paris.

You then output:

Answer: The capital of France is Paris
""".strip()


action_re = re.compile('^Action: (\w+): (.*)$')

def query(question, max_turns=5):
    from ChatBot import ChatBot
    bot = ChatBot(prompt)
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
    return httpx.get("https://en.wikipedia.org/w/api.php", params={
        "action": "query",
        "list": "search",
        "srsearch": q,
        "format": "json"
    }).json()["query"]["search"][0]["snippet"]


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

def get_weather(location):
    return "17 Celcius, Raining"

def calculate(what):
    return eval(what)

known_actions = {
    "wikipedia": wikipedia,
    "calculate": calculate,
    "simon_blog_search": simon_blog_search,
    "get_location": get_location,
    "get_weather": get_weather
}

input = input("Question: ")
query(input)