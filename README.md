# AI Interview Scheduling Bot

An intelligent scheduling system that automates the interview scheduling process using AI and natural language processing.

## Project Overview

This project implements an AI-powered interview scheduling system that can:

- Process natural language requests for scheduling
- Suggest optimal meeting times
- Handle calendar management
- Send automated calendar invites
- Manage scheduling conflicts
- Provide a user-friendly web interface

## Components

### 1. Web Interface (`streamlit_app.py`)

- Built with Streamlit for a modern, responsive UI
- Real-time chat interface for scheduling interactions
- Sidebar for configuration settings
- Meeting details display
- Calendar integration

### 2. Calendar Management (`calendar_utils.py`)

- Calendar event creation and management
- Meeting invite generation and sending
- Working hours management
- Availability checking
- Buffer time handling
- Integration with Google Calendar

### 3. Scheduling Bot (`scheduling_bot.py`)

- Natural language processing for scheduling requests
- Intent classification
- Time slot suggestion
- Meeting type determination
- Conversation flow management

### 4. Utility Functions (`utils.py`)

- Common utility functions
- Google Meet link generation
- Helper functions for date/time handling

### 5. Configuration (`config.py`)

- Email settings
- Calendar settings
- Working hours configuration
- Meeting duration defaults
- Bot behavior settings

### 6. Testing (`test_bot.py`)

- Comprehensive test suite
- Conversation flow testing
- Calendar functionality testing
- End-to-end scheduling tests

## Machine Learning Components

### 1. Dataset Generation

- Conversation dataset generation
- Calendar event dataset creation
- Synthetic data for training

### 2. Model Training

- Intent classification model
- Time slot prediction model
- Feature engineering
- Model evaluation and selection

### 3. Data Processing

- Text preprocessing
- Feature extraction
- Label encoding
- Data validation

## Setup and Configuration

### Prerequisites

- Python 3.8+
- Required packages:
  - streamlit
  - pandas
  - numpy
  - scikit-learn
  - icalendar
  - pytz
  - faker (for testing)

### Email Configuration

```python
EMAIL_CONFIG = {
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'email': 'your-email@gmail.com',
    'password': 'your-app-specific-password'
}
```

### Calendar Settings

```python
CALENDAR_CONFIG = {
    'working_hours': {
        'start': 9,  # 9 AM
        'end': 17    # 5 PM
    },
    'meeting_durations': {
        'Technical Interview': 60,
        'HR Screening': 45,
        'Final Round': 90,
        'Initial Discussion': 30
    },
    'buffer_time': 15  # minutes between meetings
}
```

## Features Implemented

1. **Natural Language Processing**

   - Date and time extraction
   - Intent recognition
   - Context maintenance
   - Multi-language support

2. **Calendar Management**

   - Automated event creation
   - iCalendar invite generation
   - Google Meet integration
   - Timezone handling

3. **User Interface**

   - Real-time chat
   - Dynamic meeting updates
   - Responsive design
   - Configuration management

4. **Machine Learning**

   - Intent classification
   - Time slot optimization
   - Meeting type prediction
   - Model persistence

5. **Testing and Validation**
   - Unit tests
   - Integration tests
   - Synthetic data generation
   - Error handling

## Security Features

1. **Email Security**

   - SMTP with TLS
   - App-specific passwords
   - Secure credential handling

2. **Meeting Links**
   - Secure Google Meet link generation
   - Unique meeting identifiers
   - Access control

## Future Enhancements

1. **Integration Possibilities**

   - Microsoft Teams integration
   - Zoom integration
   - Slack integration
   - Mobile app development

2. **AI Improvements**
   - Advanced NLP capabilities
   - Learning from user preferences
   - Automated follow-ups
   - Multi-participant scheduling

## Running the Application

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Configure email and calendar settings in `config.py`

3. Run the Streamlit app:

```bash
python3 -m streamlit run streamlit_app.py
```

## Testing

Run the test suite:

```bash
python test_bot.py
```

## Contributors

- Jagadesh Chilla

## License

This project is licensed under the MIT License - see the LICENSE file for details.
