#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
GitHub API Integration Module
----------------------------
This module provides functions to interact with GitHub API
for tracking project progress and activities.
"""

import os
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

# In a real implementation, you would use the GitHub API client library
# For demonstration purposes, we're showing the structure
try:
    import requests
except ImportError:
    print("Requests library not installed. Run: pip install requests")


class GitHubManager:
    """Manager class for GitHub operations"""
    
    def __init__(self, token: Optional[str] = None):
        """Initialize the GitHub Manager
        
        Args:
            token: GitHub personal access token
        """
        self.token = token or os.environ.get('GITHUB_TOKEN')
        if not self.token:
            print("Warning: No GitHub token provided. API rate limits will be restricted.")
            
        self.headers = {
            'Accept': 'application/vnd.github.v3+json'
        }
        
        if self.token:
            self.headers['Authorization'] = f'token {self.token}'
            
        self.base_url = 'https://api.github.com'
        
    def get_user_repos(self, username: str) -> List[Dict[str, Any]]:
        """Get repositories for a specific user
        
        Args:
            username: GitHub username
            
        Returns:
            List of repository dictionaries
        """
        url = f"{self.base_url}/users/{username}/repos"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        
        return response.json()
    
    def get_repo_commits(self, 
                        owner: str, 
                        repo: str, 
                        since: Optional[datetime] = None,
                        until: Optional[datetime] = None) -> List[Dict[str, Any]]:
        """Get commits for a specific repository
        
        Args:
            owner: Repository owner username
            repo: Repository name
            since: Start date for commits (optional)
            until: End date for commits (optional)
            
        Returns:
            List of commit dictionaries
        """
        url = f"{self.base_url}/repos/{owner}/{repo}/commits"
        params = {}
        
        if since:
            params['since'] = since.isoformat()
        if until:
            params['until'] = until.isoformat()
            
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        
        return response.json()
    
    def get_repo_issues(self, 
                       owner: str, 
                       repo: str, 
                       state: str = 'all',
                       since: Optional[datetime] = None) -> List[Dict[str, Any]]:
        """Get issues for a specific repository
        
        Args:
            owner: Repository owner username
            repo: Repository name
            state: Issue state ('open', 'closed', or 'all')
            since: Start date for issues (optional)
            
        Returns:
            List of issue dictionaries
        """
        url = f"{self.base_url}/repos/{owner}/{repo}/issues"
        params = {'state': state}
        
        if since:
            params['since'] = since.isoformat()
            
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        
        return response.json()
    
    def get_repo_pull_requests(self, 
                              owner: str, 
                              repo: str, 
                              state: str = 'all') -> List[Dict[str, Any]]:
        """Get pull requests for a specific repository
        
        Args:
            owner: Repository owner username
            repo: Repository name
            state: PR state ('open', 'closed', or 'all')
            
        Returns:
            List of pull request dictionaries
        """
        url = f"{self.base_url}/repos/{owner}/{repo}/pulls"
        params = {'state': state}
            
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        
        return response.json()
    
    def get_user_activity(self, 
                         username: str, 
                         since_days: int = 7) -> Dict[str, Any]:
        """Get a summary of user activity across repositories
        
        Args:
            username: GitHub username
            since_days: Number of days to look back
            
        Returns:
            Dictionary with activity summary
        """
        # Calculate the date range
        since_date = datetime.now() - timedelta(days=since_days)
        
        # Get user repositories
        repos = self.get_user_repos(username)
        
        activity = {
            'username': username,
            'period': f"Last {since_days} days",
            'repositories': {},
            'total_commits': 0,
            'total_issues_opened': 0,
            'total_issues_closed': 0,
            'total_prs': 0
        }
        
        # For each repository, get commits and issues
        for repo in repos:
            repo_name = repo['name']
            repo_owner = repo['owner']['login']
            
            # Skip forks if not owned by the user
            if repo_owner.lower() != username.lower():
                continue
                
            # Get commits
            try:
                commits = self.get_repo_commits(
                    owner=repo_owner,
                    repo=repo_name,
                    since=since_date
                )
                
                # Filter commits by the user
                user_commits = [
                    commit for commit in commits
                    if commit.get('author') and commit['author'].get('login', '').lower() == username.lower()
                ]
                
                # Get issues
                issues = self.get_repo_issues(
                    owner=repo_owner,
                    repo=repo_name,
                    since=since_date
                )
                
                # Filter issues by the user
                user_issues = [
                    issue for issue in issues
                    if issue.get('user') and issue['user'].get('login', '').lower() == username.lower()
                ]
                
                # Count opened and closed issues
                opened_issues = len(user_issues)
                closed_issues = len([i for i in user_issues if i['state'] == 'closed'])
                
                # Get pull requests
                prs = self.get_repo_pull_requests(
                    owner=repo_owner,
                    repo=repo_name
                )
                
                # Filter PRs by the user and date
                user_prs = [
                    pr for pr in prs
                    if pr.get('user') and pr['user'].get('login', '').lower() == username.lower()
                    and datetime.fromisoformat(pr['created_at'].replace('Z', '+00:00')) >= since_date
                ]
                
                # Store repository activity
                activity['repositories'][repo_name] = {
                    'commits': len(user_commits),
                    'issues_opened': opened_issues,
                    'issues_closed': closed_issues,
                    'pull_requests': len(user_prs)
                }
                
                # Update totals
                activity['total_commits'] += len(user_commits)
                activity['total_issues_opened'] += opened_issues
                activity['total_issues_closed'] += closed_issues
                activity['total_prs'] += len(user_prs)
                
            except Exception as e:
                print(f"Error processing repository {repo_name}: {str(e)}")
                continue
        
        return activity
    
    def get_project_status(self, 
                          owner: str, 
                          repo: str) -> Dict[str, Any]:
        """Get comprehensive status of a specific project/repository
        
        Args:
            owner: Repository owner username
            repo: Repository name
            
        Returns:
            Dictionary with project status details
        """
        status = {
            'repository': f"{owner}/{repo}",
            'timestamp': datetime.now().isoformat(),
            'open_issues': 0,
            'open_prs': 0,
            'recent_commits': [],
            'contributors': []
        }
        
        # Get open issues
        try:
            issues = self.get_repo_issues(owner, repo, state='open')
            status['open_issues'] = len(issues)
            
            # Get recent issues details
            status['recent_issues'] = [
                {
                    'title': issue['title'],
                    'number': issue['number'],
                    'created_at': issue['created_at'],
                    'url': issue['html_url']
                }
                for issue in issues[:5]  # Get details for 5 most recent
            ]
        except Exception as e:
            print(f"Error fetching issues: {str(e)}")
        
        # Get open PRs
        try:
            prs = self.get_repo_pull_requests(owner, repo, state='open')
            status['open_prs'] = len(prs)
            
            # Get recent PR details
            status['recent_prs'] = [
                {
                    'title': pr['title'],
                    'number': pr['number'],
                    'created_at': pr['created_at'],
                    'url': pr['html_url']
                }
                for pr in prs[:5]  # Get details for 5 most recent
            ]
        except Exception as e:
            print(f"Error fetching pull requests: {str(e)}")
        
        # Get recent commits
        try:
            since_date = datetime.now() - timedelta(days=7)
            commits = self.get_repo_commits(owner, repo, since=since_date)
            
            # Get commit details
            status['recent_commits'] = [
                {
                    'sha': commit['sha'][:7],
                    'message': commit['commit']['message'].split('\n')[0],  # First line only
                    'author': commit['commit']['author']['name'],
                    'date': commit['commit']['author']['date']
                }
                for commit in commits[:10]  # Get details for 10 most recent
            ]
            
            # Get unique contributors from recent commits
            contributors = {}
            for commit in commits:
                author = commit['commit']['author']['name']
                if author not in contributors:
                    contributors[author] = 0
                contributors[author] += 1
                
            status['contributors'] = [
                {'name': name, 'commits': count}
                for name, count in contributors.items()
            ]
        except Exception as e:
            print(f"Error fetching commits: {str(e)}")
        
        return status


def main():
    """Example usage of the GitHubManager class"""
    # Use GitHub token from environment variable
    github = GitHubManager()
    
    # Example: Get user repositories
    username = "octocat"  # Example GitHub username
    print(f"Fetching repositories for {username}...")
    
    try:
        repos = github.get_user_repos(username)
        print(f"Found {len(repos)} repositories")
        
        # Print repository names
        for repo in repos[:5]:  # Show first 5
            print(f"- {repo['name']}")
            
        # Get activity for a user
        print(f"\nFetching activity for {username} in the last 7 days...")
        activity = github.get_user_activity(username)
        print(f"Total commits: {activity['total_commits']}")
        print(f"Total issues opened: {activity['total_issues_opened']}")
        print(f"Total PRs: {activity['total_prs']}")
        
    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == '__main__':
    main()
