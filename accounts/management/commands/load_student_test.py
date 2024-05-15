import random
from django.core.management.base import BaseCommand
from accounts.models import  Student, Question, Answer, StudentAnswer, Category,Suggestion,CustUser

class Command(BaseCommand):
    # help = 'Populate the database with synthetic data'
   
    def handle(self, *args, **kwargs):
        disabilities = [
            {"name": "Mobility Impairment", "access_technology": "Wheelchair"},
            {"name": "Visual Impairment", "access_technology": "Screen Reader"},
            {"name": "Hearing Impairment", "access_technology": "Hearing Aid"},
            {"name": "Learning Disability", "access_technology": "Text-to-Speech Software"},
            {"name": "Autism Spectrum Disorder", "access_technology": "Communication App"},
            {"name": "Speech Impairment", "access_technology": "Augmentative and Alternative Communication (AAC) Device"},
            {"name": "Intellectual Disability", "access_technology": "Assistive Learning Tools"}
        ]
        questions = [
                    "What is 2 + 2?",
                    "Who was the first President of the United States?",
                    "What is the chemical symbol for water?",
                    "What is the capital of France?",
                    "What is the past tense of 'eat'?",
                    "Who painted the Mona Lisa?",
                    "What instrument does Yo-Yo Ma play?",
                    "Which sport uses a shuttlecock?",
                    "What gas do plants absorb from the air?",
                    "What company developed the iPhone?"
                ]
        answer_choices = [
                            ["3", "4", "5"],
                            ["George Washington", "Thomas Jefferson", "John Adams"],
                            ["H2O", "CO2", "NaCl"],
                            ["London", "New York", "Paris"],
                            ["Ate", "Eaten", "Eating"],
                            ["Leonardo da Vinci", "Pablo Picasso", "Vincent van Gogh"],
                            ["Violin", "Cello", "Piano"],
                            ["Tennis", "Badminton", "Soccer"],
                            ["Oxygen", "Carbon dioxide", "Nitrogen"],
                            ["Samsung", "Apple", "Google"]
                        ]
        
        correct_answers = [
                            "4",
                            "George Washington",
                            "H2O",
                            "Paris",
                            "Ate",
                            "Leonardo da Vinci",
                            "Cello",
                            "Badminton",
                            "Carbon dioxide",
                            "Apple"
                        ]
        for Student_ID in range(1, 101):
            student_disability = disabilities[Student_ID % len(disabilities)]

            student = Student.objects.create(
                std_id=f"STU{str(Student_ID).zfill(3)}",
                age=random.randint(6, 19),
                gender=random.choice(["Male", "Female"]),
                disability=student_disability["name"],
                accesstechnology=student_disability["access_technology"]
            )
            
            all_answers=list(Answer.objects.all())
            if len(all_answers) < len(questions):
                questions = random.sample(questions, len(all_answers))
        
            random.shuffle(all_answers)
            student_answers = random.sample(all_answers, len(questions))

            for i, question in enumerate(questions):
                StudentAnswer.objects.create(
                    student=student,
                    question=Question.objects.get(text=question),
                    answer=student_answers[i]
                )

            score = StudentAnswer.objects.filter(student=student, answer__is_correct=True).count()
            # category = Category.objects.filter(name__in=["Very Poor", "Poor", "Average", "Good", "Excellent"])
            # .filter(id__gte=score).first()
            #  if category== "Very Poor":
            # cat = Category.objects.all()
            sug=Suggestion.objects.all()

            if score >= 8:
                student.category = "Excellent"
                for i in sug:
                   if i.cat.name == "Excellent":
                      student.suggestion= i.suggestion
                      student.video=i.video
                      student.audio=i.audio
            elif score >= 6:
                student.category = "Good"
                for i in sug:
                   if i.cat.name == "Good":
                    student.suggestion= i.suggestion
                    student.video=i.video
                    student.audio=i.audio
           
            elif score>= 4:
                student.category = "Average"
                for i in sug:
                   if i.cat.name == "Average":
                    student.suggestion= i.suggestion
                    student.video=i.video
                    student.audio=i.audio
           
            elif score >= 2:
                student.category = "Poor"
                for i in sug:
                   if i.cat.name == "Poor":
                    student.suggestion= i.suggestion
                    student.video=i.video
                    student.audio=i.audio
        
            else:
                student.category = "Very Poor"
                for i in sug:
                   if i.cat.name == "Very Poor":
                    student.suggestion= i.suggestion
                    student.video=i.video
                    student.audio=i.audio
          
                

            # if student.category is not None:
            #     student.category = category.name  # Assign the category's name as a string
            # else:
            #     student.category = "Unknown"
            student.score=score
            student.save()







