from django.db import models

EmploymentType = [
    ("Full Time", "Full Time"),
    ("Part Time", "Part Time"),
    ("Contract", "Contract")
]


ExperienceLevel = [
    ("Entry Level", "Entry Level"),
    ("Mid Level", "Mid Level"),
    ("Senior", "Senior"),
]


LocationTypeChoice = [
    ("Onsite", "Onsite"),
    ("Hybrid", "Hybrid"),
    ("Remote", "Remote"),
]


# All 64 districts of Bangladesh, grouped by division for readability.
BANGLADESH_DISTRICTS = [
    # Dhaka Division
    ("Dhaka", "Dhaka"),
    ("Faridpur", "Faridpur"),
    ("Gazipur", "Gazipur"),
    ("Gopalganj", "Gopalganj"),
    ("Kishoreganj", "Kishoreganj"),
    ("Madaripur", "Madaripur"),
    ("Manikganj", "Manikganj"),
    ("Munshiganj", "Munshiganj"),
    ("Narayanganj", "Narayanganj"),
    ("Narsingdi", "Narsingdi"),
    ("Rajbari", "Rajbari"),
    ("Shariatpur", "Shariatpur"),
    ("Tangail", "Tangail"),
    # Chattogram Division
    ("Bandarban", "Bandarban"),
    ("Brahmanbaria", "Brahmanbaria"),
    ("Chandpur", "Chandpur"),
    ("Chattogram", "Chattogram"),
    ("Cumilla", "Cumilla"),
    ("Cox's Bazar", "Cox's Bazar"),
    ("Feni", "Feni"),
    ("Khagrachhari", "Khagrachhari"),
    ("Lakshmipur", "Lakshmipur"),
    ("Noakhali", "Noakhali"),
    ("Rangamati", "Rangamati"),
    # Rajshahi Division
    ("Bogura", "Bogura"),
    ("Joypurhat", "Joypurhat"),
    ("Naogaon", "Naogaon"),
    ("Natore", "Natore"),
    ("Chapainawabganj", "Chapainawabganj"),
    ("Pabna", "Pabna"),
    ("Rajshahi", "Rajshahi"),
    ("Sirajganj", "Sirajganj"),
    # Khulna Division
    ("Bagerhat", "Bagerhat"),
    ("Chuadanga", "Chuadanga"),
    ("Jashore", "Jashore"),
    ("Jhenaidah", "Jhenaidah"),
    ("Khulna", "Khulna"),
    ("Kushtia", "Kushtia"),
    ("Magura", "Magura"),
    ("Meherpur", "Meherpur"),
    ("Narail", "Narail"),
    ("Satkhira", "Satkhira"),
    # Barishal Division
    ("Barguna", "Barguna"),
    ("Barishal", "Barishal"),
    ("Bhola", "Bhola"),
    ("Jhalokati", "Jhalokati"),
    ("Patuakhali", "Patuakhali"),
    ("Pirojpur", "Pirojpur"),
    # Sylhet Division
    ("Habiganj", "Habiganj"),
    ("Moulvibazar", "Moulvibazar"),
    ("Sunamganj", "Sunamganj"),
    ("Sylhet", "Sylhet"),
    # Rangpur Division
    ("Dinajpur", "Dinajpur"),
    ("Gaibandha", "Gaibandha"),
    ("Kurigram", "Kurigram"),
    ("Lalmonirhat", "Lalmonirhat"),
    ("Nilphamari", "Nilphamari"),
    ("Panchagarh", "Panchagarh"),
    ("Rangpur", "Rangpur"),
    ("Thakurgaon", "Thakurgaon"),
    # Mymensingh Division
    ("Jamalpur", "Jamalpur"),
    ("Mymensingh", "Mymensingh"),
    ("Netrokona", "Netrokona"),
    ("Sherpur", "Sherpur"),
]


class ApplicationStatus(models.TextChoices):
    APPLIED = ("APPLIED", "APPLIED")
    REJECTED = ("REJECTED", "REJECTED")
    INTERVIEW = ("INTERVIEW", "INTERVIEW")