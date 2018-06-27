from django.db import models


class HousingGroup(models.Model):
    CONTAINER = ('container', 'Container')
    VAN = ('van', 'Van')
    RECREATIONAL_VEHICLE = ('rv', 'RV')
    SHIFTPOD = ('shiftpod', 'Shiftpod')
    CAMP_YURT = ('campyurt', 'Camp Yurt')
    NEW_YURT = ('personalyurt', 'Personal Yurt')
    TENT = ('tent', 'Tent')
    OTHER = ('other', 'Other')
    HOUSING_CHOICES = (
        CAMP_YURT,
        NEW_YURT,
        TENT,
        RECREATIONAL_VEHICLE,
        CONTAINER,
        VAN,
        SHIFTPOD,
        OTHER,
    )

    housing_type = models.CharField(
        max_length=10,
        choices=HOUSING_CHOICES,
        blank=True,
        null=True
    )

    def __str__(self):
        return 'HousingGroup #{}: {}'.format(self.id, self.housing_type)

