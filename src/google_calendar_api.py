#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Google Calendar API Integration Module
-------------------------------------
This module provides functions to interact with Google Calendar API
for the Work Schedule Agent system.
"""

import os
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

# In a real implementation, you would use the Google API client library
# For demonstration purposes, we're showing the structure
try:
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
except ImportError:
    print("Google API libraries not installed. Run: pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib")

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']


class GoogleCalendarManager:
    """Manager class for Google Calendar operations"""
    
    def __init__(self, credentials_file: str = 'credentials.json', token_file: str = 'token.json'):
        """Initialize the Google Calendar Manager
        
        Args:
            credentials_file: Path to the credentials.json file
            token_file: Path to the token.json file
        """
        self.credentials_file = credentials_file
        self.token_file = token_file
        self.service = self._get_calendar_service()
        
    def _get_calendar_service(self):
        """Get authenticated Google Calendar service
        
        Returns:
            Google Calendar service object
        """
        creds = None
        # The file token.json stores the user's access and refresh tokens
        if os.path.exists(self.token_file):
            creds = Credentials.from_authorized_user_info(
                json.load(open(self.token_file)), SCOPES)
                
        # If there are no valid credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(self.token_file, 'w') as token:
                token.write(creds.to_json())

        return build('calendar', 'v3', credentials=creds)
    
    def get_events(self, 
                  calendar_id: str = 'primary', 
                  time_min: Optional[datetime] = None,
                  time_max: Optional[datetime] = None,
                  max_results: int = 10) -> List[Dict[str, Any]]:
        """Get events from Google Calendar
        
        Args:
            calendar_id: Calendar ID to fetch events from
            time_min: Start time for events (defaults to now)
            time_max: End time for events (defaults to end of day)
            max_results: Maximum number of events to return
            
        Returns:
            List of event dictionaries
        """
        if time_min is None:
            time_min = datetime.utcnow()
            
        if time_max is None:
            time_max = time_min.replace(hour=23, minute=59, second=59)
            
        events_result = self.service.events().list(
            calendarId=calendar_id,
            timeMin=time_min.isoformat() + 'Z',
            timeMax=time_max.isoformat() + 'Z',
            maxResults=max_results,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        return events_result.get('items', [])
    
    def create_event(self, 
                    summary: str,
                    start_time: datetime,
                    end_time: datetime,
                    description: str = '',
                    location: str = '',
                    calendar_id: str = 'primary',
                    project_code: str = None) -> Dict[str, Any]:
        """Create a new event in Google Calendar
        
        Args:
            summary: Event title
            start_time: Event start time
            end_time: Event end time
            description: Event description
            location: Event location
            calendar_id: Calendar ID to create event in
            project_code: Project code for categorization (MAIN, SIDE, PORT)
            
        Returns:
            Created event dictionary
        """
        # Add project code to summary if provided
        if project_code:
            summary = f"[{project_code}] {summary}"
            
        event = {
            'summary': summary,
            'location': location,
            'description': description,
            'start': {
                'dateTime': start_time.isoformat(),
                'timeZone': 'UTC',
            },
            'end': {
                'dateTime': end_time.isoformat(),
                'timeZone': 'UTC',
            },
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'popup', 'minutes': 10},
                ],
            },
        }

        return self.service.events().insert(calendarId=calendar_id, body=event).execute()
    
    def update_event(self, 
                    event_id: str,
                    summary: str = None,
                    start_time: datetime = None,
                    end_time: datetime = None,
                    description: str = None,
                    location: str = None,
                    calendar_id: str = 'primary') -> Dict[str, Any]:
        """Update an existing event in Google Calendar
        
        Args:
            event_id: ID of the event to update
            summary: New event title (if None, keeps existing)
            start_time: New start time (if None, keeps existing)
            end_time: New end time (if None, keeps existing)
            description: New description (if None, keeps existing)
            location: New location (if None, keeps existing)
            calendar_id: Calendar ID containing the event
            
        Returns:
            Updated event dictionary
        """
        # Get the existing event
        event = self.service.events().get(calendarId=calendar_id, eventId=event_id).execute()
        
        # Update fields if provided
        if summary:
            event['summary'] = summary
        if description:
            event['description'] = description
        if location:
            event['location'] = location
        if start_time:
            event['start']['dateTime'] = start_time.isoformat()
        if end_time:
            event['end']['dateTime'] = end_time.isoformat()
            
        return self.service.events().update(calendarId=calendar_id, eventId=event_id, body=event).execute()
    
    def delete_event(self, event_id: str, calendar_id: str = 'primary') -> None:
        """Delete an event from Google Calendar
        
        Args:
            event_id: ID of the event to delete
            calendar_id: Calendar ID containing the event
        """
        self.service.events().delete(calendarId=calendar_id, eventId=event_id).execute()
        
    def create_work_blocks(self, 
                          date: datetime,
                          start_hour: int = 10,
                          end_hour: int = 18,
                          block_duration: int = 45,
                          break_duration: int = 15,
                          lunch_start: int = 12,
                          lunch_end: int = 13,
                          calendar_id: str = 'primary') -> List[Dict[str, Any]]:
        """Create work time blocks for a specific day
        
        Args:
            date: Date to create blocks for
            start_hour: Hour to start work blocks (24h format)
            end_hour: Hour to end work blocks (24h format)
            block_duration: Duration of each work block in minutes
            break_duration: Duration of breaks between blocks in minutes
            lunch_start: Hour to start lunch break (24h format)
            lunch_end: Hour to end lunch break (24h format)
            calendar_id: Calendar ID to create events in
            
        Returns:
            List of created event dictionaries
        """
        created_events = []
        current_time = date.replace(hour=start_hour, minute=0, second=0)
        end_time = date.replace(hour=end_hour, minute=0, second=0)
        
        while current_time < end_time:
            # Skip lunch time
            if current_time.hour == lunch_start and current_time.minute == 0:
                current_time = current_time.replace(hour=lunch_end, minute=0)
                continue
                
            # Calculate block end time
            block_end = current_time + timedelta(minutes=block_duration)
            
            # Create a work block
            event = self.create_event(
                summary="Focus Work Block",
                start_time=current_time,
                end_time=block_end,
                description="45-minute focused work session",
                calendar_id=calendar_id
            )
            created_events.append(event)
            
            # Move to next block (after break)
            current_time = block_end + timedelta(minutes=break_duration)
            
        return created_events
    
    def get_project_events(self, 
                          project_code: str,
                          time_min: Optional[datetime] = None,
                          time_max: Optional[datetime] = None,
                          calendar_id: str = 'primary') -> List[Dict[str, Any]]:
        """Get events for a specific project code
        
        Args:
            project_code: Project code to filter by (MAIN, SIDE, PORT)
            time_min: Start time for events (defaults to start of day)
            time_max: End time for events (defaults to end of day)
            calendar_id: Calendar ID to fetch events from
            
        Returns:
            List of event dictionaries for the specified project
        """
        if time_min is None:
            time_min = datetime.now().replace(hour=0, minute=0, second=0)
            
        if time_max is None:
            time_max = time_min.replace(hour=23, minute=59, second=59)
            
        events = self.get_events(
            calendar_id=calendar_id,
            time_min=time_min,
            time_max=time_max,
            max_results=100  # Increase to ensure we get all events
        )
        
        # Filter events by project code in summary
        project_events = [
            event for event in events 
            if event.get('summary', '').startswith(f'[{project_code}]')
        ]
        
        return project_events


def main():
    """Example usage of the GoogleCalendarManager class"""
    calendar = GoogleCalendarManager()
    
    # Get today's events
    today = datetime.now()
    events = calendar.get_events(time_min=today)
    
    print(f"Today's events ({len(events)}):")
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(f"{start} - {event['summary']}")
    
    # Create work blocks for tomorrow
    tomorrow = today + timedelta(days=1)
    print(f"\nCreating work blocks for {tomorrow.date()}...")
    blocks = calendar.create_work_blocks(date=tomorrow)
    print(f"Created {len(blocks)} work blocks")


if __name__ == '__main__':
    main()
