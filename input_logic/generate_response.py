from openai import OpenAI
import time

client = OpenAI()

def get_openai_response(message, assistant_id, thread_id):

    my_thread_message = client.beta.threads.messages.create(
    thread_id=thread_id,
    role="user",
    content=message,
    )

    # Step 4: Run the Assistant
    my_run = client.beta.threads.runs.create(
    thread_id=thread_id,
    assistant_id=assistant_id,
    )

    # Step 5: Periodically retrieve the Run to check on its status to see if it has moved to completed
    while my_run.status != "completed":
        keep_retrieving_run = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=my_run.id
        )
        if keep_retrieving_run.status == "completed":
            print("\n")
            break
        time.sleep(0.5)

    # Step 6: Retrieve the Messages added by the Assistant to the Thread
    all_messages = client.beta.threads.messages.list(
    thread_id=thread_id
    )
    return all_messages.data[0].content[0].text.value
    