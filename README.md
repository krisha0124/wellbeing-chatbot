Wellbeing Chatbot

A simple chatbot that conducts wellbeing conversations using Gemini AI and stores data in MongoDB.

Features
- Asks for user name and date of birth
- Conducts wellbeing conversations (sleep, stress, mood, energy)
- 10-message limit
- Automatic sentiment analysis (Positive/Negative)
- MongoDB data storage
- Streamlit web interface

Setup Instructions
Prerequisites
- Python 3.8+
- MongoDB Atlas account (free)
- Google Gemini API key (free)

Installation

1. Create virtual environment
   ```bash
   python -m venv chatbot-env
   source chatbot-env/bin/activate  # Mac
   chatbot-env\Scripts\activate    # Windows

2. Install dependencies
   ```bash
    pip install -r requirements.txt

4. Setup environment variables
   ```bash
    GEMINI_API_KEY=AIzaSyCo_BZiGazsangokwMvkoZdjl2wLueWew
    MONGODB_URI=mongodb+srv://wellbeinguser:gavjod-xamhoq-3reBte@wellbeing-cluster.dpudtqo.mongodb.net/?appName=wellbeing-cluster

6. Run application
   ```bash
    streamlit run app.py


PROJECT STRUCTURE 
```bash

wellbeing-chatbot/
├── app.py 
├── requirements.txt
├── .env
├── flow_diagram.txt
└── README.md
