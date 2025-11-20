---
description: Convert existing tasks into actionable, dependency-ordered Linear issues for the feature based on available design artifacts.
tools: ['mcp__linear-server__create_issue', 'mcp__linear-server__list_teams', 'mcp__linear-server__list_projects', 'mcp__linear-server__list_issue_labels']
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

1. Run `.specify/scripts/bash/check-prerequisites.sh --json --require-tasks --include-tasks` from repo root and parse FEATURE_DIR and AVAILABLE_DOCS list. All paths must be absolute. For single quotes in args like "I'm Groot", use escape syntax: e.g 'I'\''m Groot' (or double-quote if possible: "I'm Groot").

2. From the executed script, extract the path to **tasks.md**.

3. Read the tasks.md file and parse all tasks, extracting:
   - Task ID (e.g., T001, T002)
   - Priority markers [P] for parallelizable tasks
   - Story labels (e.g., [US1], [US2])
   - Task description including file paths
   - Phase organization (Setup, Foundational, User Stories, Polish)

4. Get the Linear team for the project:
   - List available Linear teams using `mcp__linear-server__list_teams`
   - Identify the appropriate team (default: match repository name or use first team)
   - Store the team ID for issue creation

5. (Optional) Check for existing Linear project:
   - List projects using `mcp__linear-server__list_projects`
   - Check if a project exists for this feature
   - If not, ask user if they want to create a project or use team backlog

6. (Optional) Get available labels:
   - List issue labels using `mcp__linear-server__list_issue_labels`
   - Map task phases/types to appropriate labels (e.g., "setup", "foundational", user story labels)

7. Create Linear issues for each task:
   - Use `mcp__linear-server__create_issue` for each task in tasks.md
   - **Issue Title**: Use the task description (without the Task ID prefix)
   - **Issue Description**: Include:
     - Full task details from tasks.md
     - Task ID reference
     - Phase information
     - File paths involved
     - Link to related design artifacts if available
   - **Labels**: Apply appropriate labels based on:
     - Phase (setup, foundational, user-story, polish)
     - Story label (US1, US2, etc.)
     - Parallelizable marker [P]
   - **Team**: Use the team ID from step 4
   - **Project** (optional): Link to project if identified in step 5
   - **Priority** (optional): Map from task priorities if specified

8. Handle dependencies:
   - Add dependency information in issue descriptions
   - Use Linear's parent/child relationships for task hierarchies if applicable
   - Document execution order based on phases

9. Report summary:
   - Total issues created
   - Issues per phase/user story
   - Linear project/team used
   - Links to created issues (if available from API response)
