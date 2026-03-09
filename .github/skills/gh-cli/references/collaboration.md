# Collaboration

## Issues (gh issue)

### Create Issue

```bash
# Create issue interactively
gh issue create

# Create with title
gh issue create --title "Bug: Login not working"

# Create with title and body
gh issue create \
  --title "Bug: Login not working" \
  --body "Steps to reproduce..."

# Create with body from file
gh issue create --body-file issue.md

# Create with labels
gh issue create --title "Fix bug" --labels bug,high-priority

# Create with assignees
gh issue create --title "Fix bug" --assignee user1,user2

# Create in specific repository
gh issue create --repo owner/repo --title "Issue title"

# Create issue from web
gh issue create --web
```

### List Issues

```bash
# List all open issues
gh issue list

# List all issues (including closed)
gh issue list --state all

# List closed issues
gh issue list --state closed

# Limit results
gh issue list --limit 50

# Filter by assignee
gh issue list --assignee username
gh issue list --assignee @me

# Filter by labels
gh issue list --labels bug,enhancement

# Filter by milestone
gh issue list --milestone "v1.0"

# Search/filter
gh issue list --search "is:open is:issue label:bug"

# JSON output
gh issue list --json number,title,state,author

# Table view
gh issue list --json number,title,labels --jq '.[] | [.number, .title, .labels[].name] | @tsv'

# Show comments count
gh issue list --json number,title,comments --jq '.[] | [.number, .title, .comments]'

# Sort by
gh issue list --sort created --order desc
```

### View Issue

```bash
# View issue
gh issue view 123

# View with comments
gh issue view 123 --comments

# View in browser
gh issue view 123 --web

# JSON output
gh issue view 123 --json title,body,state,labels,comments

# View specific fields
gh issue view 123 --json title --jq '.title'
```

### Edit Issue

```bash
# Edit interactively
gh issue edit 123

# Edit title
gh issue edit 123 --title "New title"

# Edit body
gh issue edit 123 --body "New description"

# Add labels
gh issue edit 123 --add-label bug,high-priority

# Remove labels
gh issue edit 123 --remove-label stale

# Add assignees
gh issue edit 123 --add-assignee user1,user2

# Remove assignees
gh issue edit 123 --remove-assignee user1

# Set milestone
gh issue edit 123 --milestone "v1.0"
```

### Close/Reopen Issue

```bash
# Close issue
gh issue close 123

# Close with comment
gh issue close 123 --comment "Fixed in PR #456"

# Reopen issue
gh issue reopen 123
```

### Comment on Issue

```bash
# Add comment
gh issue comment 123 --body "This looks good!"

# Edit comment
gh issue comment 123 --edit 456789 --body "Updated comment"

# Delete comment
gh issue comment 123 --delete 456789
```

### Issue Status

```bash
# Show issue status summary
gh issue status

# Status for specific repository
gh issue status --repo owner/repo
```

### Pin/Unpin Issues

```bash
# Pin issue (pinned to repo dashboard)
gh issue pin 123

# Unpin issue
gh issue unpin 123
```

### Lock/Unlock Issue

```bash
# Lock conversation
gh issue lock 123

# Lock with reason
gh issue lock 123 --reason off-topic

# Unlock
gh issue unlock 123
```

### Transfer Issue

```bash
# Transfer to another repository
gh issue transfer 123 --repo owner/new-repo
```

### Delete Issue

```bash
# Delete issue
gh issue delete 123

# Confirm without prompt
gh issue delete 123 --yes
```

### Develop Issue (Draft PR)

```bash
# Create draft PR from issue
gh issue develop 123

# Create in specific branch
gh issue develop 123 --branch fix/issue-123

# Create with base branch
gh issue develop 123 --base main
```

---

## Pull Requests (gh pr)

### Create Pull Request

