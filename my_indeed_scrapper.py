import csv
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import shutil, os

# template = 'https://www.indeed.com/jobs?q={}&l={}'
def get_url(position, location):
    """
    Generate a URL from position and location
    """

    template = 'https://www.indeed.com/jobs?q={}&l={}'
    url = template.format(position, location)
    return url

def get_record(card):
    """
    Extract Job data from a single Job Post
    """
    atag = card.h2.a
    # title
    try:
        job_title = atag.get('title')
    except:
        job_title = ''
    # link
    try:
        job_link = 'https://www.indeed.com'+atag.get('href')
    except:
        job_link = ''
    # company
    try:
        job_company = card.find('span', 'company').text.strip()
    except:
        job_company = ''
    # location
    try:
        job_location = card.find('div', 'recJobLoc').get('data-rc-loc')
    except:
        job_location = ''
    # summary
    try:
        job_summary = card.find('div', 'summary').text.strip()
    except:
        job_summary = ''
    # post date
    try:
        post_date = card.find('span', 'date').text
    except:
        post_date = ''
    # today date
    try:
        today_date = datetime.today().strftime('%Y-%m-%d')
    except:
        today_date = ''
    # salary
    try:
        job_salary = card.find('span', 'salaryText').text.strip()
    except:
        job_salary = ''
    # remote job
    try:
        job_remote = card.find('span', 'remote').text.strip()
    except:
        job_remote = ''
    # rating
    try:
        job_rating = card.find('span', 'ratingsContent').text.strip()
    except:
        job_rating = ''

    result = (
        job_title,
        job_salary,
        job_company,
        job_location,
        job_remote,
        job_rating,
        job_summary, 
        post_date, 
        today_date, 
        job_link
        )
    return result

def extract(position, location):
    """
    Run 
    """
    url = get_url(position, location)
    print(url)
    records = []

    while True:
        response = requests.get(url)
        # print(response.reason) # Expected to be OK
        # print(response.text)
        soup = BeautifulSoup(response.text, 'html.parser' )
        # print(soup)
        cards = soup.find_all('div', 'jobsearch-SerpJobCard')

        # print(len(cards))

        for card in cards:
            rec = get_record(card)
            records.append(rec)
        try:
            url = 'https://www.indeed.com' + soup.find('a', {'aria-label': 'Next'}).get('href')
        except AttributeError:
            break
    print(len(records))
    with open("./outputs/job_postings_data_scientist_"+location+".csv", mode= 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['job_title','salary', 'company', 'location','is_remote', 'job_rating', 'job_summary', 'post_date', 'extract_date', 'job_url'])
        writer.writerows(records)

    # store_path = 'outputs'
    # if not os.path.isdir(store_path):
    #     os.makedirs('store_path')
    #     shutil.move(writer,store_path)
    # else:
    #     shutil.move(writer,store_path)

cities = [
    # 'Austin, TX',
    #         'Dallas, TX',
    #         'Raleigh, NC',
    #         'San Jose, CA',
    #         'Sunnyvale, CA',
    #         'Santa Clara, CA',
    #         'Charlotte, NC',
    #         'Seattle, WA',
    #         'San Francisco',
    #         'Oakland, CA',
            'Hayward, CA',
            'Atlanta, GA',
            'Huntsville, AL',
            'Denver, CO',
            'Washington, D.C.',
            'Boulder, CO',
            'Durham, NC',
            'Columbus, OH',
            'Colorado Springs, CO',
            'Boston, MA',
            'Baltimore, MD',
            'Madison, WI',
            'San Diego, CA',
            'Trenton, NJ',
            'Los Angeles, CA',
            'Houston, TX',
            'New York, NY']

for i in cities:
    extract('data scientist', i)

# url = get_url('senior accountant', 'charlotte nc')

# response = requests.get(url)
# # print(response.reason) # Expected to be OK

# soup = BeautifulSoup(response.text, 'html.parser' )
# cards = soup.find_all('div', 'jobsearch-SerpJobCard')

# print(len(cards))

# records = []

# for card in cards:
#     rec = get_record(card)
#     records.append(rec)

# print(records[0:3])

# while True:
#     try:
#         url = 'https://www.indeed.com' + soup.find('a', {'aria-label': 'Next'}).get('href')
#     except AttributeError:
#         break

#     response = requests.get(url)
#     # print(response.reason) # Expected to be OK

#     soup = BeautifulSoup(response.text, 'html.parser' )
#     cards = soup.find_all('div', 'jobsearch-SerpJobCard')

#     # print(len(cards))

#     for card in cards:
#         rec = get_record(card)
#         records.append(rec)

# print(len(records))

