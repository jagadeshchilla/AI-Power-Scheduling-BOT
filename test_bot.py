"""
Test module for the AI Interview Scheduler

This module contains test cases for the scheduling bot and calendar functionality.
It simulates a conversation flow and tests the meeting scheduling process.
"""

from scheduling_bot import SchedulingBot
from calendar_utils import CalendarManager
from datetime import datetime, timedelta
import pytz
from utils import generate_meet_link


def test_scheduling_conversation():
    """
    Test the complete interview scheduling conversation flow.

    This function tests:
    1. Basic conversation handling
    2. Time slot suggestions
    3. Meeting scheduling
    4. Calendar invite sending
    """
    # Initialize the bot and calendar manager
    bot = SchedulingBot()
    calendar = CalendarManager()

    # Set up test participants
    recruiter_email = "chillajagadesh68@gmail.com"
    candidate_email = "nikithchowdaryachanta@gmail.com"
    bot.set_participants(recruiter_email, candidate_email)

    # Test conversation flow
    conversations = [
        ("Candidate", "I'm looking to schedule an interview"),
        ("Bot", "I'll help you find a suitable time slot. What days work best for you?"),
        ("Candidate", "I'm available tomorrow between 3 PM and 5 PM"),
        ("Bot", "I've noted your availability. Would you like me to schedule the meeting?"),
        ("Candidate", "Yes, please schedule it"),
        ("Bot", "Let me suggest a suitable meeting type for you.")
    ]

    print("Starting test conversation:")
    print("-" * 50)

    for speaker, message in conversations:
        print(f"{speaker}: {message}")
        if speaker == "Candidate":
            response = bot.process_message(message)
            print(f"Bot: {response}")

    # Test time slot suggestion
    print("\nTesting time slot suggestion:")
    print("-" * 50)
    suggestion = bot.suggest_time_slot(department="Engineering")
    print(f"Bot: {suggestion}")

    # Schedule actual meeting
    print("\nScheduling the meeting:")
    print("-" * 50)

    # Generate Google Meet link
    meet_link = generate_meet_link()

    # Create meeting info
    tomorrow = datetime.now(pytz.UTC) + timedelta(days=1)
    meeting_start = tomorrow.replace(
        hour=15, minute=0, second=0, microsecond=0)  # 3 PM tomorrow
    meeting_end = meeting_start + timedelta(hours=1)

    meeting_info = {
        'title': 'Technical Interview - Engineering Position',
        'start_time': meeting_start,
        'end_time': meeting_end,
        'timezone': 'UTC',
        'location': meet_link,
        'description': f'''Technical Interview for Engineering Position

Meeting Link: {meet_link}

Agenda:
1. Technical Discussion
2. Problem Solving Session
3. Q&A

Please prepare to discuss your experience and technical skills.
Join the meeting using the Google Meet link above.

Note: If you have any issues joining the meeting, please contact the recruiter.''',
        'meeting_type': 'Technical Interview',
        'recruiter_email': recruiter_email,
        'candidate_email': candidate_email
    }

    # Send calendar invite
    print("Sending calendar invite...")
    if calendar.send_calendar_invite(meeting_info):
        print("✓ Calendar invite sent successfully!")
        print(f"\nMeeting Details:")
        print(f"Date: {meeting_start.strftime('%Y-%m-%d')}")
        print(
            f"Time: {meeting_start.strftime('%I:%M %p')} - {meeting_end.strftime('%I:%M %p')} UTC")
        print(f"Participants: {recruiter_email}, {candidate_email}")
        print(f"Type: {meeting_info['meeting_type']}")
        print(f"Meeting Link: {meet_link}")
    else:
        print(
            "× Failed to send calendar invite. Please check email settings and try again.")


if __name__ == "__main__":
    test_scheduling_conversation()
