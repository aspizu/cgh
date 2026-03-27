# AWS CodeCommit CLI for humans

[![Discord](https://img.shields.io/discord/1462182798210109505?style=flat&logo=discord&label=Discord)](https://discord.gg/mKQqsJ6UtK) ![GitHub License](https://img.shields.io/github/license/aspizu/cgh)

A better CLI for working with AWS CodeCommit repositories.

## Installation

Make sure you have the AWS CLI installed and login using `aws login`.

Use uv to install cgh:

```bash
uv tool install git+https://github.com/aspizu/cgh
```

## Usage

The CLI interface is similar to the GitHub CLI `gh`.

```bash
cgh --help
```

## Agents

Add the following to your `AGENTS.md` file to use cgh to work with CodeCommit
repositories.

```md
This is an AWS CodeCommit repository, use the `cgh` command to work with pull requests.
The interface is exactly the same as the GitHub's CLI `gh` command.
```
