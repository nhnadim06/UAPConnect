from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils import timezone

from accounts.models import User
from common.models import BaseModel

from .enums import BANGLADESH_DISTRICTS, ApplicationStatus, EmploymentType, ExperienceLevel, LocationTypeChoice


class JobAdvertQuerySet(models.QuerySet):
    def active(self):
        today = timezone.now().date()
        return self.filter(is_published=True, deadline__gte=today)

    def search(self, keyword: str = "", location: str = ""):
        filters = Q()

        if keyword:
            filters &= (
                Q(title__icontains=keyword)
                | Q(company_name__icontains=keyword)
                | Q(description__icontains=keyword)
                | Q(skills__icontains=keyword)
            )

        if location:
            filters &= Q(location__icontains=location)

        return self.active().filter(filters)


class JobAdvert(BaseModel):
    title = models.CharField(max_length=150)
    company_name = models.CharField(max_length=150)
    employment_type = models.CharField(max_length=50, choices=EmploymentType)
    experience_level = models.CharField(max_length=50, choices=ExperienceLevel)
    job_type = models.CharField(max_length=50, choices=LocationTypeChoice)
    description = models.TextField()
    location = models.CharField(
        max_length=50, choices=BANGLADESH_DISTRICTS, null=True, blank=True
    )
    skills = models.CharField(max_length=255)
    deadline = models.DateField()
    is_published = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True
    )

    objects = JobAdvertQuerySet.as_manager()

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.title} @ {self.company_name}"

    def publish_advert(self) -> None:
        self.is_published = True
        self.save(update_fields=["is_published"])

    @property
    def total_applicants(self) -> int:
        return self.applications.count()

    @property
    def pending_applications_count(self) -> int:
        return self.applications.filter(status=ApplicationStatus.APPLIED).count()

    def get_absolute_url(self):
        return reverse("job_advert", kwargs={"advert_id": self.id})


class JobApplication(BaseModel):
    job_advert = models.ForeignKey(
        JobAdvert, related_name="applications", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=50)
    email = models.EmailField()
    portfolio_url = models.URLField()
    cv = models.FileField()
    status = models.CharField(
        max_length=20,
        choices=ApplicationStatus.choices,
        default=ApplicationStatus.APPLIED,
    )
    # Whether the applicant has viewed the latest status change.
    decision_seen = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} -> {self.job_advert.title}"
