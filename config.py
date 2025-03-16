# Email Configuration
EMAIL_CONFIG = {
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'email': 'chillajagadesh68@gmail.com',
    # This should be an App Password generated from Google Account settings
    'password': 'bmrs kbjo zyjw omdp'
}

# Calendar Settings
CALENDAR_CONFIG = {
    'working_hours': {
        'start': 9,  # 9 AM
        'end': 17    # 5 PM
    },
    'meeting_durations': {
        'Technical Interview': 60,
        'HR Screening': 45,
        'Final Round': 90,
        'Initial Discussion': 30,
        'Follow-up Meeting': 30,
        'Project Presentation': 60
    },
    'buffer_time': 15  # minutes between meetings
}

# Bot Settings
BOT_CONFIG = {
    'default_timezone': 'UTC',
    'supported_languages': ['en', 'es', 'fr', 'de'],
    'model_paths': {
        'intent_model': 'results/best_intent_classification_model.pkl',
        'time_slot_model': 'results/best_time_slot_prediction_model.pkl',
        'conversation_encoders': 'results/conversation_label_encoders.pkl',
        'calendar_encoders': 'results/calendar_label_encoders.pkl'
    }
}
