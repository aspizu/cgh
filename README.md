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

### `cgh pr view`

View details of a pull request by its ID.

```sh
cgh pr view 42
cgh pr view 42 --web   # open in browser
```