# import random
# from django.core.management.base import BaseCommand
# from accounts.models import Student, Question, AnswerChoice, CorrectAnswer

# class Command(BaseCommand):
#     help = 'Populate the database with synthetic data'

#     def handle(self, *args, **kwargs):
#         questions = [
#             "What is 2 + 2?",
#             "Who was the first President of the United States?",
#             "What is the chemical symbol for water?",
#             "What is the capital of France?",
#             "What is the past tense of 'eat'?",
#             "Who painted the Mona Lisa?",
#             "What instrument does Yo-Yo Ma play?",
#             "Which sport uses a shuttlecock?",
#             "What gas do plants absorb from the air?",
#             "What company developed the iPhone?"
#         ]

#         answer_choices = [
#             ["3", "4", "5"],
#             ["George Washington", "Thomas Jefferson", "John Adams"],
#             ["H2O", "CO2", "NaCl"],
#             ["London", "New York", "Paris"],
#             ["Ate", "Eaten", "Eating"],
#             ["Leonardo da Vinci", "Pablo Picasso", "Vincent van Gogh"],
#             ["Violin", "Cello", "Piano"],
#             ["Tennis", "Badminton", "Soccer"],
#             ["Oxygen", "Carbon dioxide", "Nitrogen"],
#             ["Samsung", "Apple", "Google"]
#         ]

#         correct_answers = [
#             "4",
#             "George Washington",
#             "H2O",
#             "Paris",
#             "Ate",
#             "Leonardo da Vinci",
#             "Cello",
#             "Badminton",
#             "Carbon dioxide",
#             "Apple"
#         ]
#         disabilities = [
#                 {"name": "Mobility Impairment", "access_technology": "Wheelchair"},
#                 {"name": "Visual Impairment", "access_technology": "Screen Reader"},
#                 {"name": "Hearing Impairment", "access_technology": "Hearing Aid"},
#                 {"name": "Learning Disability", "access_technology": "Text-to-Speech Software"},
#                 {"name": "Autism Spectrum Disorder", "access_technology": "Communication App"},
#                 {"name": "Speech Impairment", "access_technology": "Augmentative and Alternative Communication (AAC) Device"},
#                 {"name": "Intellectual Disability", "access_technology": "Assistive Learning Tools"}
#             ]
#         for Student_ID in range(1, 101):
#            student_disability = disabilities[Student_ID % len(disabilities)]

#         disability_students = []

#         for Student_ID in range(1, 101):
#             student = Student.objects.create(
#                 std_id=f"STU{str(Student_ID).zfill(3)}",
#                  age= random.randint(6, 19),
#                 gender= random.choice(["Male", "Female"]),
#                 disability= student_disability["name"],
#                 accesstechnology= student_disability["access_technology"],
#                 score=0,  # Initialize score to 0
#                 category="Not Calculated"  # Initialize category to some default value
#             )

#             for i, question_text in enumerate(questions):
#                 question = Question.objects.create(text=question_text)
#                 correct_answer_text = correct_answers[i]
#                 correct_answer = CorrectAnswer.objects.create(question=question, text=correct_answer_text)

#                 for answer_choice_text in answer_choices[i]:
#                     answer_choice = AnswerChoice.objects.create(question=question, text=answer_choice_text)

#         self.stdout.write(self.style.SUCCESS('Successfully populated the database.'))