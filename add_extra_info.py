#open the csv file 
import pandas as pd
from bs4 import BeautifulSoup

house_basic_info = pd.read_csv('house_htmls.csv')

#extract the content from the column
house_htmls = house_basic_info['0'].tolist()

count = 1

house_basic_info = pd.read_csv('house_basic_info.csv')

walk_score_list = []

transit_score_list = []

bike_score_list = []

house_school = []

for i in house_htmls:
    
    soup = BeautifulSoup(i, 'html.parser')
    
    schools = soup.find('div',class_ ="schools-content").find_all('div',class_="ListItem")
    
    school_info_list = []
    
    try:
        transit_info = soup.find('section', class_='bp-Section bp-AroundThisHomeSection font-body-base useContainer has-top-rule')
        
        walk_score = int(transit_info.find('div', class_='transport-icon-and-percentage walkscore').text.split('/')[0].strip())
        
        transit_score = int(transit_info.find('div', class_='transport-icon-and-percentage transitscore').text.split('/')[0].strip())
        
        bike_score = int(transit_info.find('div', class_='transport-icon-and-percentage bikescore').text.split('/')[0].strip())
        
        walk_score_list.append(walk_score)
        
        transit_score_list.append(transit_score)
        
        bike_score_list.append(bike_score)
                
    except AttributeError:
        
        walk_score_list.append("N/A")
        
        transit_score_list.append("N/A")
        
        bike_score_list.append("N/A")
    
    schools = soup.find('div',class_ ="schools-content").find_all('div',class_="ListItem")
    
    for school in schools:
        
        school_name = school.find('div',class_='ListItem__content flex flex-column').find('div',class_='ListItem__heading font-body-base-bold color-text-primary').text
        
        school_info = school.find('div',class_='ListItem__content flex flex-column').find('p',class_='ListItem__description font-body-small-compact color-text-secondary').text
        
        score = school.find('span',class_='rating-num').text

        temp = [school_name, school_info, score]
        
        if 'PreK' not in school_info:
            school_info_list.append(temp)
                
    house_school.append(school_info_list)
        
#add the new columns to the dataframe
house_basic_info['walk_score'] = walk_score_list

house_basic_info['transit_score'] = transit_score_list

house_basic_info['bike_score'] = bike_score_list

school1_names = []

school1_info = []

school1_score = []

school2_names = []

school2_info = []

school2_score = []

school3_names = []

school3_info = []

school3_score = []

for i in house_school:
    school1_names.append(i[0][0])
    school1_info.append(i[0][1])
    school1_score.append(i[0][2])
    try:
        school2_names.append(i[1][0])
        school2_info.append(i[1][1])
        school2_score.append(i[1][2])
    except:
        school2_names.append('N/A')
        school2_info.append('N/A')
        school2_score.append('N/A')
    try:
        school3_names.append(i[2][0])
        school3_info.append(i[2][1])
        school3_score.append(i[2][2])
    except:
        school3_names.append('N/A')
        school3_info.append('N/A')
        school3_score.append('N/A')

house_basic_info['school1_names'] = school1_names

house_basic_info['school1_info'] = school1_info

house_basic_info['school1_score'] = school1_score

house_basic_info['school2_names'] = school2_names

house_basic_info['school2_info'] = school2_info

house_basic_info['school2_score'] = school2_score

house_basic_info['school3_names'] = school3_names

house_basic_info['school3_info'] = school3_info

house_basic_info['school3_score'] = school3_score

house_basic_info.rename(columns = {'0':'order'}, inplace = True)
house_basic_info.rename(columns = {'1':'rent'}, inplace = True)
house_basic_info.rename(columns = {'2':'number of beds'}, inplace = True)
house_basic_info.rename(columns = {'3':'number of baths'}, inplace = True)
house_basic_info.rename(columns = {'4':'size'}, inplace = True)
house_basic_info.rename(columns = {'5':'address'}, inplace = True)
house_basic_info.rename(columns = {'6':'contact'}, inplace = True)
house_basic_info.rename(columns = {'7':'link'}, inplace = True)

#update the csv file 
house_basic_info.to_csv('house_full_info.csv', index=False)