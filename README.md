# Number Guessing Game

A beginner-friendly Python Flask web game with Easy, Medium and Hard difficulty levels.

## Run locally

```bash
pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:5000`.

## Deploy on Render

Create a Render Web Service from this GitHub repository.

Build Command:
```text
pip install -r requirements.txt
```

Start Command:
```text
gunicorn app:app
```
