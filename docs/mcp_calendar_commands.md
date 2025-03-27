# MCP Calendar Commands Reference

This document provides a reference for Model Context Protocol (MCP) commands that can be used to interact with the Google Calendar Work Schedule Agent through AI assistants like Claude.

## Basic Commands

### Schedule Management

| Command | Description | Example |
|---------|-------------|---------|
| `/schedule_day` | Plan your daily schedule with optimized work blocks | `/schedule_day` |
| `/adjust [Reason]` | Adjust your schedule for a specific reason | `/adjust Need to attend unexpected meeting` |
| `/view_schedule [Date]` | View your schedule for a specific date | `/view_schedule 2025-03-15` |
| `/block_time [Project] [Duration]` | Block time for a specific project | `/block_time MAIN 2h` |

### Project Management

| Command | Description | Example |
|---------|-------------|---------|
| `/update [Project]` | Update project status | `/update SIDE` |
| `/project_list` | List all active projects | `/project_list` |
| `/project_status [Project]` | Get status of a specific project | `/project_status PORT` |
| `/add_project [Code] [Name]` | Add a new project | `/add_project BLOG Personal Blog` |

### Integration Commands

| Command | Description | Example |
|---------|-------------|---------|
| `/github_status` | Check GitHub project status | `/github_status` |
| `/github_commits [Repo]` | View recent commits for a repository | `/github_commits my-project` |
| `/notion_updates` | Get recent Notion updates | `/notion_updates` |
| `/notion_search [Query]` | Search Notion pages | `/notion_search project plan` |

### Analysis Commands

| Command | Description | Example |
|---------|-------------|---------|
| `/analyze_productivity [Days]` | Analyze productivity for a period | `/analyze_productivity 7` |
| `/suggest_focus` | Get recommendations for focus areas | `/suggest_focus` |
| `/time_distribution` | View time distribution across projects | `/time_distribution` |
| `/compare_weeks` | Compare productivity between weeks | `/compare_weeks` |

## Advanced Commands

### Planning and Review

| Command | Description | Example |
|---------|-------------|---------|
| `/morning_plan` | Generate a comprehensive morning plan | `/morning_plan` |
| `/evening_review` | Conduct an evening review session | `/evening_review` |
| `/weekly_plan` | Create a plan for the upcoming week | `/weekly_plan` |
| `/monthly_review` | Review the past month's productivity | `/monthly_review` |

### Goal Tracking

| Command | Description | Example |
|---------|-------------|---------|
| `/set_goal [Project] [Description]` | Set a goal for a project | `/set_goal PORT Complete portfolio website` |
| `/goal_status [Project]` | Check status of goals for a project | `/goal_status PORT` |
| `/goal_list` | List all active goals | `/goal_list` |
| `/complete_goal [Goal ID]` | Mark a goal as completed | `/complete_goal 12` |

### Log Management

| Command | Description | Example |
|---------|-------------|---------|
| `/create_log [Project] [Activity]` | Create a new log entry | `/create_log MAIN Completed API integration` |
| `/view_logs [Project] [Date]` | View logs for a project | `/view_logs MAIN 2025-03-14` |
| `/search_logs [Query]` | Search through log entries | `/search_logs meeting notes` |
| `/export_logs [Format]` | Export logs in specified format | `/export_logs markdown` |

### System Management

| Command | Description | Example |
|---------|-------------|---------|
| `/config_update [Setting] [Value]` | Update configuration setting | `/config_update work_hours.start 9` |
| `/sync_calendars` | Synchronize multiple calendars | `/sync_calendars` |
| `/backup_data` | Create a backup of all data | `/backup_data` |
| `/system_status` | Check system status and connections | `/system_status` |

## Command Parameters

### Time Formats

- **Date**: YYYY-MM-DD (e.g., 2025-03-15)
- **Time**: HH:MM (24-hour format, e.g., 14:30)
- **Duration**: Number followed by unit (h for hours, m for minutes, e.g., 2h30m)

### Project Codes

- **MAIN**: Main job tasks
- **SIDE**: Side job projects
- **PORT**: Portfolio preparation
- **FAM**: Family activities
- Custom codes as defined in your configuration

### Filter Parameters

- **Days**: Number of days to look back (e.g., 7)
- **Limit**: Maximum number of items to return (e.g., 5)
- **Sort**: Sorting order (e.g., date, priority)

## Using Commands in Context

Commands can be used within a conversation with your AI assistant. For example:

```
User: I need to plan my day tomorrow.
