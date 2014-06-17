import sqlite3

DB = None
CONN = None

def get_student_by_github(github):
    query = """SELECT first_name, last_name, github FROM Students WHERE github = ?"""
    DB.execute(query, (github,))
    row = DB.fetchone()
    print """\
Student: %s %s
Github account: %s"""%(row[0], row[1], row[2])

def connect_to_db():
    global DB, CONN
    CONN = sqlite3.connect("hackbright.db")
    DB = CONN.cursor()

def make_new_student(first_name, last_name, github):
    query = """INSERT into Students values (?,?,?)"""
    DB.execute(query, (first_name, last_name, github))

    CONN.commit()
    print "Successfully added student: %s %s" % (first_name, last_name)

def query_for_projects(title):
    query = """SELECT * FROM Projects WHERE title=?"""
    DB.execute(query, (title,))
    row = DB.fetchall()
    row = row[0]
    print """\
    Title: %s
    Description: %s
    Maximum Grade: %r""" % (row[0], row[1], row[2])

def make_new_project(title, description, max_grade):
    query = """INSERT into Projects values (?,?,?)"""
    DB.execute(query, (title, description, max_grade))

    CONN.commit()
    print """Successfully added:\n
    Title: %s
    Description: %s
    Maximum Grade: %s""" % (title, description, max_grade)

def get_project_grade(title, github): 
    query = """SELECT student_github, project_title, grade FROM Grades WHERE project_title = ? AND student_github = ?"""
    DB.execute(query, (title, github))
    row = DB.fetchall()
    row = row[0]
    print """\
    Title: %s
    Grade: %s
    Student: %s
    """ % (row[0], row[1], row[2])

def give_grade(github, title, grade):
    query = """ INSERT INTO Grades(student_github, project_title, grade) values (?,?,?)"""
    DB.execute(query, (github, title, grade))

    CONN.commit()
    print """Successfully added:\n
    Student: %s
    Title: %s
    Grade: %s
    """ % (github, title, grade)

def show_grades(github):
    query = """ SELECT * FROM Grades WHERE student_github = ?"""
    DB.execute(query, (github,))
    row = DB.fetchall()
    for item in row:
        print """\
        Title: %s
        Grade: %s
        ***********""" % (item[1], item[2])

def main():
    connect_to_db()
    command = None
    while command != "quit":
        input_string = raw_input("HBA Database> ")
        tokens = input_string.split()
        command = tokens[0]
        args = tokens[1:]

        if command == "student":
            get_student_by_github(*args) 
        elif command == "new_student":
            make_new_student(*args)
        elif command == "get_project_by_title":
            query_for_projects(*args)
        elif command == "add_project":
            args = " ".join(args).split(', ') # undoing seperation by spaces, changing to seperating by commas.
            make_new_project(*args)
        elif command == "get_grade_for_project":
            get_project_grade(*args)
        elif command == "give_grade_for_project":
            give_grade(*args)       
        elif command == "show_grades":
            show_grades(*args)

    CONN.close()

if __name__ == "__main__":
    main()