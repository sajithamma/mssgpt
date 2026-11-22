import chainlit as cl

@cl.set_starters
async def set_starters():
    return [
    cl.Starter(
        label="What does MSS do for the community?",
        message="How does Model Service Society (MSS) serve people and create a positive impact across Dubai through its humanitarian programs?",
        icon="/public/circle-triangle.svg",
    ),
    cl.Starter(
        label="How can I volunteer with MSS?",
        message="What is the process to become a volunteer or member of MSS and participate in social and community welfare activities?",
        icon="/public/sine.svg",
    ),
    cl.Starter(
        label="What are MSS’s major programs?",
        message="Can you tell me about the main initiatives like the Iftar Program, Blood Donation Camps, Youth Festival, and Empowerment Programs conducted by MSS?",
        icon="/public/taylor.svg",
    ),
    cl.Starter(
        label="How does MSS empower youth and women?",
        message="What kind of leadership, education, and empowerment programs does MSS organize for students and women in the UAE?",
        icon="/public/neural.svg",
    ),
    cl.Starter(
        label="Who leads and supports MSS?",
        message="Who are the key leaders behind MSS, and how do they ensure transparency, inclusion, and impact in all community services?",
        icon="/public/circle-triangle.svg",
    ),
]


