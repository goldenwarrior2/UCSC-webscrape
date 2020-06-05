from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import json


def scrape_page(url):
    print(url)
    course_list = []
    # opening up connection, grabbing the page
    uClien = uReq(url)
    page_html = uClien.read()
    uClien.close()

    # html parsing
    page_soup = soup(page_html, "html.parser")

    # creates a list of dictionaries of length of the amount of courses
    classurls = page_soup.findAll('h2', {'class': 'course-name'})
    course_dicts = []
    for i in range(len(classurls)):
        course_dicts.append({})

    # grabs subject
    subjects = page_soup.findAll('div', id="main")
    subject = subjects[0].h1.text.strip()

    # grabs each course number
    classnumbers = page_soup.findAll('h2', {'class': 'course-name'})
    list_classnumbers = []
    list_classtitles = []
    for num in classnumbers:
        classnum = num.a.span.text.split()[1]
        list_classnumbers.append(classnum)

        # grabs each course title
        classtitle = num.a.text.split(classnum)[1].strip()
        list_classtitles.append(classtitle)

    # grabs each course's credits
    coursecreds = page_soup.findAll('div', {'class': 'credits'})
    list_coursecreds = []
    for creds in coursecreds:
        credit = creds.text.strip()
        list_coursecreds.append(credit)

    # grabs each course description
    coursedescs = page_soup.findAll('div', {'class': 'desc'})
    list_coursedescs = []
    for desc in coursedescs:
        coursedesc = desc.text.strip()
        coursedes = coursedesc.replace('  ', ' ')
        list_coursedescs.append(coursedes)

    # grabs each course's prerequisites
    list_prereqs = []
    classurls = page_soup.findAll('h2', {'class': 'course-name'})
    for i in range(len(classurls)):
        class_url = str(classurls[i].a["href"])
        class_url = 'https://catalog.ucsc.edu' + class_url
        uClient = uReq(class_url)
        page_html = uClient.read()
        uClient.close()
        page_soup = soup(page_html, "html.parser")
        extraFields = page_soup.findAll('div', {'class': 'extraFields'})
        for j in range(len(extraFields)):
            extraField = extraFields[j].p.text.strip()
            if type(extraField) == str:
                if extraField[0:3] == 'Pre' or extraField[0:3] == ',Pr':
                    prereq = extraField.strip()
                    prereq = prereq.split(': ')
                    prereqs = prereq[1].replace('  ', ' ')
                    list_prereqs.append(prereqs)
                    break
                elif extraField[0:3] == 'Enr':
                    prereq = extraField.strip()
                    prereqs = prereq.replace('  ', ' ')
                    list_prereqs.append(prereqs)
                    break
                elif extraField[0:3] == 'Con':
                    prereq = extraField.strip()
                    prereqs = prereq.replace('  ', ' ')
                    list_prereqs.append(prereqs)
                    break
            else:
                continue
        else:
            list_prereqs.append('')

    # put all of the elements into their respective dictionaries
    for i in range(len(course_dicts)):
        course_dicts[i]['subject'] = subject
        course_dicts[i]['number'] = list_classnumbers[i]
        course_dicts[i]['title'] = list_classtitles[i]
        course_dicts[i]['units'] = list_coursecreds[i]
        course_dicts[i]['prereqs'] = list_prereqs[i]
        course_dicts[i]['desc'] = list_coursedescs[i]
    # appends every dictionary to the full list of dictionaries
    for dictionary in course_dicts:
        course_list.append(dictionary)
    return course_list


def main():
    full_list = []
    my_url = 'https://catalog.ucsc.edu/Current/General-Catalog/Courses'
    # opening up connection, grabbing the page
    uClient = uReq(my_url)
    page_html = uClient.read()
    uClient.close()
    # html parsing
    page_soup = soup(page_html, "html.parser")
    list_links = []
    links = page_soup.find_all('a', href=True)
    for i in range((len(links) // 2) - 1):
        if links[i]['href'][0:36] == '/en/Current/General-Catalog/Courses/':
            link = str(links[i]['href'])
            link = 'https://catalog.ucsc.edu' + link
            list_links.append(link)
    for i in range(80):
        try:
            course_list = scrape_page(list_links[i])
        except:
            print(list_links[i])
        for course in course_list:
            full_list.append(course)
    print(full_list)
    return full_list


data = {}
data['courses'] = main()
with open('courses.json', 'w') as f:
    json.dump(data, f)







