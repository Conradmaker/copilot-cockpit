---
name: file-creator
description: Creates files for memory context management system - droids, commands, templates, and documentation
---

# File Creator

NOTE: Startup and cleanup are handled by `worker-base`. This skill defines the WORK PROCEDURE.

## When to Use This Skill

This skill is used for creating files in the memory context management system:
- Custom droid files
- Slash command files
- Memory template files
- Documentation updates

## Work Procedure

1. **Read feature description** to understand what file to create and where
2. **Create the file** with appropriate content:
   - For droids: YAML frontmatter (name, description, model, tools) + prompt body
   - For commands: YAML frontmatter (description, argument-hint) + prompt body
   - For templates: Markdown with proper category sections
   - For docs: Markdown with appropriate sections
3. **Verify file creation** by reading the file back
4. **Run any available validation** (e.g., check YAML frontmatter validity)

## Example Handoff

```json
{
  "salientSummary": "Created memory-synthesizer.md at ~/.factory/droids/ with low-cost model configuration and proper prompt for analyzing session context.",
  "whatWasImplemented": "Created ~/.factory/droids/memory-synthesizer.md with YAML frontmatter specifying claude-3-5-haiku-latest model and tools: ['Read', 'Edit', 'Create']. The prompt instructs the droid to analyze session context, categorize items as personal or project memory, and prompt user for confirmation before saving.",
  "whatWasLeftUndone": "",
  "verification": {
    "commandsRun": [
      {
        "command": "cat ~/.factory/droids/memory-synthesizer.md",
        "exitCode": 0,
        "observation": "File exists with valid YAML frontmatter and prompt body"
      }
    ],
    "interactiveChecks": []
  },
  "tests": {
    "added": []
  },
  "discoveredIssues": []
}
```

## When to Return to Orchestrator

- Target directory does not exist and cannot be created
- File already exists with different content than expected
- Required template structure is unclear from feature description
