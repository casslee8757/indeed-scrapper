import requests
from bs4 import BeautifulSoup

def get_last_pages(url):
  
  result = requests.get(url)
  soup = BeautifulSoup(result.text, 'html.parser')
  
  pagination = soup.find('ul', {'class': 'pagination-list'})
  links = pagination.find_all('a')
  
  pages = []
  for page in links[:-1]:
    pages.append(int(page.string))
  
  max_page = pages[-1]
  return max_page

def extract_job(html):
  title = html.find('h2', {'class': 'jobTitle'}).find('span', title=True).text
  company = html.find('span', {'class':'companyName'})
  if company is not None:
    company = company.string
  else:
    company = None 
    print(title, company)
  location = html.find('div', {'class': 'companyLocation'}).string
  job_id = html.find('a')['data-jk']
  return {
    'title': title, 
    'company': company, 
    'location': location, 
    'link': f"https://au.indeed.com/viewjob?jk={job_id}&from=web&vjs=3"
  }
    

def extract_jobs(last_page, url):
  jobs = []
  for page in range(last_page):
    print(f"Scrapping page {page}")
    result = requests.get(f"{url}&start={page+1}")
    soup = BeautifulSoup(result.text, 'html.parser')
    results = soup.find_all('div', {'class':'job_seen_beacon'})
    for result in results:
      job = extract_job(result)
      jobs.append(job)
  return jobs

def get_jobs(word):
  url = f'https://au.indeed.com/jobs?q={word}'
  last_page = get_last_pages(url)
  jobs = extract_jobs(last_page, url)
  return jobs