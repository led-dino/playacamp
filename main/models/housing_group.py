from django.db import models


class HousingGroup(models.Model):
    CAMP_YURT = ('campyurt', 'Camp Yurt')
    NEW_YURT = ('newyurt', 'New Yurt')
    TENT = ('tent', 'Tent')
    RECREATIONAL_VEHICLE = ('rv', 'RV')
    CONTAINER = ('container', 'Container')
    OTHER = ('other', 'Other')
    HOUSING_CHOICES = (CAMP_YURT, NEW_YURT, TENT, RECREATIONAL_VEHICLE, CONTAINER, OTHER)

    housing_type = models.CharField(
        max_length=10,
        choices=HOUSING_CHOICES,
        blank=True,
        null=True
    )

    def __str__(self):
        return 'HousingGroup #{}: {}'.format(self.id, self.housing_type)

