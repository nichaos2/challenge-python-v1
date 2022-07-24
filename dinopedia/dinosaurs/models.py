from django.db import models
from django.db.models import F, Q
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.postgres.fields import ArrayField


class DinoOwner(models.Model):
    name = models.TextField(null=False)

    def __str__(self):
        return self.name

class Period(models.Model):
    """Years are in BC, so the start year is always greater than the end year
    Names : triassic , jurassic, cretaceous, paleogene, neogene
    deliberately not in a choices field in case we want to add something new!!!
    """

    name = models.CharField(null=False,max_length=15)
    start_year = models.IntegerField(null=False)
    end_year = models.IntegerField(null=False)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} : from {self.start_year} to {self.end_year} BC"

    class Meta:
        ordering = ["name", "start_year"]
        constraints = [
            models.UniqueConstraint(fields=["name"], name="unique_period_name"),
            models.CheckConstraint(
                check=Q(
                    end_year__lte=F("start_year"),
                ),
                name="end_after_start",
            ),
        ]


class DinoSize(models.Model):
    """
    which is a bigger dinosaur, the tall or the heavy?

    tiny, very small, small, medium, large, very large
    - length (m) - min -> max
    - height (m) - min -> max
    - width (m) - min -> max
    - weight (kgs) - min -> max
    """

    class SizeCategory(models.TextChoices):
        TINY = "TN", _("Tiny")
        VERY_SMALL = "VS", _("Very small")
        SMALL = "S", _("Small")
        MEDIUM = "M", _("Medium")
        LARGE = "L", _("Large")
        VERY_LARGE = "VL", _("Very large")
        GIGANTIC = "G", _("Gigantic")

    size = models.CharField(
        max_length=15,
        choices=SizeCategory.choices,
        null=False,
        blank=False,
    )

    #
    height_min = models.FloatField(
        null=False, blank=False, validators=[MinValueValidator(0.001)]
    )
    height_max = models.FloatField(
        null=False, blank=False, validators=[MinValueValidator(0.001)]
    )

    #
    length_min = models.FloatField(
        null=True, blank=True, validators=[MinValueValidator(0.001)]
    )
    length_max = models.FloatField(
        null=True, blank=True, validators=[MinValueValidator(0.001)]
    )

    #
    width_min = models.FloatField(
        null=True, blank=True, validators=[MinValueValidator(0.001)]
    )
    width_max = models.FloatField(
        null=True, blank=True, validators=[MinValueValidator(0.001)]
    )

    #
    weight_min = models.FloatField(
        null=True, blank=True, validators=[MinValueValidator(0.001)]
    )
    weight_max = models.FloatField(
        null=True, blank=True, validators=[MinValueValidator(0.001)]
    )

    def __str__(self):
        return f"{self.size} : from {self.height_min} to {self.height_max} meters"

    class Meta:
        ordering = ["height_min"]
        constraints = [
            models.UniqueConstraint(fields=["size"], name="unique_dino_size"),
            models.CheckConstraint(
                check=Q(
                    length_max__gt=F("length_min"),
                ),
                name="max_length_gt_min",
            ),
            models.CheckConstraint(
                check=Q(
                    height_max__gt=F("height_min"),
                ),
                name="max_height_gt_min",
            ),
            models.CheckConstraint(
                check=Q(
                    width_max__gt=F("width_min"),
                ),
                name="max_width_gt_min",
            ),
            models.CheckConstraint(
                check=Q(
                    weight_max__gt=F("weight_min"),
                ),
                name="max_weight_gt_min",
            ),
        ]


class EatingType(models.Model):
    """ """

    class EatingCategory(models.TextChoices):
        CARNIVORE = "C", _("Carnivore")
        HERBIVORE = "H", _("Herbivore")
        OMNIVORE = "O", _("Omnivore")

    eating_type = models.CharField(
        max_length=15,
        choices=EatingCategory.choices,
        null=False,
        blank=False,
    )

    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.eating_type}"

    class Meta:
        ordering = ["eating_type"]
        constraints = [
            models.UniqueConstraint(fields=["eating_type"], name="unique_eating_type"),
        ]

def image_directory_path(instance, filename):
    """
    where the images will be stored
    """
    folder_name = instance.name
    # period = instance.timestamp # could use also period to further put the image

    return f"images/{folder_name}/{filename}"
class Dinosaur(models.Model):
    """
    A dinosaur is a living thing that lived in the past.
    """

    name = models.CharField(null=False,max_length=250)
    period = models.ForeignKey(Period,null=True, blank=True, on_delete=models.SET_NULL)
    size = models.ForeignKey(DinoSize,null=True, blank=True, on_delete=models.SET_NULL)
    eating_type = models.ForeignKey(EatingType,null=True, blank=True, on_delete=models.SET_NULL)
    description = models.TextField(null=True, blank=True)
    #
    typical_colours = ArrayField(
        models.CharField(
            max_length=12, null=True,
        ),
        size=4,
        null=True,
    )

    # TODO add delete images if the dinosaur is deleted
    image1 = models.ImageField(
        upload_to=image_directory_path, default="img1.jpg"
    )
    image2 = models.ImageField(
        upload_to=image_directory_path, default="img2.jpg"
    )

    def __str__(self):
        return f"{self.name} : {self.period} : {self.size} : {self.eating_type}"

    class Meta:
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(fields=["name"], name="unique_dinosaur_name"),
        ]