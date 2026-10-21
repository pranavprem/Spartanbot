# Agent guide

Spartanbot is a Spring 2017 SJSU CMPE 273 greensheet bot. Read this before editing. [CLAUDE.md](CLAUDE.md) points here. The short Cursor rule in `.cursor/rules/project.mdc` does too.

## Architecture

`controller.find_solution` is the only reply policy. Every front door calls it:

- `spartanbot.py` for Slack and the terminal
- `twilio_handle.py` for `POST /twilio` and `GET /alexa_endpoint/<question>`
- `Alexa Skill Lambda/service.py` HTTP-calls that GET route; it does not score questions itself

Order inside `find_solution`, after lowercasing:

1. If the previous reply was the "valid response" prompt (`db_mode_flag`), store this message and answer `I'll remember that`.
2. If the command is exactly `no`, ask for a better answer and set the flag.
3. Small talk. A score at or above 0.65 returns immediately, with no satisfaction question.
4. Commands that start with `do` go to `calculator`.
5. Otherwise the greensheet path prefixes `CUSTOM SOLUTION :: `, leaves Watson NLC empty, appends `Additionally, this might help:`, and appends Google hits only when that call returns items.
6. Unless the reply is the remember acknowledgement or the flag is set, append `Are you satisfied with that response?`

`learn.py` fills the store. `sentence_engine` builds `{keywords, sentence}`. `scorer.analyzer` ranks stored sentences. `db.spartandb` is MongoDB when `MONGODB_URI` is set, otherwise `data/knowledge.json` (override with `SPARTANBOT_LOCAL_DB`).

The remember flag is in memory on one `controller` instance. The Flask process and the Slack worker do not share it. Heroku's old design posted SMS into Slack so the worker owned the flag. Socket Mode does not echo the bot's own messages, so the Flask process now answers SMS itself.

## Conventions

- Keep the flat modules and the original names (`sentence_engine`, `doCustom`, `insertCollection`, `set_color_in_session`). They are the project's vocabulary.
- Python 3.12. Format with Ruff (`line-length` 100, rules E, F, I, W). Config is in `pyproject.toml`.
- Secrets come from the environment. `settings.setting` accepts the 2017 name and a modern alias. `load_dotenv` uses `setdefault`. Tests set `SPARTANBOT_DISABLE_DOTENV=1` in `tests/conftest.py`.
- Do not commit `.env`, `env/`, `nltk_data/`, `data/*.json`, bytecode, or `training-data.csv`.
- Do not add a license file.
- Do not "correct" `cmpe273-greensheet.docx`, `subjects.txt`, or `objects.txt`. That text is the corpus, including odd spellings.
- Watson NLC and Google Custom Search must degrade to an empty result. Do not wire in a replacement classifier or search API.
- New tests go in `tests/` and should not need Slack, Mongo, Google, or Watson. Inject fakes. The greensheet integration test is `tests/test_learn_greensheet.py`.

## Commands

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
python -m nltk.downloader punkt_tab wordnet omw-1.4
ruff check .
ruff format .
pytest
python learn.py
python spartanbot.py --local
PORT=6000 python twilio_handle.py
python "Alexa Skill Lambda/service.py"
```

CI is `.github/workflows/ci.yml`: checkout, Python 3.12, `pip install -r requirements-dev.txt`, NLTK download, `ruff check`, `ruff format --check`, `pytest`.

## Environment

| Name | Used for |
| --- | --- |
| `SLACK_BOT_TOKEN`, `slacktoken` | Slack Web API, RTM, `findbotid.py` |
| `SLACK_APP_TOKEN` | Socket Mode. Preferred over RTM |
| `SLACK_BOT_ID`, `bot_id` | Mention string. Optional |
| `SLACK_BOT_NAME` | Default `testonebot` |
| `SLACK_CHANNEL` | Default `#testonebotchanel` |
| `MONGODB_URI` | MongoDB. Unset means the JSON file |
| `MONGODB_DB` | Database name. Else the URI default, else `heroku_jrt9gnq3` |
| `SPARTANBOT_LOCAL_DB` | JSON path |
| `user_number` | SMS allow-list. Unset rejects the relay with 403 |
| `my_api_key`, `GOOGLE_API_KEY` | Custom Search |
| `my_cse_id`, `GOOGLE_CSE_ID` | Custom Search engine id |
| `bluemix_username`, `WATSON_USERNAME` | Retired NLC |
| `bluemix_password`, `WATSON_PASSWORD` | Retired NLC |
| `WATSON_CLASSIFIER_ID` | Retired NLC. No default id |
| `ALEXA_BACKEND_URL` | Skill backend. Default is the old Heroku URL |
| `PORT` | Flask port. Default 6000 |
| `NLTK_DATA` | Tokenizer and WordNet location |

## Gotchas

- The scorer divides by the longer keyword list and multiplies by 100, then keeps scores at or above `max - (max - min) / 4`. Do not "fix" this to match the old README formula.
- Small talk is one ChatterBot `ListTrainer` chain, not a cleaned FAQ. `Hi` replies `Hello`, and `You are welcome.` replies `Whats your name?`. Threshold is 0.65 via `difflib.SequenceMatcher`.
- WordNet contributes synonyms from the first synset only. PyDictionary's scrapers no longer work; do not bring that package back.
- `learn.py` appends greensheet rows on every run. Keyword inserts are deduped and stripped. The 2017 code appended duplicates and kept leading spaces from `subjects.txt`, which broke substring matches.
- Calculator answers used to be glued to the follow-up (`result is 4Are you satisfied...`). A newline is inserted when the reply does not already end with one. Bad `do` commands return `invalid operation` instead of raising.
- Google and Watson clients must not raise out of `find_solution`. Missing configuration is an empty result, not a startup crash. Importing the app used to require `MONGODB_URI`, `my_api_key`, and `slacktoken` even when those calls were commented out.
- `nlc_module.classify` is intentionally not called by the controller. The 2017 code disabled it. The module remains so a configured, still-failing endpoint stays an empty string.
- Alexa `QuestionIntent` with no `Question` slot used to read unbound locals and crash. It now says it did not catch that. Launch still says `Yo`.
- Slack text is clipped around 3900 characters at the Slack boundary only. Alexa and the REPL get the full string.
- `pymongo` Collection `.save()` was removed in PyMongo 4. Keyword updates use `replace_one`.
- Flask's default port is 6000. Chrome refuses that port (`ERR_UNSAFE_PORT`). Use `PORT=8080` when checking the page in a browser.
- The committed `env/` directory was a Python 2.7 virtualenv used to zip the Alexa lambda. Do not restore it. The skill handler has no third-party imports.
- History on `master` still contains Slack bot tokens and a Bluemix password. Do not copy them back into the tree. Tell the owner to rotate them; rewriting history is a separate force-push they have to choose.

## Tests worth knowing

- `tests/test_scorer.py` locks the longer-list formula and the threshold.
- `tests/test_degraded_apis.py` locks empty Google and Watson results.
- `tests/test_learn_greensheet.py` loads the real docx and expects `sithu` in the instructor answer.
- `tests/test_slack_and_web.py` covers mention parsing, Socket Mode ack, the SMS allow-list, and the Alexa small-talk route.
- MongoDB is not started in CI. `MongoBackend` is exercised with an in-memory fake that requires `replace_one`.
