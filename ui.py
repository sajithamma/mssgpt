import chainlit as cl
from pathlib import Path
from dotenv import load_dotenv
from app.chainlit_extras import set_starters
from app.skills import process_image, process_input
load_dotenv()


@cl.on_chat_start
async def on_chat_start():

    cl.user_session.set(
        "message_history",
        [
            {"role": "system", "content": "You are an expert about MSS"}
        ],
    )

@cl.on_message
async def main_chat(message: cl.Message):

    images = [file for file in message.elements if "image" in file.mime]
    has_image = len(images) > 0


    if images:
        image_path = images[0].path
        response = await process_image(image_path, message.content)
        
        user_prompt=response
        
    else:

        user_prompt=message.content

    await process_input(user_prompt)
        