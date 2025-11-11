import requests
import json
from typing import List, Optional, Dict, Any


class GitHubPRManager:
    """
    A class to manage GitHub Pull Requests via the API.
    Allows creating PRs and adding reviewers.
    """

    def __init__(self, token: str, owner: str, repo: str, base_url: str = "https://api.github.com"):
        """
        Initializes the GitHub PR manager.

        Args:
            token (str): GitHub Personal Access Token
            owner (str): Repository owner (username or organization)
            repo (str): Repository name
            base_url (str): GitHub API base URL (default: https://api.github.com)
        """
        # Remove any whitespace from the token
        self.token = token.strip()
        self.owner = owner
        self.repo = repo
        self.base_url = base_url
        # Check if the token starts with github_pat_
        if not self.token.startswith('github_pat_'):
            print("⚠️  Warning: Token does not start with 'github_pat_', it might not be loaded correctly")

        # Additional token validation
        if '"' in self.token or "'" in self.token:
            raise ValueError("Token contains invalid characters (quotes or apostrophes)")

        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github+json",  # Update Accept header
            "X-GitHub-Api-Version": "2022-11-28",    # Add API version
            "Content-Type": "application/json"
        }

        # Debug information about headers (hide most of the token)
        token_preview = f"{token[:15]}...{token[-5:]}" if len(token) > 20 else token
        print(f"🔐 Using token: {token_preview}")
        print("📡 API Headers:")
        for key, value in self.headers.items():
            if key == "Authorization":
                print(f"   {key}: Bearer {token_preview}")
            else:
                print(f"   {key}: {value}")

    def check_branch_exists(self, branch_name: str) -> bool:
        """
        Checks if a branch exists in the GitHub repository.

        Args:
            branch_name (str): The name of the branch to check

        Returns:
            bool: True if the branch exists, False otherwise
        """
        url = f"{self.base_url}/repos/{self.owner}/{self.repo}/branches/{branch_name}"

        try:
            response = requests.get(url, headers=self.headers)
            return response.status_code == 200
        except requests.RequestException:
            return False

    def validate_branches(self, head: str, base: str) -> None:
        """
        Checks if both branches (head and base) exist in the repository.
        Raises an exception if either branch does not exist.

        Args:
            head (str): The name of the source branch
            base (str): The name of the target branch

        Raises:
            ValueError: When a branch does not exist
        """
        if not self.check_branch_exists(head):
            raise ValueError(f"❌ Source branch '{head}' does not exist in the repository!")

        if not self.check_branch_exists(base):
            raise ValueError(f"❌ Target branch '{base}' does not exist in the repository!")

        print("✅ Both branches exist in the repository!")

    def create_pull_request(
        self,
        title: str,
        head: str,
        base: str,
        body: Optional[str] = None,
        draft: bool = False
    ) -> Dict[str, Any]:
        """
        Creates a new Pull Request.

        Args:
            title (str): The title of the Pull Request
            head (str): The name of the branch to merge from
            base (str): The name of the target branch (e.g., 'main', 'master')
            body (str, optional): The description of the Pull Request
            draft (bool): Whether the PR should be a draft

        Returns:
            Dict[str, Any]: The response from the GitHub API with the created PR data

        Raises:
            requests.RequestException: When an HTTP request error occurs
            ValueError: When the API returns an error or a branch does not exist
        """
        # Check if branches exist before creating the PR
        self.validate_branches(head, base)

        url = f"{self.base_url}/repos/{self.owner}/{self.repo}/pulls"

        data = {
            "title": title,
            "head": head,
            "base": base,
            "draft": draft
        }

        if body:
            data["body"] = body

        try:
            response = requests.post(url, headers=self.headers, data=json.dumps(data))
            response.raise_for_status()

            pr_data = response.json()
            print("✅ Pull Request created successfully!")
            print(f"📋 Title: {pr_data['title']}")
            print(f"🔗 URL: {pr_data['html_url']}")
            print(f"🆔 PR Number: #{pr_data['number']}")

            return pr_data

        except requests.RequestException as e:
            print(f"❌ Error creating PR: {e}")
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_data = e.response.json()
                    print(f"📝 Error details: {error_data}")
                except Exception:
                    print(f"📝 Server response: {e.response.text}")
            raise

    def add_reviewers(
        self,
        pr_number: int,
        reviewers: Optional[List[str]] = None,
        team_reviewers: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Adds reviewers to an existing Pull Request.

        Args:
            pr_number (int): The Pull Request number
            reviewers (List[str], optional): A list of user usernames
            team_reviewers (List[str], optional): A list of team names

        Returns:
            Dict[str, Any]: The response from the GitHub API

        Raises:
            requests.RequestException: When an HTTP request error occurs
            ValueError: When no reviewers are provided or the API returns an error
        """
        if not reviewers and not team_reviewers:
            raise ValueError("At least one reviewer or team must be provided")

        url = f"{self.base_url}/repos/{self.owner}/{self.repo}/pulls/{pr_number}/requested_reviewers"

        data = {}
        if reviewers:
            data["reviewers"] = reviewers
        if team_reviewers:
            data["team_reviewers"] = team_reviewers

        try:
            response = requests.post(url, headers=self.headers, data=json.dumps(data))
            response.raise_for_status()

            result = response.json()
            print(f"✅ Reviewers added successfully to PR #{pr_number}!")

            if reviewers:
                print(f"👥 Added reviewers: {', '.join(reviewers)}")
            if team_reviewers:
                print(f"🏢 Added teams: {', '.join(team_reviewers)}")

            return result

        except requests.RequestException as e:
            print(f"❌ Error adding reviewers: {e}")
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_data = e.response.json()
                    print(f"📝 Error details: {error_data}")
                except Exception:
                    print(f"📝 Server response: {e.response.text}")
            raise

    def create_pr_with_reviewers(
        self,
        title: str,
        head: str,
        base: str,
        body: Optional[str] = None,
        draft: bool = False,
        reviewers: Optional[List[str]] = None,
        team_reviewers: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Creates a Pull Request and immediately adds reviewers to it.

        Args:
            title (str): The title of the Pull Request
            head (str): The name of the source branch
            base (str): The name of the target branch
            body (str, optional): The description of the Pull Request
            draft (bool): Whether the PR should be a draft
            reviewers (List[str], optional): A list of reviewer usernames
            team_reviewers (List[str], optional): A list of team names

        Returns:
            Dict[str, Any]: The created PR data with information about the reviewers
        """
        # First, create the PR
        pr_data = self.create_pull_request(title, head, base, body, draft)
        pr_number = pr_data['number']

        # Then, add reviewers if provided
        if reviewers or team_reviewers:
            try:
                self.add_reviewers(pr_number, reviewers, team_reviewers)
                pr_data['reviewers_added'] = True
            except Exception as e:
                print(f"⚠️  PR was created, but an error occurred while adding reviewers: {e}")
                pr_data['reviewers_added'] = False

        return pr_data

    def get_pull_request(self, pr_number: int) -> Dict[str, Any]:
        """
        Retrieves information about a Pull Request.

        Args:
            pr_number (int): The Pull Request number

        Returns:
            Dict[str, Any]: The Pull Request data
        """
        url = f"{self.base_url}/repos/{self.owner}/{self.repo}/pulls/{pr_number}"

        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()

        except requests.RequestException as e:
            print(f"❌ Error retrieving PR information: {e}")
            raise