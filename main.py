import os
import csv

"""
student columns: user_id, user_name, state
course columns: course_id, course_name, state
enrollment columns: user_id, course_id, state

For all data types, state is in ['active', 'deleted']. The user_id and course_id are globally unique,
so a new id means a new record, an id they've seen before means an update to an existing record.

Attached is a .zip of CSVs. You should write a program that processes the files in order. You'll need to
determine the type of data in the csv based on the headers in the first row. At the end, you need to spit
out a list of active courses, and for each course a list of active students with active enrollments in that course.

Some gotchas:

Some of the enrollments are invalid (reference non-existing user or course).
Watch out for quoting problems if you try to parse the CSVs by hand
An active enrollment might point to a deleted user, and enrollments may be deleted as well.
Column order in the CSV is unspecified, one user csv may be ordered differently than the next.
"""

CSV_DIR = './csvs/'


def main():

    users = []
    users_clean = []
    users_delete = []
    courses = []
    courses_clean = []
    courses_deleted = []
    user_courses = []
    user_courses_clean = []
    user_courses_deleted = []

    # First open sorted csv's and parse data into lists
    for f in sorted(os.listdir(CSV_DIR)):
        with open(CSV_DIR + f, 'rb') as csvfile:
            data = csv.reader(csvfile)
            headers = data.next()

            if 'user_name' in headers:
                users.extend( _format_data(headers, data) )

            elif 'course_name' in headers:
                courses.extend( _format_data(headers, data))

            else:
                user_courses.extend( _format_data(headers, data) )

    # Next remove 'deleted' records
    users_clean, users_delete = _remove_deleted(users)
    courses_clean, courses_deleted = _remove_deleted(courses)
    user_courses_clean, user_courses_deleted = _remove_deleted(user_courses)



def _format_data(headers, data):
    data_list = []
    for row in data:
        data_dict = {}
        for i, col in enumerate(row):
            data_dict[headers[i]] = col
        data_list.append(data_dict)
    return data_list


def _remove_deleted(original):
    clean = []
    deleted = []
    for rec in original:
        if rec['state'] == 'deleted':
            deleted.append(rec)
        else:
            clean.append(rec)

    return clean, deleted


main()
