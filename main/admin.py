from django.contrib import admin

from .models import FoodRestriction, Team, TeamMembership, UserProfile

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