```bash
# Create PR interactively
gh pr create

# Create with title
gh pr create --title "Feature: Add new functionality"

# Create with title and body
gh pr create \
  --title "Feature: Add new functionality" \
  --body "This PR adds..."

# Fill body from template
gh pr create --body-file .github/PULL_REQUEST_TEMPLATE.md

# Set base branch
gh pr create --base main

# Set head branch (default: current branch)
gh pr create --head feature-branch

# Create draft PR
gh pr create --draft

# Add assignees
gh pr create --assignee user1,user2

# Add reviewers
gh pr create --reviewer user1,user2

# Add labels
gh pr create --labels enhancement,feature

# Link to issue
gh pr create --issue 123

# Create in specific repository
gh pr create --repo owner/repo

# Open in browser after creation
gh pr create --web
```

### List Pull Requests

```bash
# List open PRs
gh pr list

# List all PRs
gh pr list --state all

# List merged PRs
gh pr list --state merged

# List closed (not merged) PRs
gh pr list --state closed

# Filter by head branch
gh pr list --head feature-branch

# Filter by base branch
gh pr list --base main

# Filter by author
gh pr list --author username
gh pr list --author @me

# Filter by assignee
gh pr list --assignee username

# Filter by labels
gh pr list --labels bug,enhancement

# Limit results
gh pr list --limit 50

# Search
gh pr list --search "is:open is:pr label:review-required"

# JSON output
gh pr list --json number,title,state,author,headRefName

# Show check status
gh pr list --json number,title,statusCheckRollup --jq '.[] | [.number, .title, .statusCheckRollup[]?.status]'

# Sort by
gh pr list --sort created --order desc
```

### View Pull Request

```bash
# View PR
gh pr view 123

# View with comments
gh pr view 123 --comments

# View in browser
gh pr view 123 --web

# JSON output
gh pr view 123 --json title,body,state,author,commits,files

# View diff
gh pr view 123 --json files --jq '.files[].path'

# View with jq query
gh pr view 123 --json title,state --jq '"\(.title): \(.state)"'
```

### Checkout Pull Request

```bash
# Checkout PR branch
gh pr checkout 123

# Checkout with specific branch name
gh pr checkout 123 --branch name-123

# Force checkout
gh pr checkout 123 --force
```

### Diff Pull Request

```bash
# View PR diff
gh pr diff 123

# View diff with color
gh pr diff 123 --color always

# Output to file
gh pr diff 123 > pr-123.patch

# View diff of specific files
gh pr diff 123 --name-only
```

### Merge Pull Request

```bash
# Merge PR
gh pr merge 123

# Merge with specific method
gh pr merge 123 --merge
gh pr merge 123 --squash
gh pr merge 123 --rebase

# Delete branch after merge
gh pr merge 123 --delete-branch

# Merge with comment
gh pr merge 123 --subject "Merge PR #123" --body "Merging feature"

# Merge draft PR
gh pr merge 123 --admin

# Force merge (skip checks)
gh pr merge 123 --admin
```

### Close Pull Request

```bash
# Close PR (as draft, not merge)
gh pr close 123

# Close with comment
gh pr close 123 --comment "Closing due to..."
```

### Reopen Pull Request

```bash
# Reopen closed PR
gh pr reopen 123
```

### Edit Pull Request

```bash
# Edit interactively
gh pr edit 123

# Edit title
gh pr edit 123 --title "New title"

# Edit body
gh pr edit 123 --body "New description"

# Add labels
gh pr edit 123 --add-label bug,enhancement

# Remove labels
gh pr edit 123 --remove-label stale

# Add assignees
gh pr edit 123 --add-assignee user1,user2

# Remove assignees
gh pr edit 123 --remove-assignee user1

# Add reviewers
gh pr edit 123 --add-reviewer user1,user2

# Remove reviewers
gh pr edit 123 --remove-reviewer user1

# Mark as ready for review
gh pr edit 123 --ready
```

### Ready for Review

```bash
# Mark draft PR as ready
gh pr ready 123
```

### Pull Request Checks

```bash
# View PR checks
gh pr checks 123

# Watch checks in real-time
gh pr checks 123 --watch

# Watch interval (seconds)
gh pr checks 123 --watch --interval 5
```

