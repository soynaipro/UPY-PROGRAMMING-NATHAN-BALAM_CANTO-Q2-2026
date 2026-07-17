# Required Structures
users = {
    'jperez': {'password': '1234', 'rol': 'student', 'name': 'Juan Pérez'},
    'dromo': {'password': '1234', 'rol': 'student', 'name': 'Daniela Romo'},
    'mjuarez': {'password': '1234', 'rol': 'student', 'name': 'Mauricio Juárez'},
    'mlopez': {'password': '1234', 'rol': 'student', 'name': 'María López'},
    'euc': {'password': '1234', 'rol': 'student', 'name': 'Ernesto Uc'},
    'cbalam': {'password': '1234', 'rol': 'student', 'name': 'Carlos Balam'},
    'jpedrozo': {'passw ord': '1234', 'rol': 'professor', 'name': 'Jorge Pedrozo'},
    'dgamboa': {'password': '1234', 'rol': 'coordinator', 'name': 'Didier Gamboa'}
}

subjects = (
    "Discrete Mathematics",
    "Programming",
    "English II",
    "Differential Calculus",
    "Probability and Statistics",
    "Computer and Server Architecture",
    "Socio-Emotional Skills and Conflict Management"
)

notes = {
    'jperez': {'Discrete Mathematics': 8.5, 'Programming': 9.2, 'English II': 9.0, 'Differential Calculus': 7.8, 'Probability and Statistics': 8.3, 'Computer and Server Architecture': 6.8, 'Socio-Emotional Skills and Conflict Management': 9.5},
    'dromo': {'Discrete Mathematics': 9.0, 'Programming': 6.7, 'English II': 9.4, 'Differential Calculus': 6.2, 'Probability and Statistics': 9.1, 'Computer and Server Architecture': 6.5, 'Socio-Emotional Skills and Conflict Management': 9.8},
    'mjuarez': {'Discrete Mathematics': 7.5, 'Programming': 8.0, 'English II': 8.5, 'Differential Calculus': 7.0, 'Probability and Statistics': 7.8, 'Computer and Server Architecture': 6.2, 'Socio-Emotional Skills and Conflict Management': 8.9},
    'mlopez': {'Discrete Mathematics': 9.5, 'Programming': 9.8, 'English II': 9.2, 'Differential Calculus': 9.0, 'Probability and Statistics': 9.6, 'Computer and Server Architecture': 9.4, 'Socio-Emotional Skills and Conflict Management': 10.0},
    'euc': {'Discrete Mathematics': 8.2, 'Programming': 6.9, 'English II': 8.8, 'Differential Calculus': 6.0, 'Probability and Statistics': 6.4, 'Computer and Server Architecture': 8.1, 'Socio-Emotional Skills and Conflict Management': 9.0},
    'cbalam': {'Discrete Mathematics': 8.8, 'Programming': 9.0, 'English II': 8.5, 'Differential Calculus': 6.6, 'Probability and Statistics': 8.9, 'Computer and Server Architecture': 8.7, 'Socio-Emotional Skills and Conflict Management': 9.2}
}

# --- 1. Login System ---
logged_in = False
current_user = ""
current_role = ""
current_name = ""

while not logged_in:
    username = input("User: ")
    password = input("Password: ")
    
    if username in users and users[username]['password'] == password:
        logged_in = True
        current_user = username
        current_role = users[username]['rol']
        current_name = users[username]['name']
        print(f"\nBienvenid@!, {current_name} ({current_role})")
    else:
        print("Invalid credentials. Please try again.\n")

# --- 2. Role Branching ---
if current_role == 'student':
    print("\nSchool Report\n")
    
    approved_subjects = set()
    
    for subj in subjects:
        grade = notes[current_user][subj]
        print(f"{subj[:26]:<27}: {grade}")
        
        if float(grade) >= 8.0:
            approved_subjects.add(subj)
            
    pending_subjects = set(subjects) - approved_subjects
    
    print(f"\nApproved: {approved_subjects}")
    print(f"Pending: {pending_subjects}\n")

elif current_role == 'professor':
    while True: 
        print("\nStudents")
        for user_id, user_data in users.items():
            if user_data['rol'] == 'student':
                print(f"User: {user_id:<10} | Student: {user_data['name']}")
                
        target_student = input("\nStudent to grade (username): ")
        
        if target_student in notes:
            print()
            for subj in subjects:
                print(subj)
                
            target_subject = input("\nSubject to grade: ")
            
            if target_subject in subjects:
                new_grade = input("New grade: ")
                old_grade = notes[target_student][target_subject]
                
                print("Do you confirm (yes/no)?")
                print(f"{target_subject}: {old_grade} ==> {new_grade}")
                confirm = input()
                
                if confirm.lower() == 'yes':
                    notes[target_student][target_subject] = new_grade if '.' not in new_grade else float(new_grade)
                    print("\nGrade updated!")
                    print(notes[target_student])
                elif confirm.lower() == 'no':
                    print("Write other thing to exit")
            else:
                print("Subject not found.")
        else:
             print("Student not found.")

elif current_role == 'coordinator':
    print("\nProfessors")
    for user_id, user_data in users.items():
        if user_data['rol'] == 'professor':
            print(f"User: {user_id:<10} | Professor: {user_data['name']}")
            
    print("\nStudents")
    student_ids = []
    for user_id, user_data in users.items():
        if user_data['rol'] == 'student':
            print(f"User: {user_id:<10} | Student: {user_data['name']}")
            student_ids.append(user_id)
            
    print("\nRecords")
    header = f"{'SUBJECTS':<13} | " + " | ".join([f"{u:<6}" for u in student_ids])
    print(header)
    
    for subj in subjects:
        row = f"{subj[:13]:<13} | "
        grades_list = []
        for s_id in student_ids:
            grades_list.append(f"{str(notes[s_id][subj]):<6}")
        row += " | ".join(grades_list)
        print(row)
    print()