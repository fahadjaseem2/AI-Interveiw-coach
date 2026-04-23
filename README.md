# 🎤 AI Interview Coach

An AI-powered interview assistant that listens to voice questions, converts speech into text using Whisper, generates interview answers using Gemma via Ollama, and displays responses in a professional Streamlit UI.

Inspired by platforms like entity["company","Parakeet AI","AI interview assistant platform"].

---

## Features

* 🎙 Real-time voice recording
* ⛔ Manual start/stop recording
* 📝 Speech-to-text using entity["software","Whisper","speech recognition model"]
* 🤖 AI-generated interview answers using entity["software","Gemma","LLM model"] via entity["software","Ollama","local LLM runtime"]
* 🌐 Professional frontend using entity["software","Streamlit","Python web framework"]
* Faster transcription optimization

---

## Tech Stack

* Python
* Streamlit
* Faster Whisper
* Gemma
* Ollama
* NumPy
* SciPy

---

## Project Architecture

```text
User Voice Input
      ↓
Speech Recording
      ↓
Whisper Transcription
      ↓
Gemma (via Ollama)
      ↓
AI Response
      ↓
Streamlit UI
```

---

## Project Structure

```bash
ai-interview-coach/
│
├── app.py
├── ui.py
├── speech_to_text.py
├── llm_response.py
├── requirements.txt
├── README.md
└── screenshots/
```

---

## Installation

Clone repository:

```bash
git clone https://github.com/your-username/ai-interview-coach.git
cd ai-interview-coach
```

Create virtual environment:

```bash
python -m venv ai-venv
source ai-venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Install Ollama model:

```bash
ollama pull gemma4
```

---

## Run Project

Run terminal version:

```bash
python app.py
```

Run frontend version:

```bash
streamlit run ui.py
```

---

## Future Improvements

* Zoom/Google Meet audio capture
* Real-time transcription
* Floating overlay answers
* Resume upload feature
* Interview analytics dashboard

---

## Sample Use Case

User asks:

> Explain Docker networking

AI response:

* Bridge network
* Host network
* Overlay network
* Practical use cases

---

## GitHub Topics

python ai whisper ollama gemma streamlit speech-to-text interview-preparation

---

## Author

Fahad Jaseem

#90DaysOfDevOps #DevOpsKaJosh #TrainWithShubham
