# GitHub PR Manager

A Python tool for creating and managing GitHub Pull Requests via the GitHub API. This project provides a simple and flexible way to automate PR creation and reviewer management.

## Features

- ✅ **Create Pull Requests** - Programmatically create PRs between branches
- ✅ **Add Reviewers** - Automatically assign reviewers (users and teams) to PRs
- ✅ **Branch Validation** - Verify that source and target branches exist before creating a PR
- ✅ **Flexible Configuration** - Configure via environment variables or use default values
- ✅ **Custom API URLs** - Support for GitHub Enterprise or custom GitHub API endpoints
- ✅ **Error Handling** - Comprehensive error messages and validation

## Prerequisites

- Python 3.7+
- GitHub Personal Access Token with the following permissions:
  - `repo` - Full control of private repositories
  - `read:org` and `write:org` - For adding team reviewers (optional)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/vilkh3m/test-pr.git
cd test-pr
```

2. Create a virtual environment (optional but recommended):
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
cp .env.example .env
```

Edit the `.env` file and add your GitHub token:
```env
GITHUB_TOKEN=your_github_personal_access_token_here

# Optional parameters (defaults shown)
GITHUB_OWNER=vilkh3m
GITHUB_REPO=test-pr
GITHUB_API_URL=https://api.github.com
```

## Usage

### Basic Example

Run the demo script:
```bash
python main.py
```

### Programmatic Usage

```python
from github_pr_manager import GitHubPRManager

# Initialize the PR manager
pr_manager = GitHubPRManager(
    token="your_github_token",
    owner="repository_owner",
    repo="repository_name"
)

# Create a Pull Request
pr_data = pr_manager.create_pull_request(
    title="Add new feature",
    head="feature-branch",
    base="main",
    body="Description of the changes",
    draft=False
)

# Add reviewers
pr_manager.add_reviewers(
    pr_number=pr_data['number'],
    reviewers=["username1", "username2"],
    team_reviewers=["team-name"]
)

# Or create a PR with reviewers in one step
pr_data = pr_manager.create_pr_with_reviewers(
    title="Add new feature",
    head="feature-branch",
    base="main",
    body="Description of the changes",
    reviewers=["username1"]
)
```

## API Reference

### `GitHubPRManager`

#### `__init__(token, owner, repo, base_url="https://api.github.com")`
Initialize the PR manager.

**Parameters:**
- `token` (str): GitHub Personal Access Token
- `owner` (str): Repository owner (username or organization)
- `repo` (str): Repository name
- `base_url` (str, optional): GitHub API base URL

#### `create_pull_request(title, head, base, body=None, draft=False)`
Create a new Pull Request.

**Parameters:**
- `title` (str): PR title
- `head` (str): Source branch name
- `base` (str): Target branch name
- `body` (str, optional): PR description
- `draft` (bool): Whether the PR should be a draft

**Returns:** Dict with PR data from GitHub API

#### `add_reviewers(pr_number, reviewers=None, team_reviewers=None)`
Add reviewers to an existing Pull Request.

**Parameters:**
- `pr_number` (int): PR number
- `reviewers` (list, optional): List of GitHub usernames
- `team_reviewers` (list, optional): List of team names

**Returns:** Dict with updated PR data

#### `create_pr_with_reviewers(title, head, base, body=None, draft=False, reviewers=None, team_reviewers=None)`
Create a PR and add reviewers in one operation.

**Parameters:** Combination of `create_pull_request` and `add_reviewers` parameters

**Returns:** Dict with PR data including reviewer status

## Configuration

The tool can be configured using environment variables in the `.env` file:

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `GITHUB_TOKEN` | ✅ Yes | - | GitHub Personal Access Token |
| `GITHUB_OWNER` | ❌ No | `vilkh3m` | Repository owner |
| `GITHUB_REPO` | ❌ No | `test-pr` | Repository name |
| `GITHUB_API_URL` | ❌ No | `https://api.github.com` | GitHub API endpoint |

## Creating a GitHub Token

1. Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token (classic)"
3. Select scopes:
   - ✅ `repo` - Full control of repositories
   - ✅ `write:org` - If you need to add team reviewers
4. Generate and copy the token
5. Add it to your `.env` file

For fine-grained tokens:
1. Go to GitHub Settings → Developer settings → Personal access tokens → Fine-grained tokens
2. Click "Generate new token"
3. Select repository access
4. Set Repository permissions:
   - **Pull requests**: Read and write
   - **Contents**: Read and write
   - **Metadata**: Read-only (automatically included)

## Troubleshooting

### 403 Forbidden Error
- Ensure your token has the correct permissions (`repo` scope)
- Verify the token hasn't expired
- Check that you have write access to the repository

### Branch Not Found
- Make sure both source and target branches exist in the repository
- Branch names are case-sensitive

### Token Not Loading from .env
- Ensure the `.env` file is in the same directory as `main.py`
- Remove any quotes around the token value in `.env`
- Run `load_dotenv(override=True)` to override system environment variables

## Project Structure

```
test-pr/
├── github_pr_manager.py    # Main PR manager class
├── main.py                 # Demo script
├── requirements.txt        # Python dependencies
├── .env.example           # Example environment configuration
├── .env                   # Your environment configuration (not in git)
└── README.md              # This file
```

## License

Apache License 2.0

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Author

Created by [vilkh3m](https://github.com/vilkh3m)