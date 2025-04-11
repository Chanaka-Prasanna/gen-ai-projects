from crewai_tools import YoutubeVideoSearchTool

youtube_tool = YoutubeVideoSearchTool(
    config=dict(
        llm=dict(
            provider="google",  # Specify that you're using Google
            config=dict(
                model="gemini/gemini-2.0-pro-exp-02-05",
            ),
        ),
        embedder=dict(
            provider="google",  # Use the same for embedder
            config=dict(
                model="models/embedding-001",
                task_type="retrieval_document",
            ),
        ),
    )
)
