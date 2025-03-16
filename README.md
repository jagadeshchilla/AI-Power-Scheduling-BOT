# AI Interview Scheduling Bot 🤖

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An intelligent AI-powered system that automates interview scheduling through natural language processing and machine learning.

## 🌟 Features

- Natural language processing for scheduling requests
- AI-powered optimal time slot suggestions
- Automated calendar management and invites
- Real-time chat interface
- Google Calendar integration
- Smart conflict resolution
- Multi-language support

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Google Calendar API credentials
- SMTP server access for email notifications

### Installation

1. Clone the repository:

```bash
git clone https://github.com/jagadeshchilla/AI-Power-Scheduling-BOT-.git
cd AI-Power-Scheduling-BOT-
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Configure your credentials:

   - Create a `credentials.json` file with your Google Calendar API credentials
   - Update email settings in `config.py`

4. Run the application:

```bash
streamlit run streamlit_app.py
```

## 🏗️ Architecture

### Core Components

- **Web Interface** (`streamlit_app.py`): Modern Streamlit-based UI
- **Calendar Management** (`calendar_utils.py`): Event handling and Google Calendar integration
- **Scheduling Bot** (`scheduling_bot.py`): NLP and scheduling logic
- **ML Models** (`results/`): Pre-trained models for intent classification and time slot prediction

### Machine Learning Pipeline

- Intent Classification
- Time Slot Optimization
- Meeting Type Prediction
- Context Understanding

## 📊 Data Processing

The system processes two main types of data:

- Conversation data for intent classification
- Calendar data for time slot optimization

Pre-trained models and encoders are stored in the `results/` directory.

## ⚙️ Configuration

Key configurations in `config.py`:

```python
CALENDAR_CONFIG = {
    'working_hours': {'start': 9, 'end': 17},
    'buffer_time': 15  # minutes
}

EMAIL_CONFIG = {
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587
}
```

## 🧪 Testing

Run the test suite:

```bash
python test_bot.py
```

## 🔒 Security

- SMTP with TLS encryption
- Secure credential handling
- OAuth2.0 authentication for Google Calendar
- Environment variable-based secrets management

## 🛣️ Roadmap

- [ ] Microsoft Teams/Zoom integration
- [ ] Mobile application development
- [ ] Multi-participant scheduling
- [ ] Advanced NLP capabilities
- [ ] User preference learning

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Jagadesh Chilla**

- GitHub: [@jagadeshchilla](https://github.com/jagadeshchilla)

## ⭐ Show your support

Give a ⭐️ if this project helped you!
