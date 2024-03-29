import json
import pytest
from langchain_community.llms.fake import FakeListLLM
from summarizer.templates import make_time_chain


transcript_json = [
    {"start": "00:00:01", "text": "Hello world."},
    {"start": "00:00:05", "text": "This is a test."},
    {"start": "00:00:10", "text": "Another sentence."},
]

similar_turns = [
    {"id": 0, "topic": "Intro", "similarity": "extremely similar"},
    {"id": 1, "topic": "Intro Continued", "similarity": "extremely similar"},
    {"id": 2, "topic": "Main Content", "similarity": "not similar"},
    {"id": 3, "topic": "Main Content Continued", "similarity": "very similar"},
    {"id": 4, "topic": "Conclusion", "similarity": "not similar"},
]

simple_turns = [
    {"id": 0, "topic": "Intro", "similarity": "not similar"},
    {"id": 1, "topic": "Main Content", "similarity": "not similar"},
    {"id": 2, "topic": "Conclusion", "similarity": "not similar"},
]

simple_transcript = [
    {
        "title": "Introduction",
        "summary": "Hello world.",
        "insights": [{"sourceIds": [0], "markdown": "Hello world."}],
    }
]


@pytest.fixture
def mock_model():
    return FakeListLLM(
        responses=[
            json.dumps({"topics": simple_turns}),
            json.dumps({"articles": simple_transcript}),
            json.dumps({"articles": simple_transcript}),
        ]
    )


def test_make_time_chain(mock_model):
    # Create the time chain
    time_chain = make_time_chain(transcript_json)

    # Assert that the result matches the expected output
    assert time_chain(mock_model) == simple_transcript + simple_transcript
