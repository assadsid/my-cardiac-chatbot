import streamlit as st
import google.generativeai as genai
from streamlit_chat import message
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Fetch the API key from the environment variable
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# Check if the API key is properly loaded
if GOOGLE_API_KEY is None:
    st.error("API Key is not set in the environment variables.")
else:
    genai.configure(api_key=GOOGLE_API_KEY)

# Initialize the Generative Model
model = genai.GenerativeModel(
    'gemini-1.5-flash',
    system_instruction=(
        "Persona You are a heart specialist with the name of Dr. Siddiqui. Only provide information related to heart health, symptoms, and advice."
        "Ask users about their heart-related symptoms and provide consultation and guidance based on their input. "
        "Always provide brief answers, additionaly the inquiry is not related to heart health, politely say that you can only provide heart-related information."
        "Responses will be in Urdu (written in English) and English as well."
        "If a user asks for an appointment or a consultation, you can respond with 'You can book an appointment by filling out the form below' and the form will be displayed."
    )
)

# Function to get response from the chatbot
def get_chatbot_response(user_input):
    response = model.generate_content(user_input)
    return response.text.strip()

# Set Streamlit page configuration
st.set_page_config(
    page_title="Heart Health Chatbot",
    page_icon="👨‍⚕",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Add background image
st.markdown("""
    <style>
        .stApp {
            background-image: url('https://cdn.wallpapersafari.com/29/34/8Ak1Sf.png');
            background-size: cover;
            background-position: tile;
            background-attachment: fixed;
        }
    </style>
""", unsafe_allow_html=True)

# Load and display a custom header image (optional)
def load_header():
    header_html = """
    <div style="padding:10px;border-radius:10px;text-align:center;">
        <h1 style="color:white;margin:0;">Heart Health Chatbot 🫀</h1>
        <p style="color:white;margin:0;">Ask me anything about heart diseases!</p>
    </div>
    """
    st.markdown(header_html, unsafe_allow_html=True)

# Initialize session state for chat history and form visibility
if "history" not in st.session_state:
    st.session_state.history = []
if "show_form" not in st.session_state:
    st.session_state.show_form = False

user_avatar_url = "https://img.freepik.com/free-photo/sad-cartoon-anatomical-heart_23-2149767987.jpg?t=st=1725263300~exp=1725266900~hmac=3763e175a896a554720d54c6d774dc645dd73078c952913accec719977d50b48&w=740"
bot_avatar_url = "https://img.freepik.com/premium-photo/3d-render-man-doctor-avatar-round-sticker-with-cartoon-character-face-user-id-thumbnail-modern-69_1181551-3160.jpg?w=740"

# Function to display chat messages
def display_chat_history():
    for chat in st.session_state.history:
        if chat["role"] == "user":
            st.markdown(f"""
                <div style="display: flex; justify-content: flex-end; align-items: center; margin-bottom: 10px;">
                    <div style="display: flex; align-items: center;">
                        <div style="background-color: #075e54; color: white; padding: 10px; border-radius: 10px; max-width: 70%; ">
                            <p style="margin: 0;"><b>You:</b> {chat['content']}</p>
                        </div>
                        <img src="{user_avatar_url}" style="width: 50px; height: 50px; border-radius: 50%; margin-left: 10px;"/>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div style="display: flex; align-items: center; margin-bottom: 10px;">
                    <img src="{bot_avatar_url}" style="width: 50px; height: 50px; border-radius: 50%; margin-right: 10px;">
                    <div style="background-color: #128c7E; color: white; padding: 10px; border-radius: 10px; max-width: 70%;">
                        <p style="margin: 0;"><b>Bot:</b> {chat['content']}</p>
                    </div>
                </div>
            """, unsafe_allow_html=True)

# Function to handle the appointment form
def handle_appointment_form():
    if st.session_state.show_form:
        with st.form(key="appointment_form"):
            st.write("### Appointment Form")
            name = st.text_input("Name")
            contact = st.text_input("Contact Number")
            email = st.text_input("Email Address")
            doctor = st.selectbox("Choose a Doctor", ["Dr. Arshad Ali (Sr. Cardiologist)", "Dr. Gul Zavier (Surgeon)", "Dr. Zarrish Fatima (Physician)", "Dr. Zaiyaan-ul-Haq (Doctor Medicine)"])
            time = st.selectbox("Preferred Appointment Time", ["09:00am", "12:00pm", "03:00pm", "06:00pm"])
            confirm = st.checkbox("Confirm Appointment")

            # Submit button
            submit_button = st.form_submit_button(label="Submit")

            # Handling form submission and displaying the confirmation message
            if submit_button:
                if confirm:
                    st.success(f"Your booking has been confirmed!\n\n**Name:** {name}\n\n**Contact:** {contact}\n\n**Email:** {email}\n\n**Doctor:** {doctor}\n\n**Preferred Time:** {time}")
                else:
                    st.error("Please confirm your appointment.")

# Main application layout
def main():
    load_header()
    st.write("")  # Add spacing

    with st.container():
        display_chat_history()

        # User input area
        with st.form(key="user_input_form", clear_on_submit=True):
            user_input = st.text_input(
                label="",
                placeholder="Type your message here...",
                max_chars=500
            )
            submit_button = st.form_submit_button(label="Send")

            if submit_button and user_input.strip():
                with st.spinner("Thinking..."):
                    bot_response = get_chatbot_response(user_input)
                
                # Update chat history
                st.session_state.history.append({"role": "user", "content": user_input})
                st.session_state.history.append({"role": "bot", "content": bot_response})
                
                # Display the user question and bot response
                st.write(f"""
                <div style="color: yellow">
                        <p>Q: {user_input}</p>
                    </div>
                """, unsafe_allow_html=True)
                st.write(f"""
                <div style="color: white">
                        <p>{bot_response}</p>
                    </div>
                """, unsafe_allow_html=True)
                
                # If the user asks for an appointment, set flag to show form
                if "appointment" in user_input.lower():
                    st.session_state.show_form = True

    # Handle the appointment form outside the user input form
    handle_appointment_form()

# Footer with provided link
st.markdown("""
    <p style="text-align:center; color:white; margin-top:50px;">
        Check out the <a href="https://live-appointment-chatbot20.zapier.app/" target="_blank" style="color:#34c759;">Live Appointment</a>.
    </p>
""", unsafe_allow_html=True)

# Run the app
if __name__ == "__main__":
    main()
