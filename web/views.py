import os
import requests
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.http import HttpResponse

# List of real projects to display
REAL_PROJECTS = {
    "graduation-project",
    "django_project",
    "TommyDB",
    "UCD_python_TomislavColic",
    "musicnauts.github.io",
    "wisewalletucd"
}

# Fetch call function with GitHub token
def fetch_github_repos(usernames):
    repos = []
    GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')  # Add your token as env variable
    headers = {"Authorization": f"token {GITHUB_TOKEN}"} if GITHUB_TOKEN else {}

    for username in usernames:
        url = f'https://api.github.com/users/{username}/repos'
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            repos += response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from {url}: {e}")
    return repos

def home(request):
    github_usernames = ['TomyLee88']  # Only your account now

    # Fetch all repositories
    repos = fetch_github_repos(github_usernames)

    # Filter repos to include only the real projects and add homepage URLs
    filtered_repos = [
        {**repo, 'live_demo_url': repo.get('homepage')}
        for repo in repos if repo['name'] in REAL_PROJECTS
    ]

    # Sort combined repos by creation date
    repos_sorted = sorted(filtered_repos, key=lambda x: x['created_at'], reverse=True)

    return render(request, 'web/home.html', {'latest_repos': repos_sorted[:2]})

def github_repos(request):
    github_usernames = ['TomyLee88']

    repos = fetch_github_repos(github_usernames)

    filtered_repos = [
        {**repo, 'live_demo_url': repo.get('homepage')}
        for repo in repos if repo['name'] in REAL_PROJECTS
    ]

    return render(request, 'web/projects.html', {'repos': filtered_repos})

# Other views unchanged
def about(request):
    return render(request, 'web/about.html')

def contact(request):
    return render(request, 'web/contact.html')

def contact_view(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        sender = request.POST.get('email')
        recipients = ['tomislavcolic003@gmail.com']

        email_body = f"Message from: {sender}\n\n{message}"
        print(f"Subject: {subject}, Message: {email_body}, Sender: {sender}")

        try:
            send_mail(subject, email_body, sender, recipients)
            return redirect('success')
        except Exception as e:
            print(f"Error sending email: {e}")
            return HttpResponse("Error sending email", status=500)

    return render(request, 'web/contact.html')

def success_view(request):
    return render(request, 'web/success.html')
