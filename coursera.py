import requests
from lxml import etree
from random import shuffle
from bs4 import BeautifulSoup


def get_courses_list(url, amount_of_cources):
	courses_list = []
	url = url
	row_course_in_xml = requests.get(url).content
	root_xml = etree.fromstring(row_course_in_xml)
	for link in root_xml.iter():
		if 'loc' in link.tag:
			courses_list.append(link.text)
	shuffle(courses_list)
	return courses_list[:amount_of_cources]


def get_course_info(course_slug):
	for course in course_slug:
		response_content = requests.get(course)
		response_content.encoding = 'utf-8'
		raw_content = response_content.text	
		parsing_course = BeautifulSoup(raw_content, 'html.parser')
		course_name = parsing_course.h1.text
		course_language = parsing_course.find('div', 'rc-Language').text
		start_date = parsing_course.find('div', 'startdate')
		if start_date == None:
			start_date = 'No info'
		else:
			start_date = start_date.text 
		course_week = parsing_course.find('div', 'rc-WeekView')
		if course_week == None:
			course_week = 'No info'
		else:
			course_week = len(course_week)
		ratings = parsing_course.find('div', 'ratings-text')
		if ratings == None:
			ratings = 'No info'
		else:
			ratings = ratings.text
		print(f"""Course name : {course_name}, \n \
			language: {course_language} , \n \
			start: {start_date},  \n \
			week: {course_week}  , \n \
			rate: {ratings}""")


def output_courses_info_to_xlsx(filepath):
    pass


if __name__ == '__main__':
    url = 'https://www.coursera.org/sitemap~www~courses.xml'
    result = get_courses_list(url, 20)
    get_course_info(result)





# def get_courses_list(amount_of_cources):
#    url = "https://www.coursera.org/sitemap~www~courses.xml"
#    coursera_courses_responce = requests.get(url)  
#    coursera_courses_xml_as_bytecode = coursera_courses_responce.content
#    urlset_xml_root_object = objectify.fromstring(coursera_courses_xml_as_bytecode)
#    full_courses_list = [
#        url_object.loc.text
#        for url_object in urlset_xml_root_object.iterchildren()
#    ]
#    cources_links_list = random.sample(full_courses_list, amount_of_cources)
#    print(cources_links_list)
#    return cources_links_list

