# Jarvis — Personal Voice Assistant

A voice-controlled personal assistant built in Python that listens for a wake word and executes everyday desktop commands — opening websites and apps, playing music, and doing quick calculations, all through natural spoken commands.

## Overview

Jarvis is an ongoing project built to explore speech recognition, text-to-speech, and system automation in Python. It runs continuously in the background, listening for the wake word "Jarvis," then processes whatever command follows. It's actively being expanded — the current focus is integrating LLM-powered understanding so it can handle more flexible, conversational commands instead of fixed keyword matching.

## Features

- 🎙️ **Voice Recognition** — captures and transcribes spoken commands using Google's speech recognition API
- 🔊 **Text-to-Speech (TTS)** — responds audibly using `pyttsx3`
- 👂 **Wake Word Detection** — stays idle until it hears "Jarvis," then activates and listens for a command
- 🌐 **Web Browsing** — opens YouTube, Google, Facebook, and Instagram on request
- 🚀 **App Launching** — opens Notepad, Calculator, Command Prompt, and Camera
- 🎵 **Music Playback** — asks which song to play and opens it from a predefined song-link mapping
- ➗ **Voice Calculator** — parses spoken math expressions (e.g. "what is 5 plus 3") and evaluates them
- 🛑 **Exit Command** — shuts down cleanly on "exit" or "shutdown"

## Tech Stack

- **Language:** Python
- **Speech Recognition:** `SpeechRecognition` (Google Speech-to-Text API)
- **Text-to-Speech:** `pyttsx3`
- **Web/App Control:** `webbrowser`, `os.startfile`
- **Custom module:** `music.py` — maps song names to playback links

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/jarvis.git
cd jarvis

# Install dependencies
pip install SpeechRecognition pyttsx3 pyaudio

# Run Jarvis
python main.py
```

> **Note:** `pyaudio` is required for microphone access via `SpeechRecognition` and can sometimes need extra setup on Windows — if `pip install pyaudio` fails, install it via `pip install pipwin` then `pipwin install pyaudio`.

## Usage

1. Run the script — Jarvis will greet you on startup
2. Say **"Jarvis"** to activate
3. After it responds, give a command, for example:
   - "Open YouTube"
   - "Open Notepad"
   - "Play a song"
   - "What is 12 plus 8"
   - "Exit" or "Shutdown" to close the assistant

## Roadmap

- [ ] Integrate LLM API for natural language command understanding (move beyond fixed keyword matching)
- [ ] Add tool-calling support for more dynamic, flexible task execution
- [ ] Expand app/site control beyond the current fixed list
- [ ] Improve error handling for calculation parsing (currently uses `eval`, which is functional but not safe for untrusted input)

## Project Status

Actively developed — this is a running project I'm continuously upgrading as I learn more about APIs, LLMs, and agentic AI systems.

## Author

Built by [Abdullah](https://www.linkedin.com/in/abdullah-zahid-dev/) — Software Engineering student, FAST-NUCES.
