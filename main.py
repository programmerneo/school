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
    good_user_courses = []

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

    # Next remove duplicates, i.e. updates
    users = _remove_duplicates('user_id', users)
    courses = _remove_duplicates('course_id', courses)
    user_courses = _remove_duplicates_user_courses(user_courses)

    # Next remove 'deleted' records
    users_clean, users_delete = _remove_deleted(users)
    courses_clean, courses_deleted = _remove_deleted(courses)
    user_courses_clean, user_courses_deleted = _remove_deleted(user_courses)

    # remove bad records where user or course was deleted
    good_user_courses = _remove_bad_user_courses(user_courses_clean, users_delete, courses_deleted)

    print 'Good Users'
    print users_clean
    print '________________________________________'
    print 'Good Courses'
    print courses_clean
    print '________________________________________'
    print 'Good User - Courses'
    print good_user_courses

    _print_output(users_clean, courses_clean, good_user_courses)


def _format_data(headers, data):
    data_list = []
    for row in data:
        data_dict = {}
        for i, col in enumerate(row):
            data_dict[headers[i]] = col
        data_list.append(data_dict)
    return data_list


def _remove_duplicates(key, data):
    return {rec[key]: rec for rec in data}.values()


def _remove_duplicates_user_courses(data):
    two_keys_dict = {}
    clean = []

    for rec in data:
        key = (rec['user_id'], rec['course_id'])
        two_keys_dict[key] = rec
        two_keys_dict[key]['state'] = rec['state']

    for k, v in two_keys_dict.iteritems():
        clean.append(v)

    return clean


def _remove_deleted(original):
    clean = []
    deleted = []
    for rec in original:
        if rec['state'] == 'deleted':
            deleted.append(rec)
        else:
            clean.append(rec)

    return clean, deleted


def _remove_bad_user_courses(user_courses_clean, users_deleted, courses_deleted):
    good_user_courses = []

    users_delete_list = [u_d['user_id'] for u_d in users_deleted]
    courses_deleted_list = [c_d['course_id'] for c_d in courses_deleted]

    for u_c_c in user_courses_clean:
        if u_c_c['user_id'] != users_delete_list and u_c_c['course_id'] != courses_deleted_list:
            good_user_courses.append(u_c_c)

    return good_user_courses

def _print_output(users_clean, courses_clean, good_user_courses):
    course_list = [c['course_id'] for c in good_user_courses]
    user_list = [u['user_id'] for u in good_user_courses]
    for c in courses_clean:
        if c['course_id'] in course_list:
            print '________________________________________'
            print c['course_name']
            print '________________________________________'
            for u in users_clean:
                if u['user_id'] in user_list:
                    print u['user_name']
main()
