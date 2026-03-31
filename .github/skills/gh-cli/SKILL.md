---
name: gh-cli
description: "GitHub CLI (gh) comprehensive reference for repositories, issues, pull requests, Actions, projects, releases, gists, codespaces, organizations, extensions, and all GitHub operations from the command line."
---

# GitHub CLI (gh)

Comprehensive reference for GitHub CLI (gh) - work seamlessly with GitHub from the command line.

**Version:** 2.85.0 (current as of January 2026)

---

## Prerequisites

### Installation

```bash
# macOS
brew install gh

# Linux
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update
sudo apt install gh

# Windows
winget install --id GitHub.cli

# Verify installation
gh --version
```

### Authentication

```bash
# Interactive login (default: github.com)
gh auth login

# Check authentication status
gh auth status

# Configure git to use gh as credential helper
gh auth setup-git
```

---

## CLI Structure

```
gh                          # Root command
├── auth                    # Authentication
│   ├── login
│   ├── logout
│   ├── refresh
│   ├── setup-git
│   ├── status
│   ├── switch
│   └── token
├── browse                  # Open in browser
├── codespace               # GitHub Codespaces
│   ├── code
│   ├── cp
│   ├── create
│   ├── delete
│   ├── edit
│   ├── jupyter
│   ├── list
│   ├── logs
│   ├── ports
│   ├── rebuild
│   ├── ssh
│   ├── stop
│   └── view
├── gist                    # Gists
│   ├── clone
│   ├── create
│   ├── delete
│   ├── edit
│   ├── list
│   ├── rename
│   └── view
├── issue                   # Issues
│   ├── create
│   ├── list
│   ├── status
│   ├── close
│   ├── comment
│   ├── delete
│   ├── develop
│   ├── edit
│   ├── lock
│   ├── pin
│   ├── reopen
│   ├── transfer
│   ├── unlock
│   └── view
├── org                     # Organizations
│   └── list
├── pr                      # Pull Requests
│   ├── create
│   ├── list
│   ├── status
│   ├── checkout
│   ├── checks
│   ├── close
│   ├── comment
│   ├── diff
│   ├── edit
│   ├── lock
│   ├── merge
│   ├── ready
│   ├── reopen
│   ├── revert
│   ├── review
│   ├── unlock
│   ├── update-branch
│   └── view
├── project                 # Projects
│   ├── close
│   ├── copy
│   ├── create
│   ├── delete
│   ├── edit
│   ├── field-create
│   ├── field-delete
│   ├── field-list
│   ├── item-add
│   ├── item-archive
│   ├── item-create
│   ├── item-delete
│   ├── item-edit
│   ├── item-list
│   ├── link
│   ├── list
│   ├── mark-template
│   ├── unlink
│   └── view
├── release                 # Releases
│   ├── create
│   ├── list
│   ├── delete
│   ├── delete-asset
│   ├── download
│   ├── edit
│   ├── upload
│   ├── verify
│   ├── verify-asset
│   └── view
├── repo                    # Repositories
│   ├── create
│   ├── list
│   ├── archive
│   ├── autolink
│   ├── clone
│   ├── delete
│   ├── deploy-key
│   ├── edit
│   ├── fork
│   ├── gitignore
│   ├── license
│   ├── rename
│   ├── set-default
│   ├── sync
│   ├── unarchive
│   └── view
├── cache                   # Actions caches
│   ├── delete
│   └── list
├── run                     # Workflow runs
│   ├── cancel
│   ├── delete
│   ├── download
│   ├── list
│   ├── rerun
│   ├── view
│   └── watch
├── workflow                # Workflows
│   ├── disable
│   ├── enable
│   ├── list
│   ├── run
│   └── view
├── agent-task              # Agent tasks
├── alias                   # Command aliases
│   ├── delete
│   ├── import
│   ├── list
│   └── set
├── api                     # API requests
├── attestation             # Artifact attestations
│   ├── download
│   ├── trusted-root
│   └── verify
├── completion              # Shell completion
├── config                  # Configuration
│   ├── clear-cache
│   ├── get
│   ├── list
│   └── set
├── extension               # Extensions
│   ├── browse
│   ├── create
│   ├── exec
│   ├── install
│   ├── list
│   ├── remove
│   ├── search
│   └── upgrade
├── gpg-key                 # GPG keys
│   ├── add
│   ├── delete
│   └── list
├── label                   # Labels
│   ├── clone
│   ├── create
│   ├── delete
│   ├── edit
│   └── list
├── preview                 # Preview features
├── ruleset                 # Rulesets
│   ├── check
│   ├── list
│   └── view
├── search                  # Search
│   ├── code
│   ├── commits
│   ├── issues
│   ├── prs
│   └── repos
├── secret                  # Secrets
│   ├── delete
│   ├── list
│   └── set
├── ssh-key                 # SSH keys
│   ├── add
│   ├── delete
│   └── list
├── status                  # Status overview
└── variable                # Variables
    ├── delete
    ├── get
    ├── list
    └── set
```

