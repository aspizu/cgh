# AWS CodeCommit CLI for humans

[![Discord](https://img.shields.io/discord/1462182798210109505?style=flat&logo=discord&label=Discord)](https://discord.gg/mKQqsJ6UtK) ![GitHub License](https://img.shields.io/github/license/aspizu/cgh)

A better CLI for working with AWS CodeCommit repositories.

## Installation

Make sure you have the AWS CLI installed and login using `aws login`.

Use uv to install cgh:

```bash
uv tool install git+https://github.com/aspizu/cgh
```

## Agents

Add the following to your `AGENTS.md` file to use cgh to work with CodeCommit
repositories.

```md
This is an AWS CodeCommit repository, use the `cgh` command to work with pull requests.
The interface is exactly the same as the GitHub's CLI `gh` command.
```

## Usage

### `cgh pr create`

Create a pull request from the current branch.

```sh
cgh pr create --title "Fix login bug"
cgh pr create --title "Add feature" --body "Detailed description" --base main
cgh pr create --title "Hotfix" --head hotfix-branch --base production
```

### `cgh pr list`

List pull requests, with optional filters.

```sh
cgh pr list
cgh pr list --author @me
cgh pr list --status open --author @me
cgh pr list --status merged
```

### `cgh pr edit`

Edit the title or body of an existing pull request.

```sh
cgh pr edit 42 --title "New title"
cgh pr edit 42 --body "Updated description"
cgh pr edit 42 --title "New title" --body "Updated description"
```

### `cgh web`

Open the current repository at the current branch in the browser.

```sh
cgh web
```

### `cgh pr view`

View details of a pull request by its ID.

```sh
cgh pr view 42
cgh pr view 42 --web    # open in browser
cgh pr view 42 --jira   # open associated Jira ticket in browser
```

## Jira Integration

cgh can automatically update Jira issues when creating pull requests.

### Configuration

Add a `[jira]` section to `~/.config/cgh/config.toml`:

```toml
[jira]
url = "https://your-org.atlassian.net"
key = "PROJECT"
```

- `url` — base URL of your Jira instance
- `key` — the Jira project key (e.g. `PROJECT` for tickets like `PROJECT-123`)

### Pull Request field

When you create a PR with a Jira ticket number in the title, cgh will automatically set the `Pull-Request` custom field on the corresponding Jira issue to the PR URL. This requires [`jira-cli`](https://github.com/ankitpokhrel/jira-cli) to be installed and authenticated.

PR titles must start with the project key followed by the ticket number:

```sh
cgh pr create --title "PROJECT-123 Fix login bug"
```

cgh will run:

```sh
jira issue edit PROJECT-123 --custom Pull-Request=<pr_url>
```

If the Jira update fails (e.g. jira-cli is not installed or not configured), the error is shown and the PR is still created successfully. Pass `--verbose` to the root command to see the full error traceback:

```sh
cgh --verbose pr create --title "PROJECT-123 Fix login bug"
```
