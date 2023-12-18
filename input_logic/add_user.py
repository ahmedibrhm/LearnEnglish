from openai import OpenAI
from config import SYSTEM_PROMPT

client = OpenAI()

def create_assistant():
    assistant = client.beta.assistants.create(
        name="English Teacher",
        instructions=SYSTEM_PROMPT,
        model="gpt-3.5-turbo-1106"
    )
    return assistant

def create_thread():
    thread = client.beta.threads.create()
    return thread

def add_user():
    assistant = create_assistant()
    thread = create_thread()
    return assistant.id, thread.id