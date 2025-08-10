from django.shortcuts import render
from .models import Skill, Project, Achievement, Resume
from django.core.mail import EmailMessage
from django.conf import settings
from .forms import ContactForm
import json
import logging
import requests

logger = logging.getLogger(__name__)

def get_github_data(username):
    user_api = f"https://api.github.com/users/{username}"
    repos_api = f"https://api.github.com/users/{username}/repos"

    try:
        user_data = requests.get(user_api).json()
        repos_data = requests.get(repos_api).json()

        # Collect languages usage
        languages = {}
        total_stars = 0
        for repo in repos_data:
            lang = repo.get('language')
            if lang:
                languages[lang] = languages.get(lang, 0) + 1
            total_stars += repo.get('stargazers_count', 0)

        return {
            'name': user_data.get('name', username),
            'username': username,
            'avatar': user_data.get('avatar_url'),
            'bio': user_data.get('bio', 'GitHub Developer'),
            'profile_url': user_data.get('html_url'),
            'public_repos': user_data.get('public_repos', 0),
            'followers': user_data.get('followers', 0),
            'stars': total_stars,
            'languages': languages
        }
    except:
        return None

def home(request):
    skills = Skill.objects.all()
    skill_labels = [skill.name for skill in skills]
    skill_values = [skill.level for skill in skills]

    projects = Project.objects.all()
    achievements = Achievement.objects.all()
    resume = Resume.objects.first() #get first uploaded resume

    resume_url = None
    if resume and resume.pdf_file:
        resume_url = request.build_absolute_uri(resume.pdf_file.url)

    github_data = get_github_data("Ok-Ranjan")

    lang_labels = []
    lang_values = []
    if github_data:
        lang_labels = list(github_data['languages'].keys())
        lang_values = list(github_data['languages'].values())

    # Contact form logic
    form = ContactForm()
    if request.method == "POST":
        form = ContactForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            file = form.cleaned_data.get('file')

            try:
                email_message = EmailMessage(
                    subject=f"Portfolio Contact Form - {name}",
                    body=f"From: {name}\nEmail: {email}\n\nMessage:\n{message}",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[settings.DEFAULT_FROM_EMAIL, 'ranjannp802114@mail.com'],  # Send to both
                )

                if file:
                    email_message.attach(file.name, file.read(), file.content_type)

                email_message.send()
                logger.info("✅ Email successfully sent to SendGrid.")
            except Exception as e:
                logger.error(f"❌ Email sending failed: {e}")

    return render(request, 'home.html', {
        'skill_labels': json.dumps(skill_labels),
        'skill_values': json.dumps(skill_values),
        'projects': projects,
        'achievements': achievements,
        'resume': resume,
        'resume_url': resume_url,
        'github_data': github_data,
        'lang_labels': json.dumps(lang_labels),
        'lang_values': json.dumps(lang_values),
        'form': form    
    })

