import os
import joblib
import pandas as pd
from datetime import datetime, timedelta
import pytz
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib


class SchedulingBot:
    def __init__(self):
        # Load trained models
        self.intent_model = joblib.load(
            'results/best_intent_classification_model.pkl')
        self.time_slot_model = joblib.load(
            'results/best_time_slot_prediction_model.pkl')

        # Load label encoders
        self.conversation_encoders = joblib.load(
            'results/conversation_label_encoders.pkl')
        self.calendar_encoders = joblib.load(
            'results/calendar_label_encoders.pkl')

        # Initialize conversation context
        self.context = {
            'current_recruiter': None,
            'current_candidate': None,
            'proposed_time': None,
            'meeting_type': None,
            'duration': 60  # default duration in minutes
        }

    def process_message(self, message, speaker='Candidate'):
        """Process incoming messages and determine intent"""
        # Prepare features for intent classification
        features = self._prepare_conversation_features(message, speaker)

        # Predict intent
        intent_encoded = self.intent_model.predict([features])[0]
        intent = self.conversation_encoders['Intent_Label'].inverse_transform([
                                                                              intent_encoded])[0]

        # Handle intent
        response = self._handle_intent(intent, message)
        return response

    def _prepare_conversation_features(self, message, speaker):
        """Prepare features for intent classification"""
        # Basic feature extraction
        hour = datetime.now().hour
        text_length = len(message)
        speaker_encoded = self.conversation_encoders['Speaker'].transform([speaker])[
            0]

        # Default values for other features
        language_encoded = self.conversation_encoders['Language'].transform(['en'])[
            0]
        sentiment_encoded = self.conversation_encoders['Sentiment'].transform(['neutral'])[
            0]

        return [hour, text_length, speaker_encoded, language_encoded, sentiment_encoded]

    def _handle_intent(self, intent, message):
        """Handle different intents and generate appropriate responses"""
        if intent == 'offer_availability':
            # Extract time information from message
            # For now, just store a dummy time
            self.context['proposed_time'] = datetime.now() + timedelta(days=1)
            return "I've noted your availability. Would you like me to schedule the meeting?"

        elif intent == 'schedule_meeting':
            if self.context['proposed_time']:
                return self._schedule_meeting()
            else:
                return "Please let me know your preferred time first."

        elif intent == 'reschedule':
            return "I understand you want to reschedule. Please provide your new availability."

        elif intent == 'cancel_meeting':
            return "I'll help you cancel the meeting. Please confirm if you want to proceed."

        elif intent == 'request_time_slot':
            return "I'll help you find a suitable time slot. What days work best for you?"

        else:
            return "I'm not sure how to help with that. Could you please rephrase?"

    def _schedule_meeting(self):
        """Schedule a meeting and send calendar invites"""
        if not all([self.context['current_recruiter'],
                   self.context['current_candidate'],
                   self.context['proposed_time']]):
            return "Missing required information to schedule the meeting."

        # Here we would:
        # 1. Check final availability
        # 2. Create calendar event
        # 3. Send invites

        return f"Meeting scheduled for {self.context['proposed_time'].strftime('%Y-%m-%d %H:%M')}. Calendar invites will be sent shortly."

    def set_participants(self, recruiter_id, candidate_id):
        """Set the participants for the current scheduling session"""
        self.context['current_recruiter'] = recruiter_id
        self.context['current_candidate'] = candidate_id

    def suggest_time_slot(self, department, duration=60):
        """Suggest a time slot based on the trained model"""
        # Prepare features for time slot prediction
        features = self._prepare_calendar_features(department, duration)

        # Predict meeting type
        meeting_type_encoded = self.time_slot_model.predict([features])[0]
        meeting_type = self.calendar_encoders['Meeting_Type'].inverse_transform(
            [meeting_type_encoded])[0]

        self.context['meeting_type'] = meeting_type
        self.context['duration'] = duration

        return f"I suggest scheduling a {meeting_type} for {duration} minutes."

    def _prepare_calendar_features(self, department, duration):
        """Prepare features for time slot prediction"""
        # Encode department
        department_encoded = self.calendar_encoders['Department'].transform([department])[
            0]

        # Default values for other features
        availability_encoded = self.calendar_encoders['Availability_Status'].transform([
                                                                                       'Available'])[0]
        location_encoded = self.calendar_encoders['Location'].transform(['Zoom'])[
            0]

        return [duration, availability_encoded, location_encoded, department_encoded]


# Example usage
if __name__ == "__main__":
    # Initialize the bot
    bot = SchedulingBot()

    # Set participants
    bot.set_participants(
        recruiter_id="R123",
        candidate_id="C456"
    )

    # Example conversation
    messages = [
        "I'm available tomorrow between 2 PM and 4 PM",
        "Can we schedule a meeting?",
        "I need to reschedule our meeting",
        "What time slots are available next week?"
    ]

    # Process messages
    for message in messages:
        response = bot.process_message(message)
        print(f"\nUser: {message}")
        print(f"Bot: {response}")

    # Get time slot suggestion
    suggestion = bot.suggest_time_slot(department="Engineering")
    print(f"\nBot: {suggestion}")
