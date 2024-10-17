import requests
from bs4 import BeautifulSoup
import re
import aiohttp
import asyncio
import pandas as pd

async def fetch(session, url, headers):
    try:
        async with session.get(url, headers=headers) as response:
            print(f"Fetching {url}, Status: {response.status}")  # Debugging line
            if response.status == 200:
                text = await response.text()  # Or response.json() for JSON responses
                return text
            else:
                print(f"Failed to fetch {url}, Status: {response.status}")
                return None
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

# Function to send multiple GET requests concurrently, with headers
async def fetch_all(urls, headers):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            tasks.append(fetch(session, url, headers))  # Pass headers
        responses = await asyncio.gather(*tasks)
        return responses

urls = ['https://www.redfin.com/city/22034/VA/Chantilly/apartments-for-rent/filter/max-price=5k,min-beds=3,min-baths=2,min-sqft=1500,viewport=38.92925:38.74473:-77.0766:-77.42575,mr=6:24355+6:21282+6:6790,cats-allowed,has-parking,move-in-date=2%2F15%2F2025']

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0'}

response = requests.get(urls[0], headers=headers)
print("Status code: " + str(response.status_code))

#parse the HTML
soup = BeautifulSoup(response.text, 'html.parser')

number_of_results = int(soup.find('div', class_='homes summary reversePosition').text[:3].strip())

number_of_pages = number_of_results // 40 + 1

for page in range(number_of_pages-1):
    url_page = urls[0] + '/page-' + str(page+2)
    urls.append(url_page)

houses_list = []

count = 1

for url in urls:
    
    response = requests.get(url, headers=headers)
    print("Status code: " + str(response.status_code))
    
    #parse the HTML
    soup = BeautifulSoup(response.text, 'html.parser')
    
    pattern = re.compile(r'^MapHomeCard_\d+$')

    #find all the houses with the regex
    houses = soup.find_all('div', id=pattern)
    
    for house in houses:
        
        price = house.find('span', class_='bp-Homecard__Price--value').text
        
        number_of_rooms = house.find('span', class_='bp-Homecard__Stats--beds text-nowrap').text
        
        number_of_baths = house.find('span', class_='bp-Homecard__Stats--baths text-nowrap').text   
        
        size = house.find('span', class_='bp-Homecard__LockedStat--value').text + ' sqft'
        
        address = house.find('div', class_='bp-Homecard__Address flex align-center color-text-primary font-body-xsmall-compact').text
        
        contact_number = house.find('button', class_='bp-Button RentalCTAContact__button RentalCTAContact__button--phone bp-Button__type--ghost bp-Button__size--compact').text
        
        link = 'https://www.redfin.com' + house.find('a', class_='link-and-anchor visuallyHidden').get('href')
        
        data = [count, price, number_of_rooms, number_of_baths, size, address, contact_number, link]
        
        houses_list.append(data)
        
        count += 1

print(len(houses_list))

#convert the variable houses_list to a dataframe and save to a CSV file
df = pd.DataFrame(houses_list)

df.to_csv('house_basic_info.csv', index=False)

links = []

for house in houses_list:
    links.append(house[7])
    
house_htmls = asyncio.run(fetch_all(links, headers))

# Check if links_list contains proper content
for i, content in enumerate(house_htmls):
    if content:
        print(f"Link {i}: Content length = {len(content)}")  # Should be non-zero
    else:
        print(f"Link {i}: No content fetched")

#convert the variable links_list to a dataframe and save to a CSV file
htmls = pd.DataFrame(house_htmls)

htmls.to_csv('house_htmls.csv', index=False)