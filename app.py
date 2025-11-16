import streamlit as st
import datetime
import os
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Load environment variables
load_dotenv()

# MongoDB connection
def connect_mongodb():
    uri = os.getenv('MONGODB_URI')
    try:
        client = MongoClient(uri, server_api=ServerApi('1'))
        client.admin.command('ping')
        return client
    except:
        return None

def save_to_mongodb(user_data, messages, sentiment):
    client = connect_mongodb()
    if not client:
        return False
    
    try:
        db = client.wellbeing_chatbot
        collection = db.chats
        
        chat_record = {
            "user_name": user_data["name"],
            "date_of_birth": user_data["dob"],
            "chat_history": messages,
            "final_sentiment": sentiment,
            "timestamp": datetime.datetime.now().isoformat(),
            "tools_used": []
        }
        
        collection.insert_one(chat_record)
        client.close()
        return True
    except:
        return False

# Simple wellbeing questions
wellbeing_questions = [
    "How have you been feeling lately?",
    "How has your sleep been?",
    "On a scale of 1-10, how would you rate your stress levels?",
    "What's been bringing you joy recently?",
    "How are your energy levels throughout the day?",
    "Have you been able to relax and take time for yourself?",
    "How are things going with friends and family?",
    "What's one positive thing that happened this week?",
    "How do you usually cope when you feel stressed?",
    "Is there anything you'd like to share about your overall wellbeing?"
]

def analyze_sentiment_simple(messages):
    # Simple keyword-based sentiment analysis
    user_text = " ".join([msg['text'].lower() for msg in messages if msg['role'] == 'user'])
    
    positive_words = ['good', 'great', 'happy', 'well', 'fine', 'better', 'okay', 'excited', 'nice', 'love']
    negative_words = ['sad', 'stress', 'stressed', 'tired', 'bad', 'worried', 'anxious', 'hard', 'difficult', 'struggle']
    
    positive_count = sum(1 for word in positive_words if word in user_text)
    negative_count = sum(1 for word in negative_words if word in user_text)
    
    if positive_count > negative_count:
        return "Positive"
    elif negative_count > positive_count:
        return "Negative"
    else:
        return "Positive"  # Default to positive

# Main app
def main():
    st.title("Wellbeing Chatbot")
    
    # Initialize session state
    if 'step' not in st.session_state:
        st.session_state.step = 1  # 1: user info, 2: chat, 3: end
    if 'user_info' not in st.session_state:
        st.session_state.user_info = {}
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
    
    # Step 1: Get user information
    if st.session_state.step == 1:
        st.subheader("Before we begin:")
        
        name = st.text_input("What is your name?")
        dob = st.date_input("What is your date of birth?", datetime.date(2000, 1, 1))
        
        if st.button("Start Chat") and name:
            st.session_state.user_info = {"name": name, "dob": str(dob)}
            st.session_state.step = 2
            # Start with first question
            st.session_state.messages.append({
                "role": "assistant", 
                "text": f"Hello {name}! " + wellbeing_questions[0],
                "timestamp": datetime.datetime.now().isoformat()
            })
            st.session_state.current_question = 1
            st.rerun()
    
    # Step 2: Chat interface
    elif st.session_state.step == 2:
        st.subheader(f"Chat with {st.session_state.user_info['name']}")
        
        # Calculate remaining messages correctly
        total_messages = len(st.session_state.messages)
        remaining_messages = 10 - total_messages
        
        # Show progress
        st.write(f"Progress: {total_messages}/10 messages")
        
        # Display chat history
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                st.write(f"You: {msg['text']}")
            else:
                st.write(f"Bot: {msg['text']}")
        
        # Continue chat if under 10 messages
        if total_messages < 10 and st.session_state.current_question < len(wellbeing_questions):
            user_input = st.text_input("Your response:")
            
            if st.button("Send") and user_input:
                # Add user message
                st.session_state.messages.append({
                    "role": "user",
                    "text": user_input,
                    "timestamp": datetime.datetime.now().isoformat()
                })
                
                # Add next bot question if available
                if st.session_state.current_question < len(wellbeing_questions):
                    st.session_state.messages.append({
                        "role": "assistant",
                        "text": wellbeing_questions[st.session_state.current_question],
                        "timestamp": datetime.datetime.now().isoformat()
                    })
                    st.session_state.current_question += 1
                
                st.rerun()
        
        # End chat conditions
        end_chat = False
        
        # Condition 1: Reach 10 messages
        if len(st.session_state.messages) >= 10:
            end_chat = True
        
        # Condition 2: Manual end button
        if st.button("End Chat Now"):
            end_chat = True
        
        if end_chat:
            st.session_state.step = 3
            st.rerun()
    
    # Step 3: Show results
    elif st.session_state.step == 3:
        st.subheader("Chat Results")
        
        # Analyze sentiment
        sentiment = analyze_sentiment_simple(st.session_state.messages)
        
        st.write(f" Final Assessment: {sentiment}")
        
        if sentiment == "Positive":
            st.success("You seem to have a positive outlook overall!")
        else:
            st.info("Thank you for sharing. Remember it's okay to ask for support.")
        
        # Save to MongoDB
        if save_to_mongodb(st.session_state.user_info, st.session_state.messages, sentiment):
            st.write("Chat saved to database")
        else:
            st.write("Could not save to database")
        
        # Show chat summary
        st.write("Conversation Summary:")
        for i, msg in enumerate(st.session_state.messages):
            if msg["role"] == "user":
                st.write(f"You: {msg['text']}")
            else:
                st.write(f"Bot: {msg['text']}")
        
        # Option to start new chat
        if st.button("Start New Chat"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

if __name__ == "__main__":
    main()