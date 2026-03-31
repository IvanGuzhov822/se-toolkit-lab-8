---
name: lms
description: Use LMS MCP tools for live course data
always: true
---

# LMS Skill

Use LMS MCP tools to access live course data from the LMS backend.

## Available Tools

- `lms_health` - Check if the LMS backend is healthy and report the item count
- `lms_labs` - List all labs available in the LMS
- `lms_learners` - List all learners registered in the LMS
- `lms_pass_rates` - Get pass rates for a specific lab (requires lab parameter)
- `lms_timeline` - Get submission timeline for a specific lab (requires lab parameter)
- `lms_groups` - Get group performance for a specific lab (requires lab parameter)
- `lms_top_learners` - Get top learners by average score for a specific lab (requires lab parameter)
- `lms_completion_rate` - Get completion rate for a specific lab (requires lab parameter)
- `lms_sync_pipeline` - Trigger the LMS sync pipeline

## Strategy

### When user asks about labs, scores, pass rates, completion, groups, timeline, or top learners:

1. If the user did not specify a lab identifier:
   - Call `lms_labs` first to get the list of available labs
   - Use `mcp_webchat_ui_message` with `type: "choice"` to let the user select a lab
   - Provide each lab's `id` as the value and `title` as the label
   - If UI choice is not available on the channel, ask in plain text which lab they want

2. If the user specified a lab:
   - Call the appropriate tool directly with the lab identifier

### When user asks "what can you do?":

Explain that you can:
- Check LMS backend health
- List available labs and learners
- Show pass rates, completion rates, timelines, and group performance for specific labs
- Identify top learners per lab
- Trigger the LMS sync pipeline

### Response formatting:

- Format percentages with the % symbol
- Format counts as plain numbers
- Keep responses concise
- Include relevant lab titles when presenting results

### Error handling:

- If a tool fails, explain the error clearly and suggest retrying or checking backend health
- If no labs are available, suggest triggering the sync pipeline first
