from crewai import Crew,Process
from agents import blog_writer,researcher
from tasks import research_task,write_task

# Process with sequantial execution
crew = Crew(
    agents=[researcher,blog_writer],
    tasks=[research_task,write_task],
    process=Process.sequential,
    memory=True,
    cache=True,
    max_rpm=100,
    share_crrew=True
)

#  Start  the task execution
result = crew.kickoff(inputs={"topic": "What is Machine Learning?"})
print(result)