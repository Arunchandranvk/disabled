# import os
# import django

# # Set up Django environment
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'disabledstudents.settings')
# django.setup()


# import random
# from django.core.management.base import BaseCommand
# from accounts.models import Student  # Import the model
# from django.db import transaction

# # ... (Your existing code for generating student data)
# class Command(BaseCommand):
#     def handle(self, *args, **kwargs):
#         disability_students = []
#         # Save the records to the database
#         with transaction.atomic():
#             for student_data in disability_students:
#                 Student.objects.create(
#                     std_id=student_data["Student_ID"],
#                     age=student_data["Age"],
#                     gender=student_data["Gender"],
#                     disability=student_data["Disability"],
#                     accesstechnology=student_data["Access Technology"]
#                 )



import csv
from django.core.management.base import BaseCommand
from accounts.models import Student
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Load student data from CSV file'

    def handle(self, *args, **kwargs):
        csv_file = 'disability_students.csv'  # Specify the path to your CSV file
        # csv_file2 = 'student_answers.csv'  # Specify the path to your CSV file

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
        # with open(csv_file2, 'r') as file:
        #     csv_reader = csv.DictReader(file)
        #     for row in csv_reader:
        #         Student.objects.create(
        #             Std=row['Student_ID'],
        #             Math_Result=row['What is 2 + 2?'],
        #             Vowels=row['Who was the first President of the United States?'],
        #             Powerhouse_of_Cell=row['Who was the first President of the United States? '],
        #             Unit_of_Force=row[''],
        #             hemical_Symbol_of_Gold=row[''],
        #             Father_of_the_Nation=row[''],
        #             Founder_of_Computer=row[''],
        #             Music_Notation_of_Piano=row[''],
        #             Contour_Line_in_Drawing=row[''],
        #             World_War_Started_Year=row[''],
        #             Score=row[''],
        #             Score_Category=row[''],

        #         )        


               

        self.stdout.write(self.style.SUCCESS('Student data loaded successfully'))