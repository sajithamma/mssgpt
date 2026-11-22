# MSS GPT

An AI chat assistant for **Model Service Society (MSS)**. Visitors ask questions about MSS, its programmes and events (for example the Youth Festival) and get answers in a chat window, powered by OpenAI.

It was built in 2025 for the **MSS Youth Fest 2025** and is now handed over to the MSS team to run, update and improve.

> **Before you use it for a new event, read [Updating the content](#updating-the-content-important).** The bot only knows what is written in `system_instructions.txt`, and that file still describes the 2025 events.

---

## How it works

```
Visitor types a question (or uploads an image)
        │
        ▼
ui.py  (Chainlit chat app)
        │  image? → app/skills.py: process_image()  → OpenAI reads the image as text
        ▼
app/skills.py: process_input()
        │  sends the conversation + system_instructions.txt to OpenAI (gpt-4o)
        ▼
Answer streams back into the chat, followed by quick-action buttons
```

There is no database of events, no search and no tools. **All the knowledge the bot has comes from one text file: `system_instructions.txt`.** It is sent to the model as its instructions on every message.

## Project structure

| Path | What it is |
|---|---|
| `ui.py` | Entry point. Starts a chat session and routes each message. |
| `system_instructions.txt` | **The bot's entire knowledge.** MSS background, event details, categories, rules, schedules, all as text and JSON. |
| `app/skills.py` | Calls OpenAI: `process_input()` for chat, `process_image()` for uploaded images. Also asks for the visitor's email after 20 messages. |
| `app/actions.py` | The buttons under each answer (Contact Us, New Question, suggested questions) and the contact details. |
| `app/chainlit_extras.py` | Suggested starter questions shown on the welcome screen. |
| `app/db.py` | Saves visitor emails to a local SQLite file (`zappo.db`). |
| `chainlit.md` | Text of the welcome / readme panel in the chat UI. |
| `.chainlit/config.toml` | Chainlit settings: app name, theme, file upload limits, custom CSS/JS. |
| `public/` | Logos, backgrounds, icons, `custom.css`, `custom.js`, `theme.json`. |
| `.env.example` | Template for the environment variables (only the OpenAI key). |

## Running it locally

Needs Python 3.10 or newer and an OpenAI API key.

```bash
git clone git@github.com:sajithamma/mssgpt.git
cd mssgpt

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
# edit .env and put your real key: OPENAI_API_KEY=sk-...

chainlit run ui.py --port 8000
```

Open http://localhost:8000.

- Never commit `.env`. It is already in `.gitignore`.
- Add `-w` (`chainlit run ui.py -w`) to auto-reload while editing.
- For hosting, any service that runs a Python web process works (Railway, Render, a VM). Set `OPENAI_API_KEY` as an environment variable there, and run `chainlit run ui.py --host 0.0.0.0 --port $PORT --headless`.

## Updating the content (important)

`system_instructions.txt` is **all we set**. Everything the bot says about MSS comes from this file.

**It currently contains last year's material:** the MSS Youth Fest 2025 brochure (2 December 2025, New Dawn Private School, Dubai), its categories, competitions, rules and timings, the Interschool Quiz and Science Exhibition, and other older programme details.

If you use this bot for this year's festival or for any other programme, you **must update this file first**. Otherwise it will confidently give visitors old dates, venues and rules.

How to update it:

1. Open `system_instructions.txt`.
2. Keep the first lines (who the assistant is and how it should behave), edit them if needed.
3. Replace the old event JSON / text with the new brochure, schedule, rules, links and contacts. Plain text or JSON both work; clear headings help the model.
4. Remove anything that no longer applies. Old information left in the file will be used.
5. Restart the app and test it with real questions ("When is the event?", "Where is it?", "What are the categories for juniors?").

Also check these when an event changes:

- Contact details in `app/actions.py` (`get_contact_details`). Note: the email there currently has a typo, `info@mssgulf.orgi`.
- Suggested questions in `app/chainlit_extras.py` and `app/actions.py`.
- Welcome text in `chainlit.md` and the banner/images in `public/`.

## Known rough edges

This is about one year old code, written quickly for one event. Things worth knowing:

- The image upload prompt in `app/skills.py` still says "Read the mathematics question explained in the image" (left over from an earlier project). Change it to fit MSS, or turn image upload off in `.chainlit/config.toml`.
- The whole instructions file (about 1,600 lines) is sent with every message, which costs tokens and does not scale to many events.
- Visitor emails go to a local SQLite file, which is lost when a hosted server restarts.
- `public/` contains some unused images from older projects.
- The model is hard-coded as `gpt-4o` in `app/skills.py`. Newer, cheaper and better models are available.

## Ideas for improving it

The code is small and simple, so it is a good candidate to **rebuild or extend with an AI coding assistant ("vibe coding")** such as Claude Code, Cursor or similar. Some directions:

- **Load the knowledge dynamically.** Move events, programmes, schedules and FAQs into a database or a CMS / Google Sheet the team already edits, and load only the relevant parts per question (search or RAG). Then nobody has to edit a text file for a new event.
- **Make it agentic with tool functions.** Give the model tools it can call, for example: look up an event schedule, check registration status, find a participant's chest number, fetch the latest announcements, register interest, send a confirmation email or WhatsApp message.
- **Multiple programmes.** Youth Festival, Iftar, blood donation camps and others, each with its own data, selected automatically from the question.
- **Admin panel** for the team to update content, see common questions and export collected emails.
- **Proper storage** (Postgres or similar) for emails and chat logs, plus analytics on what people ask.
- **Languages.** Malayalam, Arabic and Hindi answers for the community.
- **Upgrade dependencies** (Chainlit, OpenAI SDK) and the model.

## Credits

Built by Sajith Amma for Model Service Society, 2025. Handed over to the MSS team in November 2026.
