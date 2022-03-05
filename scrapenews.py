from bs4 import BeautifulSoup
import random, requests 
import pandas as pd 

def findtitles():
    response = requests.get('https://www.foxnews.com/politics').text
    soup = BeautifulSoup(response, 'lxml')

    main = soup.find('main', {'class': 'main-content'})

    section = main.find_all('section')

    article = main.find_all('article')


    article_title = []
    titles = []
    links = []
    images = []
    times = []
    for i in range(len(article)):
        a = article[i].find('a')
        article_title.append(a)

    for i in range(len(article_title)):  # Finding the title, link, and image of the individual articles
        img = article_title[i].find('img')
        
        title = img.attrs['alt']
        titles.append(title)

        l = article_title[i].attrs['href']
        links.append(l)

        imgsrc = img.attrs['src']
        images.append(imgsrc)

        time = article[i].find('span', class_='time')
        times.append(time.text)

    for i in range(len(links)):  # Adding the beginning of the link to the alt attrs 
        if links[i].startswith('/politics/'):
            links[i] = 'https://foxnews.com' + links[i]
        elif links[i].startswith('/lifestyle'):
            links[i] = 'https://foxnews.com' + links[i]
        elif links[i].startswith('/opinion'):
            links[i] = 'https://foxnews.com' + links[i]
        elif links[i].startswith('/media'):
            links[i] = 'https://foxnews.com' + links[i]

    
    

    articledict = {  # Making a dataframe of the scrape so we can easily access them in the backend 
        'Title': titles,
        'Link' : links,
        'Images': images,
        'Time': times
    }



    
    foxnews = pd.DataFrame(articledict)

    return foxnews
    
        

