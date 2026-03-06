# User Testing Guide: Memory Context Management System

This document captures testing knowledge, tools, and procedures for validating the memory-system milestone.

## Overview

The memory-system milestone provides a context management system that automatically records user preferences and project context. It consists of:

1. **memory-synthesizer droid** - Analyzes session context and categorizes memory items
2. **/save-memory command** - Invokes the droid from any directory
3. **Memory files** - Personal (`~/.factory/memories.md`) and Project (`.factory/memories.md`)
4. **AGENTS.md integration** - Guide for orchestrator memory capture behavior

## Testing Approach

This system is tested through **file system inspection** and **functional invocation tests** rather than traditional UI/API testing.

### Testing Surfaces

1. **File System** - Direct file existence and content verification
2. **Droid Invocation** - Testing the memory-synthesizer via Task tool
3. **Command Execution** - Testing /save-memory command functionality

## Flow Validator Guidance: File System Testing

### Isolation Strategy

File system tests are **naturally isolated** as they operate on specific paths. Each assertion can be tested independently:

- **DROID assertions** (`VAL-DROID-*`): Test droid behavior via Task invocation
- **CMD assertions** (`VAL-CMD-*`): Test command file and invocation
- **FILE assertions** (`VAL-FILE-*`): Direct file existence and content checks
- **AGENTS assertions** (`VAL-AGENTS-*`): Documentation content verification

### Shared State to Avoid

- Do NOT modify production memory files during testing
- Use temporary test memory files if testing write operations
- Do NOT delete or overwrite existing memory files

### Resources Off-Limits

- Real user memory files in `~/.factory/memories.md`
- Real project memory files in actual projects

## Environment Setup

### Prerequisites

No services need to be started for this milestone. The system operates through:
- Factory CLI for droid invocation
- File system for memory storage

### Required Files (Pre-created by implementation features)

1. `~/.factory/droids/memory-synthesizer.md` - Droid definition
2. `~/.factory/commands/save-memory.md` - Slash command
3. `~/.factory/memories.md` - Personal memory template
4. `.factory/memories.md` - Project memory template (in repo root)
5. `AGENTS.md` - Memory capture guide

## Assertion Testing Matrix

| Assertion ID | Area | Testing Method | Description |
|--------------|------|----------------|-------------|
| VAL-DROID-001 | DROID | File check | Droid file exists |
| VAL-DROID-002 | DROID | Content check | Uses low-cost model (claude-3-5-haiku-latest) |
| VAL-DROID-003 | DROID | Functional | Analyzes session context |
| VAL-DROID-004 | DROID | Functional | Detects personal preferences |
| VAL-DROID-005 | DROID | Functional | Detects project context |
| VAL-DROID-006 | DROID | Functional | Routes to correct memory file |
| VAL-DROID-007 | DROID | Functional | Prompts user confirmation |
| VAL-DROID-008 | DROID | Functional | Appends without overwriting |
| VAL-DROID-009 | DROID | Functional | Updates existing items |
| VAL-DROID-010 | DROID | Functional | Handles empty/missing files |
| VAL-CMD-001 | CMD | File check | Command file exists |
| VAL-CMD-002 | CMD | Functional | Invokes droid correctly |
| VAL-CMD-003 | CMD | Functional | Works from any directory |
| VAL-CMD-004 | CMD | Functional | Passes session context |
| VAL-FILE-001 | FILE | File check | Personal memory file exists |
| VAL-FILE-002 | FILE | File check | Project memory file exists |
| VAL-FILE-003 | FILE | Content check | Personal memory categories |
| VAL-FILE-004 | FILE | Content check | Project memory categories |
| VAL-FILE-005 | FILE | Content check | Valid markdown format |
| VAL-FILE-006 | FILE | Permission check | Readable and writable |
| VAL-FILE-007 | FILE | Content check | UTF-8 encoding |
| VAL-AGENTS-001 | AGENTS | Content check | Memory capture guide exists |
| VAL-AGENTS-002 | AGENTS | Content check | Orchestrator behavior documented |

## Testing Tools

- **File operations**: `ls`, `cat`, `test -f`, `test -r`, `test -w`
- **Content validation**: `grep`, `jq`
- **Droid invocation**: Task tool with `memory-synthesizer` subagent
- **Encoding check**: `file -I` (macOS) or `file -bi` (Linux)

## Known Quirks

1. **Droid location**: Custom droids are stored in `~/.factory/droids/`, not in the project
2. **Memory file location**: Personal memory is in home directory, project memory is relative to project root
3. **Model configuration**: Droid uses `claude-3-5-haiku-latest` for cost efficiency
4. **No service startup required**: This milestone is file-based, no servers to start