### Comment on Pull Request

```bash
# Add comment
gh pr comment 123 --body "Looks good!"

# Comment on specific line
gh pr comment 123 --body "Fix this" \
  --repo owner/repo \
  --head-owner owner --head-branch feature

# Edit comment
gh pr comment 123 --edit 456789 --body "Updated"

# Delete comment
gh pr comment 123 --delete 456789
```

### Review Pull Request

```bash
# Review PR (opens editor)
gh pr review 123

# Approve PR
gh pr review 123 --approve --body "LGTM!"

# Request changes
gh pr review 123 --request-changes \
  --body "Please fix these issues"

# Comment on PR
gh pr review 123 --comment --body "Some thoughts..."

# Dismiss review
gh pr review 123 --dismiss
```

### Update Branch

```bash
# Update PR branch with latest base branch
gh pr update-branch 123

# Force update
gh pr update-branch 123 --force

# Use merge strategy
gh pr update-branch 123 --merge
```

### Lock/Unlock Pull Request

```bash
# Lock PR conversation
gh pr lock 123

# Lock with reason
gh pr lock 123 --reason off-topic

# Unlock
gh pr unlock 123
```

### Revert Pull Request

```bash
# Revert merged PR
gh pr revert 123

# Revert with specific branch name
gh pr revert 123 --branch revert-pr-123
```

### Pull Request Status

```bash
# Show PR status summary
gh pr status

# Status for specific repository
gh pr status --repo owner/repo
```

---

## Projects (gh project)

```bash
# List projects
gh project list

# List for owner
gh project list --owner owner

# Open projects
gh project list --open

# View project
gh project view 123

# View project items
gh project view 123 --format json

# Create project
gh project create --title "My Project"

# Create in organization
gh project create --title "Project" --org orgname

# Create with readme
gh project create --title "Project" --readme "Description here"

# Edit project
gh project edit 123 --title "New Title"

# Delete project
gh project delete 123

# Close project
gh project close 123

# Copy project
gh project copy 123 --owner target-owner --title "Copy"

# Mark template
gh project mark-template 123

# List fields
gh project field-list 123

# Create field
gh project field-create 123 --title "Status" --datatype single_select

# Delete field
gh project field-delete 123 --id 456

# List items
gh project item-list 123

# Create item
gh project item-create 123 --title "New item"

# Add item to project
gh project item-add 123 --owner-owner --repo repo --issue 456

# Edit item
gh project item-edit 123 --id 456 --title "Updated title"

# Delete item
gh project item-delete 123 --id 456

# Archive item
gh project item-archive 123 --id 456

# Link items
gh project link 123 --id 456 --link-id 789

# Unlink items
gh project unlink 123 --id 456 --link-id 789

# View project in browser
gh project view 123 --web
```

---

## Labels (gh label)

```bash
# List labels
gh label list

# Create label
gh label create bug --color "d73a4a" --description "Something isn't working"

# Create with hex color
gh label create enhancement --color "#a2eeef"

# Edit label
gh label edit bug --name "bug-report" --color "ff0000"

# Delete label
gh label delete bug

# Clone labels from repository
gh label clone owner/repo

# Clone to specific repository
gh label clone owner/repo --repo target/repo
```

---

## Search (gh search)

```bash
# Search code
gh search code "TODO"

# Search in specific repository
gh search code "TODO" --repo owner/repo

# Search commits
gh search commits "fix bug"

# Search issues
gh search issues "label:bug state:open"

# Search PRs
gh search prs "is:open is:pr review:required"

# Search repositories
gh search repos "stars:>1000 language:python"

# Limit results
gh search repos "topic:api" --limit 50

# JSON output
gh search repos "stars:>100" --json name,description,stargazers

# Order results
gh search repos "language:rust" --order desc --sort stars

# Search with extensions
gh search code "import" --extension py

# Web search (open in browser)
gh search prs "is:open" --web
```
