#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Work Schedule Agent
------------------
Main module that integrates Google Calendar, GitHub, and Notion
to create a comprehensive work schedule management system.
"""

import os
import json
import argparse
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

# Import API modules
from google_calendar_api import GoogleCalendarManager
from github_api import GitHubManager
from notion_api import NotionManager


class WorkScheduleAgent:
    """Main agent class that integrates all services"""
    
    def __init__(self, config_file: str = 'config.json'):
        """Initialize the Work Schedule Agent
        
        Args:
            config_file: Path to configuration file
        """
        self.config = self._load_config(config_file)
        self.calendar = GoogleCalendarManager()
        self.github = GitHubManager()
        
        # Only initialize Notion if token is available
        self.notion = None
        if os.environ.get('NOTION_TOKEN'):
            self.notion = NotionManager()
            
        # Create logs directory if it doesn't exist
        os.makedirs('logs', exist_ok=True)
        
    def _load_config(self, config_file: str) -> Dict[str, Any]:
        """Load configuration from file
        
        Args:
            config_file: Path to configuration file
            
        Returns:
            Configuration dictionary
        """
        default_config = {
            'work_hours': {
                'start': 10,
                'end': 18,
                'lunch_start': 12,
                'lunch_end': 13
            },
            'time_blocks': {
                'work_duration': 45,
                'break_duration': 15
            },
            'projects': {
                'MAIN': 'Main job tasks',
                'SIDE': 'Side job projects',
                'PORT': 'Portfolio preparation',
                'FAM': 'Family activities'
            },
            'github': {
                'username': '',
                'repositories': []
            },
            'notion': {
                'databases': []
            }
        }
        
        # Try to load from file
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                loaded_config = json.load(f)
                # Merge with default config
                for key, value in loaded_config.items():
                    if key in default_config and isinstance(value, dict):
                        default_config[key].update(value)
                    else:
                        default_config[key] = value
        else:
            # Save default config
            with open(config_file, 'w') as f:
                json.dump(default_config, f, indent=2)
                
        return default_config
    
    def schedule_day(self, date: Optional[datetime] = None) -> Dict[str, Any]:
        """Schedule a day based on current projects and priorities
        
        Args:
            date: Date to schedule (defaults to tomorrow)
            
        Returns:
            Dictionary with scheduled events
        """
        if date is None:
            date = datetime.now() + timedelta(days=1)
            
        # Get work hours from config
        work_hours = self.config.get('work_hours', {})
        start_hour = work_hours.get('start', 10)
        end_hour = work_hours.get('end', 18)
        lunch_start = work_hours.get('lunch_start', 12)
        lunch_end = work_hours.get('lunch_end', 13)
        
        # Get time block settings
        time_blocks = self.config.get('time_blocks', {})
        work_duration = time_blocks.get('work_duration', 45)
        break_duration = time_blocks.get('break_duration', 15)
        
        # Create work blocks
        events = self.calendar.create_work_blocks(
            date=date,
            start_hour=start_hour,
            end_hour=end_hour,
            block_duration=work_duration,
            break_duration=break_duration,
            lunch_start=lunch_start,
            lunch_end=lunch_end
        )
        
        # Log the scheduled day
        log_entry = {
            'date': date.strftime('%Y-%m-%d'),
            'events': [
                {
                    'summary': event.get('summary', ''),
                    'start': event.get('start', {}).get('dateTime', ''),
                    'end': event.get('end', {}).get('dateTime', '')
                }
                for event in events
            ]
        }
        
        self._log_activity('schedule_day', log_entry)
        
        return {
            'date': date.strftime('%Y-%m-%d'),
            'events_created': len(events)
        }
    
    def get_github_status(self) -> Dict[str, Any]:
        """Get GitHub status for configured repositories
        
        Returns:
            Dictionary with GitHub status
        """
        github_config = self.config.get('github', {})
        username = github_config.get('username', '')
        repositories = github_config.get('repositories', [])
        
        if not username:
            return {'error': 'GitHub username not configured'}
            
        # Get user activity
        activity = self.github.get_user_activity(username)
        
        # Get status for specific repositories
        repo_status = {}
        for repo in repositories:
            if '/' in repo:
                owner, repo_name = repo.split('/')
            else:
                owner, repo_name = username, repo
                
            status = self.github.get_project_status(owner, repo_name)
            repo_status[repo] = status
            
        # Log the GitHub status
        log_entry = {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'username': username,
            'activity': activity,
            'repositories': list(repo_status.keys())
        }
        
        self._log_activity('github_status', log_entry)
        
        return {
            'activity': activity,
            'repositories': repo_status
        }
    
    def get_notion_updates(self, days: int = 7) -> Dict[str, Any]:
        """Get recent Notion updates
        
        Args:
            days: Number of days to look back
            
        Returns:
            Dictionary with Notion updates
        """
        if not self.notion:
            return {'error': 'Notion API not configured'}
            
        # Get recently updated pages
        recent_pages = self.notion.get_recently_updated_pages(days)
        
        # Generate summaries for recent pages
        page_summaries = {}
        for page in recent_pages[:5]:  # Limit to 5 pages to avoid excessive API calls
            page_id = page.get('id')
            summary = self.notion.generate_page_summary(page_id)
            page_summaries[page_id] = {
                'title': page.get('title', ''),
                'url': page.get('url', ''),
                'summary': summary
            }
            
        # Log the Notion updates
        log_entry = {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'days_back': days,
            'pages_updated': len(recent_pages),
            'summaries_generated': len(page_summaries)
        }
        
        self._log_activity('notion_updates', log_entry)
        
        return {
            'recent_pages': recent_pages,
            'summaries': page_summaries
        }
    
    def analyze_productivity(self, days: int = 7) -> Dict[str, Any]:
        """Analyze productivity based on calendar events and project activity
        
        Args:
            days: Number of days to analyze
            
        Returns:
            Dictionary with productivity analysis
        """
        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # Get calendar events for the period
        events = self.calendar.get_events(
            time_min=start_date,
            time_max=end_date,
            max_results=100
        )
        
        # Categorize events by project code
        project_events = {}
        for project_code in self.config.get('projects', {}).keys():
            project_events[project_code] = self.calendar.get_project_events(
                project_code=project_code,
                time_min=start_date,
                time_max=end_date
            )
            
        # Calculate time spent on each project
        project_time = {}
        for code, events in project_events.items():
            total_minutes = 0
            for event in events:
                start = event.get('start', {}).get('dateTime', '')
                end = event.get('end', {}).get('dateTime', '')
                
                if start and end:
                    start_time = datetime.fromisoformat(start.replace('Z', '+00:00'))
                    end_time = datetime.fromisoformat(end.replace('Z', '+00:00'))
                    duration = (end_time - start_time).total_seconds() / 60
                    total_minutes += duration
                    
            project_time[code] = {
                'total_minutes': total_minutes,
                'total_hours': round(total_minutes / 60, 1),
                'events_count': len(events)
            }
            
        # Get GitHub activity if configured
        github_activity = None
        github_config = self.config.get('github', {})
        username = github_config.get('username', '')
        
        if username:
            github_activity = self.github.get_user_activity(username, since_days=days)
            
        # Log the productivity analysis
        log_entry = {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'days_analyzed': days,
            'project_time': project_time
        }
        
        self._log_activity('productivity_analysis', log_entry)
        
        return {
            'period': f"{start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}",
            'total_events': len(events),
            'project_time': project_time,
            'github_activity': github_activity
        }
    
    def suggest_focus(self) -> Dict[str, Any]:
        """Suggest focus areas based on recent activity and upcoming deadlines
        
        Returns:
            Dictionary with focus suggestions
        """
        # Get today's date
        today = datetime.now()
        
        # Get upcoming events (next 7 days)
        upcoming_events = self.calendar.get_events(
            time_min=today,
            time_max=today + timedelta(days=7),
            max_results=50
        )
        
        # Look for events with "deadline" or "due" in the title
        upcoming_deadlines = []
        for event in upcoming_events:
            summary = event.get('summary', '').lower()
            if 'deadline' in summary or 'due' in summary:
                upcoming_deadlines.append({
                    'summary': event.get('summary', ''),
                    'date': event.get('start', {}).get('dateTime', 
                           event.get('start', {}).get('date', '')),
                    'days_left': (datetime.fromisoformat(
                        event.get('start', {}).get('dateTime', 
                        event.get('start', {}).get('date', '')).split('T')[0]
                    ) - today.date()).days
                })
                
        # Get recent productivity analysis
        productivity = self.analyze_productivity(days=7)
        project_time = productivity.get('project_time', {})
        
        # Identify underserved projects (less than 4 hours in the last week)
        underserved_projects = []
        for code, time_data in project_time.items():
            if time_data.get('total_hours', 0) < 4:
                underserved_projects.append({
                    'code': code,
                    'name': self.config.get('projects', {}).get(code, ''),
                    'hours_last_week': time_data.get('total_hours', 0)
                })
                
        # Generate suggestions
        suggestions = []
        
        # Suggest focusing on imminent deadlines
        for deadline in sorted(upcoming_deadlines, key=lambda x: x.get('days_left', 0)):
            if deadline.get('days_left', 0) <= 3:  # Imminent deadlines (3 days or less)
                suggestions.append({
                    'priority': 'high',
                    'type': 'deadline',
                    'description': f"Focus on {deadline.get('summary')} due in {deadline.get('days_left')} days"
                })
                
        # Suggest focusing on underserved projects
        for project in underserved_projects:
            suggestions.append({
                'priority': 'medium',
                'type': 'underserved_project',
                'description': f"Allocate more time to {project.get('name')} ({project.get('code')}), only {project.get('hours_last_week')} hours last week"
            })
            
        # Log the focus suggestions
        log_entry = {
            'date': today.strftime('%Y-%m-%d'),
            'upcoming_deadlines': len(upcoming_deadlines),
            'underserved_projects': len(underserved_projects),
            'suggestions': len(suggestions)
        }
        
        self._log_activity('focus_suggestions', log_entry)
        
        return {
            'date': today.strftime('%Y-%m-%d'),
            'upcoming_deadlines': upcoming_deadlines,
            'underserved_projects': underserved_projects,
            'suggestions': suggestions
        }
    
    def _log_activity(self, activity_type: str, data: Dict[str, Any]) -> None:
        """Log agent activity
        
        Args:
            activity_type: Type of activity
            data: Activity data
        """
        today = datetime.now().strftime('%Y%m%d')
        log_file = f"logs/{activity_type}_{today}.json"
        
        # Create or append to log file
        if os.path.exists(log_file):
            with open(log_file, 'r') as f:
                logs = json.load(f)
                if isinstance(logs, list):
                    logs.append(data)
                else:
                    logs = [logs, data]
        else:
            logs = [data]
            
        with open(log_file, 'w') as f:
            json.dump(logs, f, indent=2)
            
        # Update log index
        self._update_log_index(activity_type, log_file)
    
    def _update_log_index(self, activity_type: str, log_file: str) -> None:
        """Update the log index file
        
        Args:
            activity_type: Type of activity
            log_file: Path to log file
        """
        index_file = 'log_index.md'
        today = datetime.now().strftime('%Y-%m-%d')
        
        # Create index file if it doesn't exist
        if not os.path.exists(index_file):
            with open(index_file, 'w') as f:
                f.write("# Activity Log Index\n\n")
                f.write("| Date | Activity Type | Log File |\n")
                f.write("|------|--------------|----------|\n")
                
        # Add entry to index
        with open(index_file, 'a') as f:
            f.write(f"| {today} | {activity_type} | [{log_file}]({log_file}) |\n")


def main():
    """Main function to run the Work Schedule Agent"""
    parser = argparse.ArgumentParser(description='Work Schedule Agent')
    parser.add_argument('command', choices=[
        'schedule_day', 'github_status', 'notion_updates', 
        'analyze_productivity', 'suggest_focus'
    ], help='Command to execute')
    parser.add_argument('--days', type=int, default=7, help='Number of days for analysis')
    parser.add_argument('--config', type=str, default='config.json', help='Path to config file')
    
    args = parser.parse_args()
    
    # Initialize agent
    agent = WorkScheduleAgent(config_file=args.config)
    
    # Execute command
    if args.command == 'schedule_day':
        result = agent.schedule_day()
        print(f"Scheduled day: {result.get('date')}")
        print(f"Created {result.get('events_created')} events")
        
    elif args.command == 'github_status':
        result = agent.get_github_status()
        if 'error' in result:
            print(f"Error: {result.get('error')}")
        else:
            activity = result.get('activity', {})
            print(f"GitHub activity for {activity.get('username')}:")
            print(f"Total commits: {activity.get('total_commits', 0)}")
            print(f"Total issues opened: {activity.get('total_issues_opened', 0)}")
            print(f"Total PRs: {activity.get('total_prs', 0)}")
            
    elif args.command == 'notion_updates':
        result = agent.get_notion_updates(days=args.days)
        if 'error' in result:
            print(f"Error: {result.get('error')}")
        else:
            recent_pages = result.get('recent_pages', [])
            print(f"Found {len(recent_pages)} recently updated Notion pages")
            for i, page in enumerate(recent_pages[:5]):
                print(f"{i+1}. {page.get('title', 'Untitled')}")
                
    elif args.command == 'analyze_productivity':
        result = agent.analyze_productivity(days=args.days)
        print(f"Productivity analysis for {result.get('period')}:")
        for code, data in result.get('project_time', {}).items():
            print(f"{code}: {data.get('total_hours')} hours ({data.get('events_count')} events)")
            
    elif args.command == 'suggest_focus':
        result = agent.suggest_focus()
        print("Focus suggestions:")
        for suggestion in result.get('suggestions', []):
            print(f"[{suggestion.get('priority', '').upper()}] {suggestion.get('description')}")


if __name__ == '__main__':
    main()
