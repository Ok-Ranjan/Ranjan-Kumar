from django.contrib import admin

from .models import Skill, Project, Achievement, Resume

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'level')

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'github_link', 'demo_link')

@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_awarded')

@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('title',)
