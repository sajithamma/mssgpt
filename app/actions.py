import chainlit as cl
# Import process_input inside functions to avoid circular dependency
# from app.skills import process_input

def get_contact_details():
    return "You can reach us at:\n  +971 547352524 / +971 508803536 \n📞 info@mssgulf.orgi"

def get_actions():
    """Returns the list of actions to be displayed with messages."""
    # Define starters based on chainlit_extras.py
    starters = [
    {
        "name": "starter_1",
        "icon": "circle-triangle",
        "label": "What does MSS do for the community?",
        "message": "How does Model Service Society (MSS) serve people and create a positive impact across Dubai through its humanitarian programs?"
    },
    {
        "name": "starter_2",
        "icon": "sine",
        "label": "How can I volunteer with MSS?",
        "message": "What is the process to become a volunteer or member of MSS and participate in social and community welfare activities?"
    },
    {
        "name": "starter_3",
        "icon": "taylor",
        "label": "What are MSS’s major programs?",
        "message": "Can you tell me about the main initiatives like the Iftar Program, Blood Donation Camps, Youth Festival, and Empowerment Programs conducted by MSS?"
    },
    {
        "name": "starter_4",
        "icon": "neural",
        "label": "How does MSS empower youth and women?",
        "message": "What kind of leadership, education, and empowerment programs does MSS organize for students and women in the UAE?"
    },
    {
        "name": "starter_5",
        "icon": "circle-triangle",
        "label": "Who leads and supports MSS?",
        "message": "Who are the key leaders behind MSS, and how do they ensure transparency, inclusion, and impact in all community services?"
    }
]



    actions = [
        cl.Action(
            name="contact_us_button",
            icon="mail",
            payload={"value": "contact_us"},
            label="Contact Us!"
        ),
        cl.Action(
            name="new_question_button",
            icon="home",
            payload={"value": "new_question"},
            label="New Question?"
        )
    ]

    # Create actions from starters
    for starter in starters:
        # Clean icon path if necessary (remove /public/)
        icon_name = starter["icon"].replace("/public/", "").replace(".svg", "")
        actions.append(cl.Action(
            name=starter["name"],
            icon=icon_name,
            payload={"value": starter["message"]},
            label=starter["label"]
        ))

    return actions

@cl.action_callback("contact_us_button")
async def on_contact_us(action: cl.Action):
    contact_info = get_contact_details()
    await cl.Message(content=contact_info).send()

@cl.action_callback("new_question_button")
async def on_new_question(action: cl.Action):
    # Redirect to home or send a message to guide the user
    await cl.Message(content="Feel free to ask any question.").send()

# Dynamically create callbacks for starters
async def _starter_callback(action: cl.Action):
    from app.skills import process_input
    await process_input(action.payload["value"])

# Register callbacks for each starter
for i in range(1, 10): # Adjust range based on the number of starters added
    cl.action_callback(f"starter_{i}")(_starter_callback)

# Keep individual callbacks if specific logic is needed later, otherwise remove
# @cl.action_callback("starter_1")
# async def on_starter_1(action: cl.Action):
#     from app.skills import process_input
#     await process_input(action.payload["value"])
#
# @cl.action_callback("starter_2")
# async def on_starter_2(action: cl.Action):
#     from app.skills import process_input
#     await process_input(action.payload["value"])
#
# @cl.action_callback("starter_3")
# async def on_starter_3(action: cl.Action):
#     from app.skills import process_input
#     await process_input(action.payload["value"]) 