from openai import OpenAI

client = OpenAI()

def get_openai_response(messages):

    # Append the new user message to the messages list
    
    # Get the response from OpenAI
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=1,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    
    # Extract the model's message from the response

    model_message = response.choices[0].message.content

    return model_message

    