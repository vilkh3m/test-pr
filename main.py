#!/usr/bin/env python3
"""
Example of using GitHubPRManager - a class for creating Pull Requests in GitHub.
"""

import os
from dotenv import load_dotenv
from github_pr_manager import GitHubPRManager

# Load environment variables from .env file, overwriting existing ones
load_dotenv(override=True)


def main():
    """Main function demonstrating the use of GitHubPRManager."""

    # Configuration - read from environment variables
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  # Token from .env file
    GITHUB_OWNER = os.getenv("GITHUB_OWNER", "some-owner")  # Repository owner (default: some-owner)
    GITHUB_REPO = os.getenv("GITHUB_REPO", "some-repo")  # Repository name (default: some-repo)
    GITHUB_API_URL = os.getenv("GITHUB_API_URL", "https://api.github.com")  # GitHub API URL (default: https://api.github.com)

    print("🔧 Configuration:")
    print(f"   Owner: {GITHUB_OWNER}")
    print(f"   Repository: {GITHUB_REPO}")
    print(f"   API URL: {GITHUB_API_URL}")

    # Check if the token was loaded
    if not GITHUB_TOKEN:
        print("❌ Error: GITHUB_TOKEN not found in environment variables!")
        print("💡 Make sure the .env file contains: GITHUB_TOKEN=your_token_here")
        return

    # Create an instance of the PR manager
    pr_manager = GitHubPRManager(
        token=GITHUB_TOKEN,
        owner=GITHUB_OWNER,
        repo=GITHUB_REPO,
        base_url=GITHUB_API_URL
    )

    print("🚀 GitHubPRManager - Pull Request Creation Demo")
    print("=" * 50)

    # Example 1: Creating a simple PR
    try:
        print("\n1️⃣ Creating a simple Pull Request...")
        pr_data = pr_manager.create_pull_request(
            title="Add new functionality",
            head="dev_branch",  # source branch
            base="master",         # target branch
            body="This PR adds new functionality to the project.\n\n- Added GitHubPRManager class\n- Added usage examples",
            draft=False
        )
        pr_number = pr_data['number']

        print(f"\n2️⃣ Adding reviewers to PR #{pr_number}...")
        pr_manager.add_reviewers(
            pr_number=pr_number,
            reviewers=["reviewer1"]  # Replace with real usernames
            # team_reviewers=["team-name"]  # Optionally teams
        )

    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Check if:")
        print("   - The GitHub token is correct")
        print("   - The 'dev_skrypt_pr' branch exists and has commits")
        print("   - The users in reviewers exist")

    print("\n" + "=" * 50)

    # # Example 2: Creating a PR with reviewers in one step
    # try:
    #     print("\n3️⃣ Creating a PR with reviewers in one step...")
    #     pr_manager.create_pr_with_reviewers(
    #         title="New feature with automatic reviewers",
    #         head="dev_branch",
    #         base="master",
    #         body="PR created with automatic addition of reviewers.",
    #         reviewers=["reviewer1"]  # Replace with real usernames
    #     )

    # except Exception as e:
    #     print(f"❌ Error: {e}")

    print("\n✨ Demo finished!")


if __name__ == "__main__":
    main()