import random
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker

from accounts.models import User
from application_tracking.enums import (
    BANGLADESH_DISTRICTS,
    EmploymentType,
    ExperienceLevel,
    LocationTypeChoice,
)
from application_tracking.models import JobAdvert

fake = Faker()

JOB_TITLES = [
    "Software Engineer", "Backend Developer", "Frontend Developer",
    "Full Stack Developer", "Data Analyst", "Data Scientist",
    "DevOps Engineer", "QA Engineer", "Product Manager",
    "UI/UX Designer", "Mobile App Developer", "Machine Learning Engineer",
    "Business Analyst", "Marketing Executive", "Content Writer",
    "HR Executive", "Graphic Designer", "Network Administrator",
]

SKILLS_POOL = [
    "Python", "Django", "JavaScript", "React", "SQL", "Git",
    "Docker", "AWS", "Figma", "Node.js", "REST API", "Java",
    "C++", "Excel", "Communication", "Project Management",
]


class Command(BaseCommand):
    help = "Bulk-create fake JobAdvert records for testing/demo purposes."

    def add_arguments(self, parser):
        parser.add_argument(
            "--count", type=int, default=20,
            help="How many adverts to create (default: 20)",
        )
        parser.add_argument(
            "--created-by", type=str, default=None,
            help="Email of the User to set as created_by (must already exist). "
                 "If omitted, adverts are created without an owner.",
        )
        parser.add_argument(
            "--unpublished", action="store_true",
            help="Create adverts as unpublished (is_published=False) instead of published.",
        )

    def handle(self, *args, **options):
        count = options["count"]
        created_by_email = options["created_by"]
        is_published = not options["unpublished"]

        owner = None
        if created_by_email:
            owner = User.objects.filter(email=created_by_email).first()
            if not owner:
                self.stderr.write(
                    self.style.ERROR(f"No user found with email: {created_by_email}")
                )
                return

        adverts = []
        for _ in range(count):
            skills = ", ".join(random.sample(SKILLS_POOL, k=random.randint(3, 6)))
            adverts.append(
                JobAdvert(
                    title=random.choice(JOB_TITLES),
                    company_name=fake.company(),
                    employment_type=random.choice(EmploymentType)[0],
                    experience_level=random.choice(ExperienceLevel)[0],
                    job_type=random.choice(LocationTypeChoice)[0],
                    description=fake.paragraph(nb_sentences=6),
                    location=random.choice(BANGLADESH_DISTRICTS)[0],
                    skills=skills,
                    deadline=timezone.now().date() + timedelta(days=random.randint(7, 60)),
                    is_published=is_published,
                    created_by=owner,
                )
            )

        JobAdvert.objects.bulk_create(adverts)

        self.stdout.write(
            self.style.SUCCESS(f"Created {count} job advert(s).")
        )
