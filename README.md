# ChatGPT Clone

A ChatGPT web UI clone built with **Flask**, **Tailwind CSS**, and **MongoDB**, wired to the OpenAI API.

It recreates the classic ChatGPT layout - the sidebar with chat history, the
Examples / Capabilities / Limitations landing screen, and the two-tone message
thread - and caches every question and answer in MongoDB, so a repeated question
is served from the database instead of hitting the API again.

## Screenshots

### Landing screen
![Landing screen](screenshots/home.png)

### Chat view
![Chat view](screenshots/chat.png)

> The answer above reads "No OPENAI_API_KEY set" because the app was started
> without a key, in UI-only mode. With a key configured, the model's reply
> renders in that spot.

## Features

- ChatGPT-style dark UI, built with Tailwind
- Ask a question and get an answer from the OpenAI API
- Answers cached in MongoDB - a repeated question is served from the DB, no API call
- Past questions listed in the sidebar
- Runs without MongoDB or an API key, so the UI can be developed on its own

## Tech stack

| Layer    | Tool                          |
|----------|-------------------------------|
| Backend  | Flask                         |
| Frontend | Tailwind CSS, vanilla JS      |
| Database | MongoDB (via Flask-PyMongo)   |
| AI       | OpenAI Chat Completions API   |

## Getting started

### 1. Clone and install

```bash
git clone https://github.com/DharamVeer970/Chatgpt-Clone.git
cd Chatgpt-Clone

pip install -r requirements.txt
npm install
```

### 2. Configure

Copy the example file and fill in what you have:

```bash
cp .env.example .env
```

Nothing in it is required - any value you leave blank simply disables that
feature, and the app still runs.

| Variable         | Required | Blank means                          |
|------------------|----------|--------------------------------------|
| `OPENAI_API_KEY` | No       | UI-only mode, no real answers        |
| `MONGO_URI`      | No       | No chat history, no answer caching   |
| `OPENAI_MODEL`   | No       | Defaults to `gpt-4o-mini`            |

A filled-in `.env` looks like this:

```ini
OPENAI_API_KEY=sk-...
MONGO_URI=mongodb+srv://<user>:<password>@<cluster>/Chatgpt
OPENAI_MODEL=gpt-4o-mini
```

Real environment variables also work and take precedence over `.env`, which is
handy in production.

> **Never commit your API key or connection string.** `.env` is already in
> `.gitignore` - keep your real values there, and only ever commit
> `.env.example`.

### 3. Run

```bash
python main.py
```

Open <http://127.0.0.1:5000>.

To rebuild the CSS after editing Tailwind classes, run this in a second terminal:

```bash
npm run tailwind
```

## UI-only mode

With no `OPENAI_API_KEY` and no `MONGO_URI`, the app still starts and the whole
interface works - the landing screen renders, the send button switches to the
chat view, and the reply bubble fills with a placeholder instead of a model
answer. This is how the screenshots above were taken, and it's the easiest way
to work on the front end without spending API credits.

## Project structure

```
Chatgpt-Clone/
|-- main.py                 # Flask app: routes, OpenAI call, MongoDB cache
|-- templates/
|   `-- index.html          # Landing screen + chat view
|-- static/
|   |-- js/script.js        # Send button -> POST /api -> render answer
|   |-- input.css           # Tailwind source
|   `-- css/main.css        # Compiled Tailwind output
|-- requirements.txt
`-- package.json            # Tailwind build
```

## How it works

1. `GET /` renders `index.html`, passing in past chats from MongoDB for the sidebar.
2. Clicking send fires `POST /api` with `{"question": "..."}` from `script.js`.
3. The server checks MongoDB for that exact question. On a hit, it returns the
   stored answer immediately.
4. On a miss, it calls the OpenAI Chat Completions API, stores the answer, and
   returns it.
5. The browser swaps the landing panel for the chat panel and renders the answer.

## License

ISC
