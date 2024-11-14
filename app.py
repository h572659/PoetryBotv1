import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(dotenv_path=".env")
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

import gradio as gr

def chat(message, history, mood):
    # We don't need "history" since the bot does not need to remember anything.
    # But it is required by gradio

    # The illusion of choice. 10 to chose from, but only 3 actual outputs, lol
    if (mood < 4.0):
        currentMood = "Bad"
    elif (mood > 7.0):
        currentMood = "Good"
    else:
        currentMood = "Neutral"
    

    response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a poet bound to never write anything longer than 280 characters, you will write a poem based on what the user provides you and the desired mood"},
        {
            "role": "user",
            "content": message + "Desired mood: " + currentMood
        }
    ],
    temperature=1,
    stream=True
    )
    
    #Makes the output to the user look a little nicer
    parMessage = ""
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            parMessage = parMessage + chunk.choices[0].delta.content
            yield parMessage

demo = gr.ChatInterface(
    fn=chat,
    type="messages",
    textbox=gr.Textbox(placeholder="I will write a tweet for you based on your mood, the mood slider bellow goes from 1 (bad mood) to 10 (good mood)", container=False, scale=7),
    additional_inputs= [gr.Slider(1,10)]
)

demo.launch()