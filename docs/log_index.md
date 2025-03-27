# Activity Log Index

This document serves as a master index of all project activities, providing a central reference for project status and history.

## Log Structure

Each log file follows a standardized naming convention:
`[PROJECT_CODE]-[SEQUENCE_NUMBER]-[DATE].md`

For example: `MAIN-01-20250314.md`

## Recent Logs

| Date | Project | Activity | Log File |
|------|---------|----------|----------|
| 2025-03-14 | MAIN | API Integration | [MAIN-01-20250314.md](../logs/MAIN-01-20250314.md) |
| 2025-03-14 | SIDE | Feature Development | [SIDE-01-20250314.md](../logs/SIDE-01-20250314.md) |
| 2025-03-14 | PORT | Portfolio Update | [PORT-01-20250314.md](../logs/PORT-01-20250314.md) |

## Log Categories

### Main Job Tasks (MAIN)

Main job tasks are tracked with the `MAIN` prefix. These logs contain information about:
- Daily work activities
- Meeting notes
- Task completions
- Blockers and challenges

### Side Projects (SIDE)

Side projects are tracked with the `SIDE` prefix. These logs contain information about:
- Feature development
- Bug fixes
- Client communications
- Project milestones

### Portfolio Preparation (PORT)

Portfolio work is tracked with the `PORT` prefix. These logs contain information about:
- Portfolio updates
- Skill development
- Project documentation
- Learning resources

### Family Activities (FAM)

Family activities are tracked with the `FAM` prefix. These logs contain information about:
- Family events
- Personal appointments
- Health and wellness activities
- Home management tasks

## Log Format

Each log file contains the following sections:

1. **Header**: Date, project code, and activity title
2. **Summary**: Brief overview of the activity
3. **Details**: Comprehensive description of work performed
4. **Time Tracking**: Hours spent on different aspects
5. **References**: Links to relevant resources (GitHub, Notion)
6. **Next Steps**: Planned follow-up activities

## Using the Logs

### For Daily Planning

Review recent logs to:
- Track ongoing projects
- Identify unfinished tasks
- Understand current priorities
- Maintain context between work sessions

### For Productivity Analysis

Analyze logs over time to:
- Identify patterns in productivity
- Track time allocation across projects
- Measure progress toward goals
- Optimize work schedules

### For Project Management

Use logs to:
- Document project history
- Track decision-making processes
- Maintain accountability
- Share progress with stakeholders

## Automated Log Management

The Work Schedule Agent provides commands for log management:

- `/create_log [PROJECT] [ACTIVITY]`: Create a new log entry
- `/view_logs [PROJECT] [DATE]`: View logs for a project
- `/search_logs [QUERY]`: Search through log entries
- `/export_logs [FORMAT]`: Export logs in specified format

## Example Log Entry

```markdown
# MAIN-01-20250314: API Integration

## Summary
Completed the integration of the payment processing API with the main application.

## Details
- Implemented OAuth2 authentication flow
- Created service classes for API interaction
- Added error handling and retry logic
- Wrote unit tests for the integration
- Updated documentation

## Time Tracking
- API Implementation: 3.5 hours
- Testing: 1.5 hours
- Documentation: 1 hour
- Total: 6 hours

## References
- GitHub: [PR #123](https://github.com/example/repo/pull/123)
- Notion: [API Integration Spec](https://notion.so/workspace/api-spec)

## Next Steps
- Monitor API performance in staging environment
- Implement additional payment methods
- Review security considerations with the team
```
