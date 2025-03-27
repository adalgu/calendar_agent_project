# Google Calendar Work Schedule Agent

This repository contains a comprehensive system for managing your work schedule using Google Calendar and MCP (Model Context Protocol) integration. It's designed to help you efficiently manage your main job, side projects, and portfolio preparation while maintaining privacy through anonymized project naming.

## Repository Structure

- **[google_calendar_agent_guide.md](docs/google_calendar_agent_guide.md)**: The main guide that explains the entire system, including work schedule framework, project management, logging system, and agent interaction.

- **[log_index.md](docs/log_index.md)**: A master index of all project activities, serving as the central reference for project status and history.

- **[logs/](logs/)**: Directory containing detailed log files for each project activity.

  - Example: [logs/MAIN-01-20250314.md](logs/MAIN-01-20250314.md)

- **[calendar_integration_example.js](src/calendar_integration_example.js)**: Example JavaScript code demonstrating how to programmatically interact with Google Calendar using the MCP tools.

- **[mcp_calendar_commands.md](docs/mcp_calendar_commands.md)**: Reference for direct MCP commands to interact with Google Calendar.
- **[example_prompts.md](docs/example_prompts.md)**: Example prompts in Korean and English for interacting with the agent.

## Getting Started

1. Read the [google_calendar_agent_guide.md](docs/google_calendar_agent_guide.md) to understand the system's structure and philosophy.

2. Review the example log files to understand the logging format.

3. Familiarize yourself with the MCP commands in [mcp_calendar_commands.md](docs/mcp_calendar_commands.md).
4. Review the example prompts in [example_prompts.md](docs/example_prompts.md) for interacting with the agent.

5. Start using the system by:
   - Creating logs for your active projects
   - Using the MCP commands to interact with your Google Calendar
   - Following the time slot structure for optimal productivity

## Work Schedule Framework

- **Regular Hours**: 10:00 AM - 6:00 PM
- **Lunch Break**: 12:00 PM - 1:30 PM
- **Time Slots**: 45 minutes of focused work + 15 minutes break per hour

## Project Management

Projects are categorized and anonymized using codes:

- **MAIN**: Main job tasks
- **SIDE**: Side job projects
- **PORT**: Portfolio preparation

## Agent Interaction

The system is designed to work with Claude or other AI assistants through MCP. Key commands include:

- `/schedule_day`: Plan your daily schedule
- `/update [Project]`: Update project status
- `/adjust [Reason]`: Handle schedule changes

## Customization

Feel free to customize this system to fit your specific needs:

- Adjust the time slot structure
- Modify the project categories
- Expand the logging format
- Add additional MCP integrations

## Privacy Considerations

This system is designed with privacy in mind:

- Projects are referenced by code names
- Sensitive details can be omitted from logs
- Calendar events use generic titles with project codes

## Implementation

The repository includes Python modules for integration with:

- Google Calendar API (`src/google_calendar_api.py`)
- GitHub API (`src/github_api.py`)
- Notion API with token optimization (`src/notion_api.py`)
- Main agent module (`src/work_schedule_agent.py`)

To install dependencies:
```
pip install -r requirements.txt
```

---

For detailed instructions on using each component, refer to the specific documentation files listed above.
