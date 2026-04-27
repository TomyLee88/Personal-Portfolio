import os
import requests
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.http import HttpResponse

PORTFOLIO_TOPIC = "portfolio"
GITHUB_USERNAMES = ["TomyLee88"]

FEATURED_GAME = {
    "name": "Munch Run",
    "tagline": "Canvas platformer game with browser play and Electron desktop packaging.",
    "description": (
        "A large JavaScript game project built around canvas rendering, custom physics, "
        "enemy systems, level progression, audio, saves, and desktop builds for Windows, "
        "macOS, and Linux."
    ),
    "source_lines": "22k+ source lines",
    "repo_lines": "70k+ repository lines",
    "modules": "96 JavaScript modules",
    "entities": "19 enemy/entity files",
    "stack": ["JavaScript", "HTML5 Canvas", "CSS", "Electron", "better-sqlite3"],
    "github_url": "https://github.com/TomyLee88/munch-run",
    "live_url": "https://munch-run-9cf7.onrender.com/?v=20260427",
}

def fetch_github_repos(usernames):
    repos = []
    GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')
    headers = {"Authorization": f"token {GITHUB_TOKEN}"} if GITHUB_TOKEN else {}

    for username in usernames:
        url = f'https://api.github.com/users/{username}/repos'
        try:
            response = requests.get(url, headers=headers, timeout=8)
            response.raise_for_status()
            repos += response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from {url}: {e}")
    return repos


def get_portfolio_repos():
    repos = fetch_github_repos(GITHUB_USERNAMES)
    portfolio_repos = []

    for repo in repos:
        topics = repo.get('topics') or []
        if PORTFOLIO_TOPIC in topics:
            portfolio_repos.append({**repo, 'live_demo_url': repo.get('homepage')})

    return sorted(portfolio_repos, key=lambda x: x['created_at'], reverse=True)


def home(request):
    repos_sorted = get_portfolio_repos()

    return render(request, 'web/home.html', {
        'latest_repos': repos_sorted[:2],
        'featured_game': FEATURED_GAME,
        'portfolio_topic': PORTFOLIO_TOPIC,
    })  # Limit to 2 repos

def github_repos(request):
    filtered_repos = get_portfolio_repos()

    return render(request, 'web/projects.html', {
        'repos': filtered_repos,
        'featured_game': FEATURED_GAME,
        'portfolio_topic': PORTFOLIO_TOPIC,
    })

# Other views unchanged
def about(request):
    return render(request, 'web/about.html')

def caseStudies(request):
    return render(request, 'web/caseStudies.html')

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
