import chainlit as cl
from pathlib import Path
import base64
from openai import OpenAI
import os
from dotenv import load_dotenv
import json

# Import actions and callbacks
# Note: Individual starter callbacks are dynamically registered in actions.py
from app.actions import get_actions, get_contact_details, on_contact_us, on_new_question

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

# Load system instructions
with open("system_instructions.txt", "r") as f:
    system_instructions = f.read()

async def process_input(user_prompt: str) -> str:
    """
    Processes the user's input and returns the AI's response.
    """
    # Increment chat count in session
    chat_count = cl.user_session.get("chat_count", 0)
    chat_count += 1
    cl.user_session.set("chat_count", chat_count)

    message_history = cl.user_session.get("message_history", [])
    message_history.append({"role": "user", "content": user_prompt})

    # First response to get tool call if needed
    response = client.responses.create(
        model="gpt-4o",
        input=message_history,        
        stream=True,
        instructions=system_instructions
    )

    msg = cl.Message(content="")
    tool_calls = []
    final_response = ""

    for event in response:
        if event.type == 'response.output_text.delta':
            await msg.stream_token(event.delta)
            final_response += event.delta

    await msg.send()

    # Update message history
    message_history.append({"role": "assistant", "content": final_response})
    cl.user_session.set("message_history", message_history)

    # Ask for email only if chat_count == 3 and not already asked
    if chat_count == 20 and not cl.user_session.get("email_asked", False):
        cl.user_session.set("email_asked", True)
        res = await cl.AskUserMessage(content="What is your email?", timeout=120).send()
        if res:
            from app.db import save_email
            email = res['output']
            save_email(email)
            await cl.Message(content=f"Thank you for your email. We will get back to you soon.").send()
            actions = get_actions()
            await cl.Message(content="Need to get in touch or explore more?", actions=actions).send()

    else:
        # Sending action buttons within a chatbot message (not when asking email)
        actions = get_actions()
        await cl.Message(content="Need to get in touch or explore more?", actions=actions).send()

async def process_image(image_path: str, question: str) -> str:
    """
    Processes an image by encoding it to base64 and sending it to OpenAI along with a question.
    Returns the AI's response text.
    """

    msg = cl.Message(content="**Processing Image...**")
    await msg.send()
    
    with open(image_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode('utf-8')
    stream = client.chat.completions.create(
        model="gpt-4o",
        stream=True,
        messages=[
            {
                "role": "system",
                "content": 
                        """Read the mathematics question explained in the image.
                        """
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": question},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                ],
            }
        ],
    )
    final_response = ""

    async with cl.Step(name="Generating code mathcing image...", default_open=True) as image_ai_step:
        
        image_ai_step.input = question
        image_ai_step.output = ""

        for part in stream:

            content_part = part.choices[0].delta.content
            
            if content_part: 
                
                await image_ai_step.stream_token(content_part)
                
                final_response += content_part

    return final_response