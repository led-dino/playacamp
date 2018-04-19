from django.db import models
from main.models.job import Job


class JobAssignment(models.Model):
    job = models.ForeignKey(Job)
    attendee = models.ForeignKey('AttendanceProfile', related_name='job_assignments')
    date = models.DateField()

    def __str__(self):
        return 'JobAssignment: ({}, {})'.format(self.job, self.attendee)

