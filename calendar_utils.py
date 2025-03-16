"""
Calendar Management Module

This module handles all calendar-related functionality including:
- Creating calendar events
- Sending calendar invites
- Managing working hours and meeting durations
"""

import os
from datetime import datetime, timedelta
import pytz
from config import CALENDAR_CONFIG
import icalendar
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import smtplib
from config import EMAIL_CONFIG


class CalendarManager:
    """
    Manages calendar operations including event creation and scheduling.

    This class handles:
    - Calendar event creation
    - Meeting invites
    - Availability checking
    - Working hours management
    """

    def __init__(self):
        """Initialize the calendar manager with configuration settings."""
        self.working_hours = CALENDAR_CONFIG['working_hours']
        self.meeting_durations = CALENDAR_CONFIG['meeting_durations']
        self.buffer_time = CALENDAR_CONFIG['buffer_time']

    def create_calendar_event(self, meeting_info):
        """
        Create an iCalendar event with the specified meeting information.

        Args:
            meeting_info (dict): Dictionary containing meeting details including:
                - title: Meeting title
                - start_time: Start datetime
                - end_time: End datetime
                - location: Meeting location/URL
                - description: Meeting description
                - recruiter_email: Organizer's email
                - candidate_email: Attendee's email

        Returns:
            icalendar.Calendar: The created calendar event
        """
        cal = icalendar.Calendar()
        cal.add('prodid', '-//Scheduling Bot//scheduling.bot//')
        cal.add('version', '2.0')
        cal.add('method', 'REQUEST')  # This is important for calendar invites

        event = icalendar.Event()

        # Basic event details
        event.add('summary', meeting_info['title'])
        event.add('dtstart', meeting_info['start_time'])
        event.add('dtend', meeting_info['end_time'])
        event.add('dtstamp', datetime.now(pytz.UTC))

        # Location and description
        event.add('location', meeting_info['location'])
        event.add('description', meeting_info['description'])

        # Add URL for the meeting
        if 'meet.google.com' in meeting_info['location']:
            event.add('url', meeting_info['location'])

        # Add organizer with common name
        event.add('organizer', f'mailto:{meeting_info["recruiter_email"]}')

        # Add attendees with roles
        event.add('attendee', f'mailto:{meeting_info["recruiter_email"]}',
                  parameters={'ROLE': 'CHAIR',
                              'PARTSTAT': 'ACCEPTED',
                              'RSVP': 'FALSE'})

        event.add('attendee', f'mailto:{meeting_info["candidate_email"]}',
                  parameters={'ROLE': 'REQ-PARTICIPANT',
                              'PARTSTAT': 'NEEDS-ACTION',
                              'RSVP': 'TRUE'})

        # Add reminder (15 minutes before)
        alarm = icalendar.Alarm()
        alarm.add('action', 'DISPLAY')
        alarm.add('trigger', timedelta(minutes=-15))
        alarm.add('description', 'Reminder')
        event.add_component(alarm)

        cal.add_component(event)
        return cal

    def send_calendar_invite(self, meeting_info):
        """
        Send calendar invite via email to all participants.

        Args:
            meeting_info (dict): Dictionary containing meeting details
                (same structure as create_calendar_event)

        Returns:
            bool: True if the invite was sent successfully, False otherwise
        """
        try:
            # Create the calendar event
            cal = self.create_calendar_event(meeting_info)

            # Create email message
            msg = MIMEMultipart()
            msg['Subject'] = meeting_info['title']
            msg['From'] = EMAIL_CONFIG['email']
            msg['To'] = ', '.join([meeting_info['candidate_email'],
                                   meeting_info['recruiter_email']])
            msg['Content-Type'] = 'text/calendar; method=REQUEST'

            # Add meeting details to email body
            body = self._create_email_body(meeting_info)
            msg.attach(MIMEText(body, 'plain'))

            # Add calendar invite attachment
            ical_data = cal.to_ical()
            attachment = MIMEBase('text', 'calendar',
                                  method='REQUEST', name='invite.ics')
            attachment.set_payload(ical_data)
            encoders.encode_base64(attachment)
            attachment.add_header('Content-Disposition',
                                  'attachment; filename="invite.ics"')
            attachment.add_header(
                'Content-Type', 'text/calendar; method=REQUEST; name="invite.ics"')
            msg.attach(attachment)

            # Send email
            with smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port']) as server:
                server.starttls()
                server.login(EMAIL_CONFIG['email'], EMAIL_CONFIG['password'])
                server.send_message(msg)
            return True

        except Exception as e:
            print(f"Failed to send calendar invite: {str(e)}")
            return False

    def _create_email_body(self, meeting_info):
        """
        Create the email body text for the calendar invite.

        Args:
            meeting_info (dict): Dictionary containing meeting details

        Returns:
            str: Formatted email body text
        """
        body = f"""
Hello,

You are invited to a {meeting_info['meeting_type']}.

Date: {meeting_info['start_time'].strftime('%Y-%m-%d')}
Time: {meeting_info['start_time'].strftime('%I:%M %p')} - {meeting_info['end_time'].strftime('%I:%M %p')} {meeting_info['timezone']}
Location: Virtual Meeting

Meeting Link: {meeting_info['location']}

{meeting_info.get('description', '')}

Best regards,
Scheduling Bot
"""
        return body

    def check_availability(self, date, start_time, duration, timezone='UTC'):
        """
        Check if a time slot is available for scheduling.

        Args:
            date (date): The date to check
            start_time (time): The start time to check
            duration (int): Meeting duration in minutes
            timezone (str): Timezone name (default: 'UTC')

        Returns:
            bool: True if the slot is available, False otherwise
        """
        # Convert to UTC for standardization
        tz = pytz.timezone(timezone)
        local_dt = tz.localize(datetime.combine(date, start_time))
        utc_dt = local_dt.astimezone(pytz.UTC)

        # Check if within working hours
        if not self._is_within_working_hours(utc_dt, timezone):
            return False

        # Here you would check against existing calendar events
        # For now, we'll just return True
        return True

    def _is_within_working_hours(self, dt, timezone):
        """
        Check if a datetime is within defined working hours.

        Args:
            dt (datetime): The datetime to check
            timezone (str): Timezone name

        Returns:
            bool: True if within working hours, False otherwise
        """
        local_dt = dt.astimezone(pytz.timezone(timezone))
        hour = local_dt.hour

        return (self.working_hours['start'] <= hour < self.working_hours['end'] and
                local_dt.weekday() < 5)  # Monday = 0, Sunday = 6

    def suggest_next_slot(self, meeting_type, timezone='UTC', start_from=None):
        """
        Suggest the next available time slot for a meeting.

        Args:
            meeting_type (str): Type of meeting to schedule
            timezone (str): Timezone name (default: 'UTC')
            start_from (datetime, optional): Starting datetime for the search

        Returns:
            datetime: Suggested meeting start time, or None if no slots available
        """
        if start_from is None:
            start_from = datetime.now(pytz.timezone(timezone))

        duration = self.meeting_durations.get(meeting_type, 60)
        current = start_from

        # Look for slots in the next 5 business days
        for _ in range(5):
            if current.weekday() >= 5:  # Skip weekends
                current += timedelta(days=1)
                continue

            # Try each hour during working hours
            for hour in range(self.working_hours['start'], self.working_hours['end']):
                slot_time = current.replace(
                    hour=hour, minute=0, second=0, microsecond=0)

                if slot_time < start_from:
                    continue

                if self.check_availability(slot_time.date(),
                                           slot_time.time(),
                                           duration,
                                           timezone):
                    return slot_time

            current += timedelta(days=1)

        return None  # No available slots found
