# Example Prompts for Google Calendar Work Schedule Agent

This document provides example prompts in both Korean and English for interacting with the Google Calendar Work Schedule Agent through AI assistants like Claude.

## Morning Planning Session Prompts

### English

```
I'd like to plan my day using the Google Calendar Work Schedule Agent. Please help me with the following:

1. Check my calendar for today's existing appointments
2. Review my GitHub activity from yesterday for repositories: [REPO_NAMES]
3. Check for any recent updates in my Notion workspace
4. Based on this information, suggest a schedule for today with appropriate time blocks
5. Prioritize my tasks based on upcoming deadlines and project status
6. Create the schedule in my Google Calendar

My current priorities are:
- [PRIORITY_1]
- [PRIORITY_2]
- [PRIORITY_3]

Please use the /schedule_day and /suggest_focus commands to help organize my day.
```

### Korean

```
Google Calendar Work Schedule Agent를 사용하여 오늘 하루를 계획하고 싶습니다. 다음 사항들을 도와주세요:

1. 오늘의 기존 일정 확인
2. 어제의 GitHub 활동 검토 (저장소: [REPO_NAMES])
3. Notion 워크스페이스의 최근 업데이트 확인
4. 이 정보를 바탕으로 적절한 시간 블록으로 오늘의 일정 제안
5. 다가오는 마감일과 프로젝트 상태에 따라 작업 우선순위 지정
6. Google 캘린더에 일정 생성

현재 우선순위는 다음과 같습니다:
- [PRIORITY_1]
- [PRIORITY_2]
- [PRIORITY_3]

/schedule_day와 /suggest_focus 명령어를 사용하여 하루 일정을 구성해 주세요.
```

## Evening Review Session Prompts

### English

```
I'd like to review my day and prepare for tomorrow using the Google Calendar Work Schedule Agent. Please help me with:

1. Analyze how I spent my time today across different projects
2. Check which scheduled tasks were completed
3. Review my GitHub commits and activity for today
4. Check any Notion updates I made today
5. Evaluate my productivity and suggest improvements
6. Prepare an initial schedule for tomorrow

Please use the /analyze_productivity and /evening_review commands to generate insights, and then use /schedule_day to prepare tomorrow's schedule.
```

### Korean

```
Google Calendar Work Schedule Agent를 사용하여 오늘을 리뷰하고 내일을 준비하고 싶습니다. 다음 사항들을 도와주세요:

1. 오늘 다양한 프로젝트에 시간을 어떻게 사용했는지 분석
2. 예정된 작업 중 완료된 항목 확인
3. 오늘의 GitHub 커밋 및 활동 검토
4. 오늘 작성한 Notion 업데이트 확인
5. 생산성 평가 및 개선점 제안
6. 내일의 초기 일정 준비

/analyze_productivity와 /evening_review 명령어를 사용하여 인사이트를 생성하고, /schedule_day를 사용하여 내일 일정을 준비해 주세요.
```

## Project Status Update Prompts

### English

```
I need to update the status of my [PROJECT_CODE] project. Please help me with the following:

1. Check the current status of this project in my GitHub repository [REPO_NAME]
2. Review the related Notion pages for this project
3. Analyze how much time I've allocated to this project in the past week
4. Update my project log with the current progress
5. Adjust upcoming calendar events related to this project based on the current status
6. Suggest next steps and priorities

Please use the /project_status, /github_status, and /notion_updates commands to gather information, and then use /update [PROJECT_CODE] to record the update.
```

### Korean

```
[PROJECT_CODE] 프로젝트의 상태를 업데이트해야 합니다. 다음 사항들을 도와주세요:

1. GitHub 저장소 [REPO_NAME]에서 이 프로젝트의 현재 상태 확인
2. 이 프로젝트와 관련된 Notion 페이지 검토
3. 지난 주에 이 프로젝트에 할당한 시간 분석
4. 현재 진행 상황으로 프로젝트 로그 업데이트
5. 현재 상태에 기반하여 이 프로젝트와 관련된 향후 캘린더 일정 조정
6. 다음 단계 및 우선순위 제안

/project_status, /github_status, /notion_updates 명령어를 사용하여 정보를 수집하고, /update [PROJECT_CODE]를 사용하여 업데이트를 기록해 주세요.
```

## Schedule Adjustment Prompts

### English

```
I need to adjust my schedule for today due to [REASON]. Please help me with:

1. Review my current calendar for today
2. Identify which tasks can be rescheduled or shortened
3. Prioritize the most important tasks that must be completed today
4. Create a revised schedule that accommodates [NEW_REQUIREMENT]
5. Update my Google Calendar with the changes
6. Adjust my project logs to reflect these changes

Please use the /view_schedule command to check my current schedule and /adjust [REASON] to make the necessary changes.
```

### Korean

```
[REASON] 때문에 오늘 일정을 조정해야 합니다. 다음 사항들을 도와주세요:

1. 오늘의 현재 캘린더 검토
2. 일정 변경이 가능하거나 단축할 수 있는 작업 식별
3. 오늘 반드시 완료해야 하는 가장 중요한 작업 우선순위 지정
4. [NEW_REQUIREMENT]를 수용하는 수정된 일정 생성
5. 변경 사항으로 Google 캘린더 업데이트
6. 이러한 변경 사항을 반영하도록 프로젝트 로그 조정

/view_schedule 명령어를 사용하여 현재 일정을 확인하고 /adjust [REASON] 명령어를 사용하여 필요한 변경을 수행해 주세요.
```

