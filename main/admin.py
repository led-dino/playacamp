import csv
import datetime
import io

from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.utils import timezone

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


class IsAttendingListFilter(admin.SimpleListFilter):
    title = 'Is Attending'
    parameter_name = 'is_attending'

    def lookups(self, request, model_admin):
        print(model_admin)
        return [
            ('yes', 'Yes'),
            ('no', 'No'),
        ]

    def queryset(self, request, queryset):
        current_year = timezone.now().year
        attending_users = User.objects.filter(attendanceprofile__year=current_year)
        print(attending_users)
        print(queryset)
        if self.value() == 'yes':
            return queryset.filter(pk__in=[u.pk for u in attending_users])

        if self.value() == 'no':
            return queryset.exclude(pk__in=[u.pk for u in attending_users])


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'first_name',
        'last_name',
        'phone_number',
        'location',
        'is_attending',
        'is_verified_by_admin',
    )
    list_filter = (
        IsAttendingListFilter,
        'is_verified_by_admin',
    )

    def export_csv(self, request, queryset):
        csv_stream = io.StringIO()
        writer = csv.writer(csv_stream)
        writer.writerow(UserProfile.csv_columns())

        for profile in queryset:
            writer.writerow(profile.to_csv())

        csv_stream.seek(0)
        now = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        filename = 'playacamp-csv-export-{}'.format(now)
        response = HttpResponse(csv_stream, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}'.format(filename)
        return response
    
    export_csv.short_description = "Export to CSV"

    actions = [export_csv]

    def location(self, obj):
        return obj.city_and_state()
    location.short_description = 'Location'


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
    list_display = ('name', 'description')


@admin.register(SocialMediaLink)
class SocialMediaLinkAdmin(admin.ModelAdmin):
    pass

