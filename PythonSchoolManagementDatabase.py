import sqlite3

connection = sqlite3.connect('mydatabase.db')

sql = connection.cursor()

sql.execute('CREATE TABLE IF NOT EXISTS students'
            '(id INTEGER PRIMARY KEY AUTOINCREMENT, '
            'first_name TEXT,'
            'last_name TEXT, '
            'age INTEGER,'
            'grade REAL);')


# sql.execute('DROP TABLE students')
def add_student():
    print('\n      New Student')
    first_name = input('\nFirst Name: ').capitalize()
    last_name = input('Last Name: ').capitalize()
    if first_name.isalpha() and last_name.isalpha():
        age = input('Age: ')
        if age.isdigit():
            grade = input('Grade: ')
            try:
                grade = float(grade)
                new_student = sql.execute('INSERT INTO students'
                                          '(first_name, last_name, age, grade)'
                                          ' VALUES(?, ?, ?, ?)',
                                          (first_name, last_name, age, grade))
                if new_student:
                    print('^' * 35)
                    print('\nStudent successfully added!')
                    connection.commit()
                else:
                    print('\nError could not add student to the database!')
                    return
            except ValueError:
                print('\nError invalid grade!')
                return
        else:
            print('\nError invalid age!')
            return
    else:
        print('\nError invalid name!')
        return


def get_student_by_name():
    print()
    print('*' * 35)
    first_name = input('\n        Search\n'
                       '\nFirstname: ').capitalize()
    if first_name.isalpha():
        last_name = input('Lastname: ').capitalize()
        if last_name.isalpha():
            print('-' * 35)
            sql.execute('SELECT * FROM students '
                        'WHERE first_name = ? or last_name = ?',
                        (first_name, last_name))
            students = sql.fetchall()
            if students:
                print('\n       Search results')
                for each_student in students:
                    print('-' * 35)
                    print(f'Student Id: {each_student[0]}\n'
                          f'First Name: {each_student[1]}\n'
                          f'Last Name: {each_student[2]}\n'
                          f'Age: {each_student[3]}\n'
                          f'Grade: {each_student[4]}\n')
                    connection.commit()
            else:
                print('\nError student not found!')
                return
        else:
            print('\nError invalid last name!')
            return
    else:
        print('\nError invalid first name!')
        return


def show_all_students():
    sql.execute('SELECT * FROM students')
    all_students = sql.fetchall()
    if all_students:
        print('-' * 35)
        print('       All students')
        count = 0
        for each_student in all_students:
            print('-' * 35)
            print(f'Student Id: {each_student[0]}\n'
                  f'First Name: {each_student[1]}\n'
                  f'Last Name: {each_student[2]}\n'
                  f'Age: {each_student[3]}\n'
                  f'Grade: {each_student[4]}\n')
            connection.commit()
            count += 1
        print('-' * 35)
        if count == 0:
            print('\nNo students')
            return
        elif count == 1:
            print(f'Total: {count} student')
            return
        else:
            print(f'Total: {count} students')
            return

    return all_students


def update_student_grade():
    print()
    print('-' * 35)
    print('        Edit Student')
    first_name = input('\nFirst Name: ').capitalize()
    if first_name.isalpha():
        student_id = input('Student Id: ')
        if student_id.isdigit():
            student_id = int(student_id)
            new_grade = input('New grade: ')
            try:
                new_grade = float(new_grade)
                student = sql.execute('SELECT * FROM students'
                                      ' WHERE first_name = ? or id = ?', (first_name, student_id)).fetchone()
                if student:
                    sql.execute('UPDATE students SET grade = ? WHERE first_name = ? OR id = ?',
                                (new_grade, first_name, student_id))
                    connection.commit()
                    sql.execute('SELECT * FROM students WHERE first_name = ? OR id = ?', (first_name, student_id))
                    updated_student = sql.fetchone()
                    print('-' * 35)
                    print('      Changes are saved')
                    print(f'\nStudent Id: {updated_student[0]}\n'
                          f'First Name: {updated_student[1]}\n'
                          f'Last Name: {updated_student[2]}\n'
                          f'Age: {student[3]}\n'
                          f'Grade: {updated_student[4]}\n')
                    return student
                else:
                    print('\nError: student not found!')
            except ValueError:
                print('\nError: invalid grade!')
        else:
            print('\nError: invalid Student Id!')
    else:
        print('\nError: invalid First Name!')


def delete_student():
    print()
    print('-' * 35)
    print('        Delete Student')
    first_name = input('\nFirst Name: ').capitalize()
    if first_name.isalpha():
        student_id = input('Student Id: ')
        if student_id.isdigit():
            student_id = int(student_id)
            sql.execute('DELETE FROM students '
                        'WHERE first_name = ? or id = ?',
                        (first_name, student_id))
            if sql.rowcount > 0:
                connection.commit()
                print('-' * 35)
                print('\nStudent successfully deleted! ')

            else:
                print('\nError student not found')
                return
        else:
            print('\nError invalid student id!')
            return
    else:
        print('\nError invalid student name!')
        return


while True:
    print()
    print('*' * 45)
    student_type = input('\n      Students Database!\n'
                         '\n1. Add a new student\n'
                         '2. Search student\n'
                         '3. All students\n'
                         '4. Edit student grade\n'
                         '5. Delete student\n'
                         '6. Exit\n'
                         '--------------------------\n'
                         'Type in number::: ')
    if student_type == '1':
        add_student()
    elif student_type == '2':
        get_student_by_name()
    elif student_type == '3':
        show_all_students()
    elif student_type == '4':
        update_student_grade()
    elif student_type == '5':
        delete_student()
    elif student_type == '6':
        connection.close()
        print('\nExit')
        exit(0)
    else:
        print('\nError invalid symbol!')
