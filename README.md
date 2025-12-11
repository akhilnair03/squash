# 🥫 Squash – Smart Food Inventory & Waste Reduction App

Squash is a smart food inventory and waste reduction app designed to help users efficiently manage groceries through voice and receipt inputs. It uses Whisper for speech-to-text, OCR for receipt parsing, and Gemini LLM to contextualize, categorize, and generate recipes — all to help "squash" food waste.

---

## 🌟 Features

- 🎙️ **Voice Logging**: Speak your grocery items — transcribed using OpenAI Whisper
- 🧾 **Receipt Scanning**: Upload photos of receipts and extract food data using OCR
- 🧠 **Gemini Integration**:
  - Categorizes items (e.g., pantry vs fridge)
  - Suggests recipes with soon-to-expire ingredients
  - Links to nearby food banks
- 📦 **MongoDB Atlas**: Persistent backend storage for food inventory
- 📱 **Mobile-ready**: Designed for React Native + Flask backend integration

---

## 🏗️ Architecture

```
[User] --> [Speech Input or Receipt Upload]
        --> [Whisper / OCR.space]
        --> [Gemini LLM] --> [MongoDB Atlas]
                        --> [Recipe Suggestions]
                        --> [Food Bank Suggestions]
```

### Backend Stack

- Flask API (`__init__.py`)
- MongoDB Atlas connection (`mongo.py`)
- OCR via OCR.space
- Whisper STT and Gemini LLM (`STT.py`)
- Recipe & food bank suggestion logic (`gemini_apis.py`)

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/your-username/squash.git
cd squash
```

### 2. Setup Python Environment

```bash
pip install -r requirements.txt
```

Or, if you're using `pyproject.toml`:

```bash
pip install .
```

### 3. Configure API Keys

Create a `.env` file with your credentials:

```env
GEMINI_API_KEY=your-google-api-key
OCR_API_KEY=your-ocr-space-key
DB_PASSWORD=your-mongodb-password
```

### 4. Run Locally

```bash
python STT.py         # For audio processing
python mongo.py       # For database testing
flask run             # To launch Flask API
```

---

## 🧪 Example Use Cases

1. Say: _"I bought two cartons of eggs and a bottle of milk."_ → Whisper transcribes → Gemini categorizes + stores in DB
2. Upload: _Grocery store receipt image_ → OCR extracts items → Gemini parses + stores
3. Ask for recipes → Gemini returns 3 dishes based on what’s expiring soon

---

## 📌 Future Work

- Add user authentication
- Weekly waste report and donation history
- Push notifications for expiring items
- Recipe filtering by dietary restrictions

---

## 🧑‍💻 Built With

- MongoDB Atlas
- Flask
- React Native (Frontend)
- Google Gemini LLM
- OCR.space
- Whisper ASR

---

**Created by**: Aarya Kulshrestha and team  
**University of Michigan – 2025**