## Productivity Analysis Prompts

### English

```
I'd like to analyze my productivity patterns over the past [NUMBER] weeks. Please help me understand:

1. How I've distributed my time across different project categories (MAIN, SIDE, PORT)
2. Which days and times I've been most productive
3. The correlation between my GitHub activity and scheduled work blocks
4. How my Notion documentation has evolved during this period
5. Whether I'm making progress towards my stated goals
6. Areas where I could improve my time management

Please use the /analyze_productivity [NUMBER] and /time_distribution commands to generate this analysis.
```

### Korean

```
지난 [NUMBER]주 동안의 생산성 패턴을 분석하고 싶습니다. 다음 사항들을 이해하는 데 도움을 주세요:

1. 다양한 프로젝트 카테고리(MAIN, SIDE, PORT)에 시간을 어떻게 분배했는지
2. 어떤 날짜와 시간에 가장 생산적이었는지
3. GitHub 활동과 예약된 작업 블록 간의 상관관계
4. 이 기간 동안 Notion 문서가 어떻게 발전했는지
5. 명시된 목표를 향해 진전을 이루고 있는지
6. 시간 관리를 개선할 수 있는 영역

/analyze_productivity [NUMBER]와 /time_distribution 명령어를 사용하여 이 분석을 생성해 주세요.
```

## Weekly Planning Prompts

### English

```
I need to plan my upcoming week with a focus on balancing my main job, side projects, and portfolio work. Please help me:

1. Review my calendar for the upcoming week to identify existing commitments
2. Check the status of all my active projects on GitHub
3. Review important Notion documents that need attention
4. Create a balanced weekly schedule with appropriate time blocks for each project category
5. Ensure I'm making progress on all priority projects
6. Include buffer time for unexpected tasks

Please use the /weekly_plan command to generate a comprehensive plan for the week.
```

### Korean

```
주요 업무, 사이드 프로젝트 및 포트폴리오 작업의 균형을 맞추는 데 중점을 두고 다가오는 주를 계획해야 합니다. 다음 사항들을 도와주세요:

1. 다가오는 주의 캘린더를 검토하여 기존 약속 확인
2. GitHub의 모든 활성 프로젝트 상태 확인
3. 주의가 필요한 중요한 Notion 문서 검토
4. 각 프로젝트 카테고리에 적절한 시간 블록이 있는 균형 잡힌 주간 일정 생성
5. 모든 우선순위 프로젝트에서 진전을 이루고 있는지 확인
6. 예상치 못한 작업을 위한 버퍼 시간 포함

/weekly_plan 명령어를 사용하여 주간 종합 계획을 생성해 주세요.
```

## Goal Setting Prompts

### English

```
I want to set goals for my [PROJECT_CODE] project for the next month. Please help me:

1. Review the current status of this project
2. Check my GitHub repository for outstanding issues and milestones
3. Review related Notion documents for requirements and ideas
4. Suggest realistic goals based on my available time and current commitments
5. Create a timeline with milestones for achieving these goals
6. Set up tracking mechanisms to monitor progress

Please use the /project_status [PROJECT_CODE] command to check the current status and /set_goal [PROJECT_CODE] to create new goals.
```

### Korean

```
다음 달 [PROJECT_CODE] 프로젝트에 대한 목표를 설정하고 싶습니다. 다음 사항들을 도와주세요:

1. 이 프로젝트의 현재 상태 검토
2. 미해결 이슈 및 마일스톤에 대한 GitHub 저장소 확인
3. 요구 사항 및 아이디어에 대한 관련 Notion 문서 검토
4. 가용 시간 및 현재 약속을 기반으로 현실적인 목표 제안
5. 이러한 목표 달성을 위한 마일스톤이 있는 타임라인 생성
6. 진행 상황을 모니터링하기 위한 추적 메커니즘 설정

/project_status [PROJECT_CODE] 명령어를 사용하여 현재 상태를 확인하고 /set_goal [PROJECT_CODE]를 사용하여 새 목표를 생성해 주세요.
```

## Log Creation Prompts

### English

```
I need to create a detailed log entry for my work on [PROJECT_CODE] today. Please help me:

1. Summarize what I accomplished today on this project
2. Include references to any GitHub commits or pull requests
3. Link to relevant Notion pages that were created or updated
4. Note any challenges encountered and how they were addressed
5. Record time spent on different aspects of the project
6. Identify next steps for tomorrow

Please use the /create_log [PROJECT_CODE] command to generate this log entry.
```

### Korean

```
오늘 [PROJECT_CODE]에 대한 작업에 대해 상세한 로그 항목을 생성해야 합니다. 다음 사항들을 도와주세요:

1. 오늘 이 프로젝트에서 완료한 작업 요약
2. GitHub 커밋이나 풀 리퀘스트에 대한 참조 포함
3. 생성되거나 업데이트된 관련 Notion 페이지 링크
4. 발생한 문제점과 해결 방법 기록
5. 프로젝트의 다양한 측면에 소요된 시간 기록
6. 내일을 위한 다음 단계 식별

/create_log [PROJECT_CODE] 명령어를 사용하여 이 로그 항목을 생성해 주세요.
```
