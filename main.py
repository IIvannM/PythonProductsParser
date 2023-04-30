import random
from time import sleep
import requests
from bs4 import BeautifulSoup
import json
import csv

URL = 'https://health-diet.ru/table_calorie/?utm_source=leftMenu&utm_medium=table_calorie'

headers = {
    'accept': '*/*',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 OPR/97.0.0.0 (Edition Yx GX)'
}


        
def main():
    with open('all_categories_dict.json', encoding='utf=8') as file:
        all_categories = json.load(file)
    
    iteration_count = int(len(all_categories)) - 1
    count = 0
    print(f'Всего итераций: {iteration_count}')
    
    for category_name, category_href in all_categories.items():
        
        for_replace = [',', ' ', '-',"'",'__']
        for item in for_replace:
            category_name = category_name.replace(item, '_')
        
        req = requests.get(url = category_href, headers= headers)
        src = req.text
        
        with open(f'data/{count}_{category_name}.html', 'w', encoding='utf=8') as file:
            file.write(src)
        with open(f'data/{count}_{category_name}.html', encoding='utf=8') as file:
            src = file.read()
        
        soup = BeautifulSoup(src, 'lxml')
        
        #checking for the presence of a page
        alert_block = soup.find(class_='uk-alert-danger')
        if alert_block is not None:
            continue
        
        #collecting headlines   
        table_headers = soup.find(class_='mzr-tc-group-table').find('tr').find_all('th')
        product = table_headers[0].text
        calories = table_headers[1].text
        proteins = table_headers[2].text
        fats = table_headers[3].text
        carbohydrates = table_headers[4].text
        
        with open(f'data/{count}_{category_name}.csv', 'w', encoding='utf-8-sig', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(
                (
                    product,
                    calories,
                    proteins,
                    fats,
                    carbohydrates
                )
            )
        #collecting data
        product_data = soup.find(class_='mzr-tc-group-table').find('tbody').find_all('tr')
        product_info = []
        
        for item in product_data:
            product_tds = item.find_all('td')
            title = product_tds[0].find('a').text
            calories = product_tds[1].text
            proteins = product_tds[2].text
            fats = product_tds[3].text
            carbohydrates = product_tds[4].text
            
            product_info.append(
                {
                    'Title': title,
                    'Calories': calories,
                    'Proteins': proteins,
                    'Fats': fats,
                    'Carbohydrates': carbohydrates
                }
            )
            
            with open(f'data/{count}_{category_name}.csv', 'a', encoding='utf-8-sig', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(
                    (
                        title,
                        calories,
                        proteins,
                        fats,
                        carbohydrates
                    )
                )
        
        with open(f'data/{count}_{category_name}.json', 'a', encoding='utf-8', newline='') as file:
            json.dump(product_info, file, indent=4, ensure_ascii=False)
            
        count +=1
        print(f'# Итерация №{count}. {category_name} записан...')
        iteration_count = iteration_count - 1
        
        if iteration_count == 0:
            print('Работа закончена')
            break
        
        print(f'Осталось итераций: {iteration_count}')
        sleep(random.randrange(2,4)) #the delay is made for the safety of the process, so that the site does not overturn us
                                     #if desired, delete it

if __name__ == '__main__':
    main()
    
'''functions that need to be executed only once or more in the code are not needed.'''

'''getHtml is launched once in main to get html markup to your computer and work with it already, 
    so as not to disturb the site with constant requests'''
def getHtml(URL, headers):
    req = requests.get(URL,headers=headers)
    src = req.text

    with open('index.html', 'w', encoding='utf=8') as file:
        file.write(src)
'''createJson is launched once. Creates a dictionary "Category - link to it" for the program to work'''       
def createJson():
    with open('index.html', encoding='utf=8') as file:
        src = file.read()
    soup = BeautifulSoup(src, 'lxml')
    
    all_products_href = soup.find_all(class_ = 'mzr-tc-group-item-href')
    all_categories_dict = {}
    
    for item in all_products_href:
        item_text = item.text
        item_href = 'https://health-diet.ru' + item.get('href')
        all_categories_dict[item_text] = item_href
    with open('all_categories_dict.json', 'w', encoding='utf=8') as file:
        json.dump(all_categories_dict, file, indent=4, ensure_ascii=False)