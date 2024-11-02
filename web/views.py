from django.shortcuts import render, redirect
import requests
# from .forms import ContactForm
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
#fetch call function
def fetch_github_repos(usernames):
    repos = []
    for username in usernames:
        url = f'https://api.github.com/users/{username}/repos'
        try:
            response = requests.get(url)
            response.raise_for_status()
            repos += response.json() 
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from {url}: {e}")
    return repos

def home(request):
    github_usernames = ['TomyLee88', 'TomislavColic']
    
    # Fetch all repositories
    repos = fetch_github_repos(github_usernames)

    # Filter repos to include only the real projects and add homepage URLs
    filtered_repos = [
        {**repo, 'live_demo_url': repo.get('homepage')} 
        for repo in repos if repo['name'] in REAL_PROJECTS
    ]

    # Sort combined repos by creation date 
    repos_sorted = sorted(filtered_repos, key=lambda x: x['created_at'], reverse=True)

    return render(request, 'web/home.html', {'latest_repos': repos_sorted[:2]})  # Limit to 2 repos

def github_repos(request):
    github_usernames = ['TomyLee88', 'TomislavColic']

    # Fetch all repositories
    repos = fetch_github_repos(github_usernames)

    # Filter repos to include only the real projects and add homepage URLs
    filtered_repos = [
        {**repo, 'live_demo_url': repo.get('homepage')} 
        for repo in repos if repo['name'] in REAL_PROJECTS
    ]

    # Pass the combined data 
    return render(request, 'web/projects.html', {'repos': filtered_repos})

def about(request):
    return render(request, 'web/about.html')
# contact 
def contact(request):
    return render(request, 'web/contact.html')


def contact_view(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        sender = request.POST.get('email')
        recipients = ['tomislavcolic003@gmail.com'] 

        #  print values to the console
        print(f"Subject: {subject}, Message: {message}, Sender: {sender}")

        # Send the email
        try:
            send_mail(subject, message, sender, recipients)
            return redirect('success')  # Redirect to success page
        except Exception as e:
            print(f"Error sending email: {e}")
            return HttpResponse("Error sending email", status=500)

    return render(request, 'web/contact.html')  # Render the form for GET requests


#message after sending email
def success_view(request):
    return render(request, 'web/success.html')  # Make sure this template exists

