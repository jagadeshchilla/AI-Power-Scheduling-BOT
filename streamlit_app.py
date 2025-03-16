"""
AI Interview Scheduler Streamlit Application

This module provides a web interface for scheduling interviews using AI assistance.
It integrates with Google Calendar for sending meeting invites and uses a custom
scheduling bot for natural language processing and scheduling logic.
"""

import streamlit as st
import time
from datetime import datetime, timedelta
import pytz
import re
from scheduling_bot import SchedulingBot
from calendar_utils import CalendarManager
from utils import generate_meet_link

# Configure the page - this must be the first Streamlit command
st.set_page_config(
    page_title="AI Interview Scheduler",
    page_icon="📅",
    layout="centered"
)

# Custom CSS for chat styling
st.markdown("""
<style>
    /* Global styles */
    .stApp {
        max-width: 100%;
        padding: 1rem;
    }

    /* Chat container styling */
    .stChatMessage {
        border-radius: 25px !important;
        padding: 1.5rem !important;
        margin: 1rem 0 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
        width: 100% !important;
        max-width: 800px !important;
        margin-left: auto !important;
        margin-right: auto !important;
    }

    .stChatMessage:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.15) !important;
    }
    
    /* User message styling */
    .stChatMessage[data-testid="user-message"] {
        background-color: #e6f3ff !important;
        margin-left: auto !important;
        border-top-right-radius: 25px !important;
        border-bottom-right-radius: 25px !important;
        border-top-left-radius: 25px !important;
        border-bottom-left-radius: 5px !important;
    }
    
    /* Assistant message styling */
    .stChatMessage[data-testid="assistant-message"] {
        background-color: #f0f2f6 !important;
        margin-right: auto !important;
        border-top-right-radius: 25px !important;
        border-bottom-right-radius: 5px !important;
        border-top-left-radius: 25px !important;
        border-bottom-left-radius: 25px !important;
    }
    
    /* Message content styling */
    .stMarkdown {
        border-radius: 25px !important;
        font-size: clamp(0.875rem, 2vw, 1rem) !important;
    }
    
    /* Input box styling */
    .stChatInputContainer {
        border-radius: 25px !important;
        padding: 0.5rem !important;
        background-color: #ffffff !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
        transition: all 0.3s ease !important;
        position: fixed !important;
        bottom: 0 !important;
        left: 0 !important;
        right: 0 !important;
        margin: 1rem !important;
        z-index: 1000 !important;
        max-width: calc(100% - 2rem) !important;
    }

    .stChatInputContainer:focus-within {
        box-shadow: 0 4px 8px rgba(0,0,0,0.15) !important;
        transform: translateY(-2px) !important;
    }

    /* Button styling */
    .stButton > button {
        border-radius: 25px !important;
        padding: 0.5rem 1.5rem !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
        max-width: 300px !important;
        margin: 0 auto !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.15) !important;
    }

    /* Sidebar styling */
    .css-1d391kg, .css-1544g2n {
        border-radius: 25px !important;
        padding: 1rem !important;
    }

    /* Input fields styling */
    .stTextInput > div > div > input {
        border-radius: 25px !important;
        padding: 0.5rem 1rem !important;
        transition: all 0.3s ease !important;
        font-size: clamp(0.875rem, 2vw, 1rem) !important;
    }

    .stTextInput > div > div > input:focus {
        box-shadow: 0 4px 8px rgba(0,0,0,0.15) !important;
        transform: translateY(-2px) !important;
    }

    /* Selectbox styling */
    .stSelectbox > div > div > div {
        border-radius: 25px !important;
        transition: all 0.3s ease !important;
        font-size: clamp(0.875rem, 2vw, 1rem) !important;
    }

    .stSelectbox > div > div > div:hover {
        border-color: #1f77b4 !important;
    }

    /* Expander styling */
    .streamlit-expanderHeader {
        border-radius: 25px !important;
        transition: all 0.3s ease !important;
        font-size: clamp(0.875rem, 2vw, 1rem) !important;
    }

    .streamlit-expanderHeader:hover {
        background-color: #f0f2f6 !important;
    }

    /* Title and header styling */
    h1, h2, h3 {
        font-size: clamp(1.5rem, 4vw, 2.5rem) !important;
        line-height: 1.2 !important;
        margin-bottom: 1rem !important;
    }

    /* Tablet styles */
    @media (max-width: 992px) {
        .stApp {
            padding: 0.5rem;
        }

        .stChatMessage {
            padding: 1.25rem !important;
            margin: 0.75rem auto !important;
            max-width: 90% !important;
        }

        .stSidebar {
            min-width: 250px !important;
            max-width: 300px !important;
        }
    }

    /* Mobile styles */
    @media (max-width: 768px) {
        .stApp {
            padding: 0.25rem;
        }

        .stChatMessage {
            padding: 1rem !important;
            margin: 0.5rem auto !important;
            max-width: 95% !important;
        }

        .stChatMessage[data-testid="user-message"],
        .stChatMessage[data-testid="assistant-message"] {
            margin: 0.5rem auto !important;
        }

        .stButton > button {
            max-width: 100% !important;
            margin-bottom: 0.5rem !important;
            font-size: 0.9rem !important;
        }

        .stSidebar {
            min-width: 200px !important;
            max-width: 100% !important;
        }

        .row-widget.stSelectbox,
        .row-widget.stTextInput {
            margin-bottom: 0.5rem !important;
        }

        .stChatInputContainer {
            margin: 0.5rem !important;
            max-width: calc(100% - 1rem) !important;
        }
    }

    /* Small mobile styles */
    @media (max-width: 480px) {
        .stMarkdown {
            font-size: 0.85rem !important;
        }

        .stChatInputContainer {
            padding: 0.3rem !important;
        }

        h1, h2, h3 {
            font-size: clamp(1.25rem, 3vw, 2rem) !important;
        }

        .stTextInput > div > div > input,
        .stSelectbox > div > div > div {
            font-size: 0.85rem !important;
        }
    }

    /* Add padding to bottom to account for fixed chat input */
    .main .block-container {
        padding-bottom: 80px !important;
    }

    /* Improve scrolling experience */
    .stApp {
        overflow-y: auto !important;
        -webkit-overflow-scrolling: touch !important;
    }

    /* Improve touch targets on mobile */
    @media (pointer: coarse) {
        .stButton > button,
        .stSelectbox > div > div > div,
        .stTextInput > div > div > input {
            min-height: 44px !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# Function to generate a random Google Meet link


def parse_date_time(message):
    """Parse date and time from user message"""
    message = message.lower()
    current_date = datetime.now()

    # Initialize date and time
    target_date = None
    target_time = None

    # Check for specific days
    if "today" in message:
        target_date = current_date.date()
    elif "tomorrow" in message:
        target_date = (current_date + timedelta(days=1)).date()
    else:
        # Check for days of the week
        days = {
            'monday': 0, 'tuesday': 1, 'wednesday': 2,
            'thursday': 3, 'friday': 4, 'saturday': 5, 'sunday': 6
        }
        for day, day_num in days.items():
            if day in message:
                # Calculate days until next occurrence of this day
                current_day = current_date.weekday()
                days_ahead = day_num - current_day
                if days_ahead <= 0:  # If the day has passed this week
                    days_ahead += 7
                target_date = (
                    current_date + timedelta(days=days_ahead)).date()
                break

        # Check for specific date (format: DD/MM, DD-MM, DD.MM)
        date_patterns = [
            r'(\d{1,2})[/.-](\d{1,2})',  # DD/MM or D/M
        ]
        for pattern in date_patterns:
            match = re.search(pattern, message)
            if match:
                day, month = map(int, match.groups())
                year = current_date.year
                try:
                    target_date = datetime(year, month, day).date()
                    # If the date is in the past, assume next year
                    if target_date < current_date.date():
                        target_date = datetime(year + 1, month, day).date()
                    break
                except ValueError:
                    continue

    # Parse time
    # Look for HH:MM format
    time_pattern = r'(\d{1,2}):(\d{2})'
    time_matches = re.findall(time_pattern, message)

    # Look for simple hour mentions with AM/PM
    hour_pattern = r'(\d{1,2})\s*(am|pm)'
    hour_matches = re.findall(hour_pattern, message)

    if time_matches:
        # Use HH:MM format
        hour, minute = map(int, time_matches[0])
        if "pm" in message.lower() and hour < 12:
            hour += 12
        elif "am" in message.lower() and hour == 12:
            hour = 0
        try:
            target_time = datetime.strptime(f"{hour}:{minute}", "%H:%M").time()
        except ValueError:
            pass
    elif hour_matches:
        # Use simple hour format
        hour = int(hour_matches[0][0])
        meridian = hour_matches[0][1].lower()
        if meridian == "pm" and hour < 12:
            hour += 12
        elif meridian == "am" and hour == 12:
            hour = 0
        try:
            target_time = datetime.strptime(f"{hour}:00", "%H:%M").time()
        except ValueError:
            pass

    return target_date, target_time

# Initialize the scheduling bot and calendar manager


@st.cache_resource
def load_bot():
    return SchedulingBot()


@st.cache_resource
def load_calendar_manager():
    return CalendarManager()


# Initialize session state variables if they don't exist
if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'scheduled' not in st.session_state:
    st.session_state.scheduled = False

if 'meeting_info' not in st.session_state:
    st.session_state.meeting_info = None

if 'step' not in st.session_state:
    st.session_state.step = 'greeting'

if 'candidate_email' not in st.session_state:
    st.session_state.candidate_email = ""

if 'recruiter_email' not in st.session_state:
    st.session_state.recruiter_email = ""

if 'available_time' not in st.session_state:
    st.session_state.available_time = None

if 'department' not in st.session_state:
    st.session_state.department = None

if 'selected_date' not in st.session_state:
    st.session_state.selected_date = None

if 'selected_time' not in st.session_state:
    st.session_state.selected_time = None

# Load the bot and calendar manager
bot = load_bot()
calendar_manager = load_calendar_manager()

# Main app interface
st.title("AI Interview Scheduler 🤖")

# Sidebar for configuration
with st.sidebar:
    st.header("Setup")

    # Email configuration
    st.subheader("Participant Information")
    recruiter_email = st.text_input(
        "Recruiter Email", value=st.session_state.recruiter_email or "chillajagadesh68@gmail.com")
    candidate_email = st.text_input(
        "Candidate Email", value=st.session_state.candidate_email or "")

    if recruiter_email and candidate_email:
        st.session_state.recruiter_email = recruiter_email
        st.session_state.candidate_email = candidate_email
        bot.set_participants(recruiter_email, candidate_email)

    # Department selection
    st.subheader("Department")
    department = st.selectbox(
        "Select Department",
        ["Engineering", "HR", "Sales", "Marketing", "Product", "Design"],
        index=0 if not st.session_state.department else [
            "Engineering", "HR", "Sales", "Marketing", "Product", "Design"].index(st.session_state.department)
    )
    st.session_state.department = department

    # Reset button
    if st.button("Reset Conversation"):
        st.session_state.messages = []
        st.session_state.scheduled = False
        st.session_state.meeting_info = None
        st.session_state.step = 'greeting'
        st.session_state.available_time = None
        st.session_state.selected_date = None
        st.session_state.selected_time = None
        st.rerun()

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Initialize the chat with a greeting if it's the first interaction
if len(st.session_state.messages) == 0:
    with st.chat_message("assistant"):
        st.write(
            "👋 Hello! I'm your Interview Scheduling Assistant. How can I help you today?")

    st.session_state.messages.append(
        {"role": "assistant", "content": "👋 Hello! I'm your Interview Scheduling Assistant. How can I help you today?"})

# Handle user input
if user_input := st.chat_input("Type your message here..."):
    # Display user message
    with st.chat_message("user"):
        st.write(user_input)

    st.session_state.messages.append({"role": "user", "content": user_input})

    # Process the message with the bot
    with st.chat_message("assistant"):
        response_placeholder = st.empty()

        # Check if emails are set
        if not st.session_state.recruiter_email or not st.session_state.candidate_email:
            response = "⚠️ Please enter both recruiter and candidate email addresses in the sidebar first."
            response_placeholder.write(response)
            st.session_state.messages.append(
                {"role": "assistant", "content": response})
            st.stop()

        # Process the conversation step by step
        if "schedule" in user_input.lower() or "interview" in user_input.lower() or "meeting" in user_input.lower():
            if st.session_state.step == 'greeting':
                response = """I'll help you schedule an interview. Please let me know your preferred day and time within the next week.
                
You can specify:
- A specific day (e.g., "Monday at 2 PM")
- Relative day (e.g., "tomorrow at 3:30 PM")
- Today with time (e.g., "today at 4 PM")
- A specific date (e.g., "25/03 at 2:30 PM")"""
                st.session_state.step = 'collect_availability'
            else:
                response = bot.process_message(user_input)

        else:
            # Try to parse date and time from the message
            target_date, target_time = parse_date_time(user_input)

            if st.session_state.step == 'collect_availability':
                if target_date and target_time:
                    # Both date and time provided
                    meeting_datetime = datetime.combine(
                        target_date, target_time)
                    if meeting_datetime < datetime.now():
                        response = "⚠️ The specified time is in the past. Please provide a future date and time."
                    else:
                        st.session_state.available_time = meeting_datetime.replace(
                            tzinfo=pytz.UTC)
                        meeting_suggestion = bot.suggest_time_slot(
                            department=st.session_state.department)
                        response = f"Thanks! I see you're available on {target_date.strftime('%A, %B %d')} at {target_time.strftime('%I:%M %p')}. {meeting_suggestion} Would you like me to schedule this now?"
                        st.session_state.step = 'confirm_schedule'
                elif target_date:
                    # Only date provided, ask for time
                    st.session_state.selected_date = target_date
                    response = f"I see you're interested in {target_date.strftime('%A, %B %d')}. What time would work best for you?"
                elif target_time:
                    # Only time provided, ask for date
                    st.session_state.selected_time = target_time
                    response = f"I see you prefer {target_time.strftime('%I:%M %p')}. Which day would you like to schedule this for?"
                else:
                    # Handle other responses during availability collection
                    response = "I didn't catch a specific day or time. Could you please specify when you'd like to schedule the interview? For example, 'tomorrow at 2 PM' or 'Monday at 3:30 PM'."

            elif "yes" in user_input.lower() or "confirm" in user_input.lower() or "schedule" in user_input.lower():
                if st.session_state.step == 'confirm_schedule' and st.session_state.available_time:
                    # Schedule the meeting
                    with st.spinner("Scheduling your interview..."):
                        # Generate Google Meet link
                        meet_link = generate_meet_link()

                        # Extract meeting type from bot context
                        meeting_type = bot.context.get(
                            'meeting_type', 'Technical Interview')
                        duration = bot.context.get('duration', 60)

                        # Create meeting info
                        meeting_start = st.session_state.available_time
                        meeting_end = meeting_start + \
                            timedelta(minutes=duration)

                        meeting_info = {
                            'title': f'{meeting_type} - {st.session_state.department} Position',
                            'start_time': meeting_start,
                            'end_time': meeting_end,
                            'timezone': 'UTC',
                            'location': meet_link,
                            'description': f'''{meeting_type} for {st.session_state.department} Position

Meeting Link: {meet_link}

Agenda:
1. Introduction
2. Technical/Role Discussion
3. Q&A

Please prepare to discuss your experience and relevant skills.
Join the meeting using the Google Meet link above.

Note: If you have any issues joining the meeting, please contact the recruiter.''',
                            'meeting_type': meeting_type,
                            'recruiter_email': st.session_state.recruiter_email,
                            'candidate_email': st.session_state.candidate_email
                        }

                        # Store meeting info in session state
                        st.session_state.meeting_info = meeting_info

                        # Send calendar invite
                        success = calendar_manager.send_calendar_invite(
                            meeting_info)

                        if success:
                            st.session_state.scheduled = True
                            response = f"""✅ Interview scheduled successfully!

**Meeting Details:**
- **Type:** {meeting_type}
- **Date:** {meeting_start.strftime('%A, %B %d, %Y')}
- **Time:** {meeting_start.strftime('%I:%M %p')} - {meeting_end.strftime('%I:%M %p')} UTC
- **Participants:** {st.session_state.recruiter_email}, {st.session_state.candidate_email}
- **Meeting Link:** {meet_link}

Calendar invites have been sent to both participants. Looking forward to the interview!"""
                            st.session_state.step = 'completed'
                        else:
                            response = "⚠️ There was an issue sending the calendar invite. Please check the email configuration and try again."
                else:
                    response = bot.process_message(user_input)

            elif "reschedule" in user_input.lower() or "change" in user_input.lower():
                # Reset the scheduling process
                st.session_state.scheduled = False
                st.session_state.meeting_info = None
                st.session_state.available_time = None
                st.session_state.selected_date = None
                st.session_state.selected_time = None
                st.session_state.step = 'collect_availability'
                response = """I understand you want to reschedule. Please let me know your new preferred day and time.

You can specify:
- A specific day (e.g., "Monday at 2 PM")
- Relative day (e.g., "tomorrow at 3:30 PM")
- Today with time (e.g., "today at 4 PM")
- A specific date (e.g., "25/03 at 2:30 PM")"""

            elif "cancel" in user_input.lower():
                if st.session_state.scheduled:
                    st.session_state.scheduled = False
                    st.session_state.meeting_info = None
                    st.session_state.available_time = None
                    st.session_state.selected_date = None
                    st.session_state.selected_time = None
                    response = "I've cancelled the scheduled interview. Let me know if you'd like to schedule another time."
                    st.session_state.step = 'greeting'
                else:
                    response = "There's no active interview scheduled to cancel. Would you like to schedule a new interview?"
                    st.session_state.step = 'greeting'

            else:
                # Default response for other queries
                response = bot.process_message(user_input)

        # Display the response with a typing animation
        full_response = ""
        for chunk in response.split():
            full_response += chunk + " "
            time.sleep(0.05)
            response_placeholder.write(full_response)

    st.session_state.messages.append(
        {"role": "assistant", "content": response})

# Display meeting details if a meeting has been scheduled
if st.session_state.scheduled and st.session_state.meeting_info:
    with st.expander("View Meeting Details", expanded=True):
        meeting_info = st.session_state.meeting_info
        st.subheader("📅 Scheduled Interview")
        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"**Meeting Type:** {meeting_info['meeting_type']}")
            st.markdown(
                f"**Date:** {meeting_info['start_time'].strftime('%A, %B %d, %Y')}")
            st.markdown(
                f"**Time:** {meeting_info['start_time'].strftime('%I:%M %p')} - {meeting_info['end_time'].strftime('%I:%M %p')} UTC")

        with col2:
            st.markdown(f"**Recruiter:** {meeting_info['recruiter_email']}")
            st.markdown(f"**Candidate:** {meeting_info['candidate_email']}")
            st.markdown(f"**Location:** Virtual (Google Meet)")

        st.markdown(
            f"**Meeting Link:** [{meeting_info['location']}]({meeting_info['location']})")

# Footer
st.markdown("---")
st.caption("AI Interview Scheduler by Jagadesh")
