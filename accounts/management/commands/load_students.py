import csv
from django.core.management.base import BaseCommand
from accounts.models import Student
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Load student data from CSV file'

    def handle(self, *args, **kwargs):
        csv_file = 'disability_students.csv' 
        with open(csv_file, 'r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                Student.objects.create(
                    std_id=row['Student_ID'],
                    age=row['Age'],
                    gender=row['Gender'],
                    disability=row['Disability'],
                    accesstechnology=row['Access Technology'],
                    
                )
        self.stdout.write(self.style.SUCCESS('Student data loaded successfully'))