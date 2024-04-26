# DataDialogue

## Objective
The objective of Data Dialogue is to interact with arbitrary data sources using natural languages and to keep all the data local to your server. This includes performing data analysis, data visualization, and calculations. 

## Features
Models - Anthropic, OpenAI, Ollama
Data Sources - CSV, Sqlite

## Installation
This projects uses PDM (https://github.com/pdm-project/pdm) for the backend and npm (https://www.npmjs.com/) for the frontend. You may also want to install Ollama (ollama.com) for hosting open source models on the backend

### Backend

  Copy src/backend/sample.config.toml to src/backend/config.toml and fill in the necessary fields.
  Then
  ```bash
    cd src/backend
    pdm install
    python migrations.py makemigrations
    python migrations.py migrate
    python migrate.py runserver
  ```

### Frontend

  ```bash
    cd src/frontend
    npm install
    npm start
  ```