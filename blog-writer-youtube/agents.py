from crewai import Agent,LLM
from tools import youtube_tool
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
load_dotenv()


llm = LLM(
        model='gemini/gemini-2.0-pro-exp-02-05',
        verbose=True,
        temperature=0.5,
        google_api_key=os.getenv("GOOGLE_API_KEY"))

# create senier blog content researcher
researcher = Agent(
    role = "Blog researcher from youtube videos",
    goal = "Get the relavent video content fro the  topic: {topic} from the youtube",
    verbose= True,
    memory=True,
    backstory="Expert in understanding videos in AI, Machine Learning, Deep learning, Natural Language Processing, Gen AI and Reinforcemnt learning. And providing the suggestions",
    tools=[youtube_tool],
    llm=llm,
    allow_delegation=True)

#  Creating a senior blog writer agent with YT tool

blog_writer = Agent(
    role = "Blog writer",
    goal = "Narrate compelling tech stories about the video {topic} from the youtube",
    verbose= True,
    memory=True,
    backstory="With a flair for simplifying complex topics, you craft engaging narratives that captivate and educate, bringing new discoveries to light in an accessible manner",
    llm=llm,
    tools=[youtube_tool],
    allow_delegation=False
)