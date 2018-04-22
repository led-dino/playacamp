from django.contrib import admin

from .models import (AttendanceProfile,
                     FoodRestriction,
                     HousingGroup,
                     Job,
                     JobAssignment,
                     Skill,
                     SocialMediaLink,
                     Team,
                     TeamMembership,
                     TransportationMethod,
                     UserProfile)


@admin.register(TeamMembership)
class TeamMembershipAdmin(admin.ModelAdmin):
    list_display = ('team', 'member', 'is_lead')


class TeamMembershipInline(admin.TabularInline):
    model = TeamMembership
    extra = 1


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    inlines = (TeamMembershipInline,)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(FoodRestriction)
class FoodRestrictionAdmin(admin.ModelAdmin):
    pass


@admin.register(AttendanceProfile)
class AttendanceProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(HousingGroup)
class HousingGroupAdmin(admin.ModelAdmin):
    pass


@admin.register(TransportationMethod)
class TransportationMethodAdmin(admin.ModelAdmin):
    pass


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    pass


@admin.register(JobAssignment)
class JobAssignmentAdmin(admin.ModelAdmin):
    pass


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    pass


@admin.register(SocialMediaLink)
class SocialMediaLinkAdmin(admin.ModelAdmin):
    pass

