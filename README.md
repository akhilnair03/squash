# Squash: Smart Food Inventory Management App

## Inspiration
The inspiration for Squash came from the need to streamline and simplify how we track groceries and manage food inventory at home. Often, people struggle to keep track of what they have, leading to unnecessary purchases or food waste. We envisioned a solution that leverages technology—specifically speech and image recognition—to automate the process of adding items to inventory, making grocery management quick, intuitive, and effortless. By combining speech-to-text and OCR (optical character recognition) technologies, we set out to build a tool that would not only help track groceries but also contribute to reducing food waste. We provide users with recipes for any meal of the day to use their groceries and food banks near them to donate if they have a surplus that they won't be able to use.

## What It Does
Squash is a smart food inventory management app designed to make grocery tracking as simple as talking or snapping a picture. Users can add food items to their inventory by either speaking into the app or taking a picture of a grocery receipt. The app uses speech recognition to convert spoken words into text and Optical Character Recognition (OCR) to scan receipts and extract information about the items purchased. Squash then categorizes these items (e.g., breakfast, lunch, dinner) to create recipes. It also stores them in a food inventory list, making it easy to know what you have at home at any given time.

## How We Built It
We built Squash using a combination of modern technologies for both the frontend and backend:

- **Frontend:** We used React Native for the mobile application, leveraging its versatility across both iOS and Android platforms. For the voice input functionality, we integrated Expo's audio recording feature, which allows users to speak into the app. We then used a custom UI to display categorized food items, designed with intuitive navigation for different meal types (breakfast, lunch, dinner).

- **Backend:** The backend is powered by Flask, a Python web framework. We implemented API endpoints to handle both OpenAI Whisper's speech-to-text and OCR processing. For the speech transcription, we convert audio recordings into base64, which is sent to the backend for processing using a machine learning model. The OCR functionality extracts text from receipt images and automatically categorizes the items based on predefined food categories.

We used many of **Gemini's LLMs** to generate responses and insights with our data.
