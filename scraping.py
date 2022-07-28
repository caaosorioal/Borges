# This script scrapes the page "https://ciudadseva.com/autor/jorge-luis-borges/cuentos/", extract the story and save it in a dataframe
from email.mime import base
import pandas as pd
import requests
from bs4 import BeautifulSoup
from os.path import join

# Get the request of the page
original_page = 'https://ciudadseva.com/autor/jorge-luis-borges/'

borges_categories = [
    'cuentos',
    'opiniones',
    'poemas'
]

# Create the empty lists for the title and the content for every story
categories = []
titles = []
stories_text = []

for category in borges_categories:
    base_page = original_page + category + '/'
    response_text = requests.get(base_page).text
    soup = BeautifulSoup(response_text, 'html.parser')
    titles_stories = soup.find_all('li', class_='text-center')

    # Loop every title story, select the content and save it in the list
    for title_story in titles_stories:
        title = title_story.text
        url_story = title_story.find('a').get('href')
        response_text_story = requests.get(url_story).text
        soup_story = BeautifulSoup(response_text_story, 'html.parser')
        paragraphs_story = soup_story.find_all('div', class_ = 'text-justify')

        if len(paragraphs_story) == 0:
            table_story = soup_story.find_all('table', class_ = 'table-center')
            text_story = table_story[0].find_all('p')[0].text
        else:
            text_story = ''
            for paragraph_story in paragraphs_story:
                text_story += paragraph_story.text
        
        categories.append(category)
        titles.append(title.strip())
        stories_text.append(text_story.strip().replace('\n', ''))

# Create the dataframe withe the titles and the stories
df = pd.DataFrame(
    data = {
        'title' : titles,
        'category' : categories,
        'story' : stories_text
    }
)
path = r'C:\Users\Carlososa\OneDrive - Caja de Compensacion Familiar de Antioquia COMFAMA\Archivos\Proyectos personales\NLP - t-SNE'
df.to_excel(join(path, 'stories.xlsx'), index = False)
print('Extraction completed successfully')