from crewai import Task
from tools import youtube_tool
from agents import blog_writer,researcher

#  Research task
research_task =  Task(
    description=(  # Corrected typo from 'desccription' to 'description'
        "Identify the video {topic}. "
        "Get detailed information about the video from YouTube."
    ),
         expected_output="A comprehensive 3 paragraphs long report based on the {topic} of video content",
         tools=[youtube_tool],
         agent=researcher,
)

#  Research task
write_task =  Task(
    description=(  # Corrected typo from 'desccription' to 'description'
        "Get the information from YouTube on the topic {topic}."
    ),
         expected_output="Summarize the info from the youtube video on the topic {topic} and create the content for the blog",
         tools=[youtube_tool],
         agent=blog_writer,
         async_execution=False,
         output_file='new-blog-post.md'
)