import requests
from lxml import etree
from random import shuffle
from bs4 import BeautifulSoup
from openpyxl import Workbook
import argparse


def get_courses_list(url, amount_of_course):
    courses_list = []
    row_course_in_xml = requests.get(url).content
    root_xml = etree.fromstring(row_course_in_xml)
    for link in root_xml.iter():
        if 'loc' in link.tag:
            courses_list.append(link.text)
    shuffle(courses_list)
    return courses_list[:amount_of_course]


def get_course_info(course_slug):
    courses_info = {}
    for course in course_slug:
        response_content = requests.get(course)
        response_content.encoding = 'utf-8'
        raw_content = response_content.text
        parsing_course = BeautifulSoup(raw_content, 'html.parser')
        course_name = parsing_course.h1.text
        course_language = parsing_course.find('div', 'rc-Language').text
        start_date = parsing_course.find('div', 'startdate')
        if start_date is None:
            start_date = 'No info'
        else:
            start_date = start_date.text
        amount_week = parsing_course.find('div', 'rc-WeekView')
        if amount_week is None:
            amount_week = 'No info'
        else:
            amount_week = len(amount_week)
        ratings = parsing_course.find('div', 'ratings-text')
        if ratings is None:
            ratings = 'No info'
        else:
            ratings = ratings.text
        courses_info.update({
        	course: {
            'course name': course_name,
            'course language': course_language,
            'start date': start_date,
            'number of week': amount_week,
            'ratings': ratings,
        }})
    return courses_info


def output_courses_info_to_xlsx(courses_info):
    xls_file = Workbook()
    sheet = xls_file.active
    for row, course in enumerate(courses_info, start=1):
        for column, description in enumerate(courses_info[course], start=1):
            sheet.cell(
                row=row,
                column=column).value = courses_info[course][description]
    xls_file.save('courses_info.xlsx')


def main():
    argument = argparse.ArgumentParser(description='Amount courses')
    argument.add_argument('-c', dest='courses', default=20, type=int,
    	help='Input amount courses you need')
    args = argument.parse_args()
    print(args.courses)
    url = 'https://www.coursera.org/sitemap~www~courses.xml'
    courses_list = get_courses_list(url, args.courses)
    course_info = get_course_info(courses_list)
    output_courses_info_to_xlsx(course_info)


if __name__ == '__main__':
    main()