---

## Common Workflows

### Create PR from Issue

```bash
gh issue develop 123 --branch feature/issue-123
git add . && git commit -m "Fix issue #123"
git push
gh pr create --title "Fix #123" --body "Closes #123"
```

### Bulk Operations

```bash
# Close multiple issues
gh issue list --search "label:stale" --json number --jq '.[].number' | \
  xargs -I {} gh issue close {} --comment "Closing as stale"

# Add label to multiple PRs
gh pr list --search "review:required" --json number --jq '.[].number' | \
  xargs -I {} gh pr edit {} --add-label needs-review
```

### Repository Setup

```bash
gh repo create my-project --public --description "My awesome project" --clone --gitignore python --license mit
cd my-project
gh label create bug --color "d73a4a" --description "Bug report"
gh label create enhancement --color "a2eeef" --description "Feature request"
```

### CI/CD Workflow

```bash
RUN_ID=$(gh workflow run ci.yml --ref main --jq '.databaseId')
gh run watch "$RUN_ID"
gh run download "$RUN_ID" --dir ./artifacts
```

### Fork Sync

```bash
gh repo fork original/repo --clone
cd repo
gh repo sync
```

---

## Best Practices

1. **Authentication**: Use environment variables for automation — `export GH_TOKEN=$(gh auth token)`
2. **Default Repository**: Set default to avoid repetition — `gh repo set-default owner/repo`
3. **JSON Parsing**: Use jq for complex data extraction — `gh pr list --json number,title --jq '.[] | select(.title | contains("fix"))'`
4. **Pagination**: Use `--paginate` for large result sets — `gh issue list --state all --paginate`
5. **Caching**: Use cache control for frequently accessed data — `gh api /user --cache force`

---

## references/ 가이드

아래 문서는 각 카테고리별 상세 명령어 레퍼런스다. 필요한 명령어가 있을 때 해당 문서를 직접 읽고 옵션을 확인한다.

| 파일 | 내용 |
| --- | --- |
| `references/core-commands.md` | Authentication, Browse, Repositories, Configuration, Aliases, API Requests, Global Flags, Output Formatting, Completion, Environment Setup |
| `references/collaboration.md` | Issues, Pull Requests, Projects, Labels, Search |
| `references/devops-and-ecosystem.md` | GitHub Actions (Runs, Workflows, Caches, Secrets, Variables), Releases, Gists, Codespaces, Organizations, SSH/GPG Keys, Extensions, Rulesets, Attestations, Status, Preview, Agent Tasks |

---

## Getting Help

```bash
gh --help                    # General help
gh pr --help                 # Command help
gh issue create --help       # Subcommand help
gh help formatting           # Help topics
gh help environment
```

## External References

- Official Manual: https://cli.github.com/manual/
- GitHub Docs: https://docs.github.com/en/github-cli
- REST API: https://docs.github.com/en/rest
- GraphQL API: https://docs.github.com/en/graphql
