# import random
# import pandas as pd

# # Create an empty list to store the dataset
# disability_students = []

# # Define a list of disabilities and corresponding access technology
# disabilities = [
#     {"name": "Mobility Impairment", "access_technology": "Wheelchair"},
#     {"name": "Visual Impairment", "access_technology": "Screen Reader"},
#     {"name": "Hearing Impairment", "access_technology": "Hearing Aid"},
#     {"name": "Learning Disability", "access_technology": "Text-to-Speech Software"},
#     {"name": "Autism Spectrum Disorder", "access_technology": "Communication App"},
#     {"name": "Speech Impairment", "access_technology": "Augmentative and Alternative Communication (AAC) Device"},
#     {"name": "Intellectual Disability", "access_technology": "Assistive Learning Tools"}
# ]

# # Generate 100 disability student records
# for Student_ID in range(1,101):
#     # Randomly select a disability for the student
#     student_disability = disabilities[Student_ID % len(disabilities)]

#     # Define student data
#     student = {
#         "Student_ID": f"STU{str(Student_ID).zfill(3)}",
#         "Age": random.randint(18, 30),  # You can adjust age range as needed
#         "Gender": random.choice(["Male", "Female", "Other"]),
#         "Disability": student_disability["name"],
#         "Access Technology": student_disability["access_technology"]
#     }

#     # Append the student record to the dataset
#     disability_students.append(student)

# # Convert the list of dictionaries to a Pandas DataFrame
# df = pd.DataFrame(disability_students)

# # Print the DataFrame
# df.to_csv("disability_students.csv", index=False)
# df

import random
import pandas as pd

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

disability_students = []

for Student_ID in range(1, 101):
    student = {
        "Student ID": f"STU{str(Student_ID).zfill(3)}"
    }

    student_answers = [random.choice(choices) for choices in answer_choices]

    for i, question in enumerate(questions):
        student[question] = student_answers[i]
        student[f"{question} (Correct)"] = student_answers[i] == correct_answers[i]

    student["Score"] = sum(student[f"{question} (Correct)"] for question in questions)

    if student["Score"] >= 8:
        student["Category"] = "Excellent"
    elif student["Score"] >= 6:
        student["Category"] = "Good"
    elif student["Score"] >= 4:
        student["Category"] = "Average"
    elif student["Score"] >= 2:
        student["Category"] = "Poor"
    else:
        student["Category"] = "Very Poor"

    disability_students.append(student)

df = pd.DataFrame(disability_students)
df.to_csv("student_answers.csv", index=False)
df