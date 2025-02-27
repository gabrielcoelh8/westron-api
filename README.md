## About
Enabling the use of various modern LLMs (ChatGPT, Gemini), the API functions as a small natural language processing model, with its main features:
* Translation of texts to various languages
* Detection of negative sentiments and making texts more positive
* Grammar and spelling correction in various languages

> The project architecture allows future addition of new models, or even the use of fine-tuned or proprietary models.

![Python](https://img.shields.io/badge/Python-3.12-blue)
![fastapi](https://img.shields.io/badge/fastapi-0.115.6-green)

## Documentation
Contains the available routes, examples, auth, Pydantic models, and more.
- [Docs](https://westron-api.onrender.com/docs/)

- [Redoc](https://westron-api.onrender.com/redoc/)

## Supported Languages (ISO 639-1):
* "en"
* "es"
* "fr"
* "de"
* "pt"
* "jp"

## Configuration and Enviroment
Requirements:
* Linux command terminal or [WSL](https://learn.microsoft.com/pt-br/windows/wsl/install)
* [Docker](https://docs.docker.com/get-started/get-docker/)

Project environment variables:
```shell
# DATABASE
POSTGRES_DB_HOSTNAME=
POSTGRES_DB_DATABASE=
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_DB_SCHEMA=
POSTGRES_DB=
POSTGRES_DB_PORT=
PG_DATA=/data/postgres
POSTGRES_DRIVERNAME="postgresql"
# LLM MODELS
OPENAI_API_VERSION="2024-08-01-preview"
GPT_ENDPOINTS="['https://models.github.ai/inference']"
GPT_KEYS="['']"
GPT_MODELS="[['gpt-4o',]]"
GPT_INPUTS="[[4096]]"
GPT_OUTPUTS="[[4096]]"
GEMINI_KEY=""
GEMINI_ENDPOINT="https://generativelanguage.googleapis.com/"
GEMINI_MODEL="gemini-2.0-flash"
# JWT
SECRET_KEY=""
ALGORITHM=""
ACCESS_TOKEN_EXPIRE_MINUTES=10
# CONFIGURATION
PROMPTS_PATH="app/utils/prompts/version-0_0_1.json"
TOKEN_URL="api/v1.0/token"
```
## Docker Build
Execute the following commands to build the project in a Linux terminal or WSL with Docker installed:
```shell
# DATABASE
docker compose up banco-dados --build

# API
docker compose up servico-api --build
```
After building, the API service will be available locally at `http://localhost:8001/`

## Routes Documentation (Swagger)
Access the complete documentation for using the routes from the `/docs` or `/redoc` endpoint.

## Dev Container
Create a *.env.dev* file containing the variables listed in the configuration section.
1. Clone the repository in some directory within WSL
2. Open the project root in [Visual Studio Code](https://code.visualstudio.com/)
3. Install the `Dev Container` extension
4. Press `CTRL` + `SHIFT` + `P` and search for the option `Dev Containers: Open Folder in Container...`
