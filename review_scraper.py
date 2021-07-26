'''
2021-07-26
by Jonas-Jun
'''

import argparse
import time
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def scraping_product(stop, sleep, driver):
    count = 0
    next_btn = ['a:nth-child(2)', 'a:nth-child(3)', 'a:nth-child(4)', 'a:nth-child(5)', 'a:nth-child(6)', 'a:nth-child(7)', 'a:nth-child(8)', 'a:nth-child(9)',
    'a:nth-child(10)', 'a:nth-child(11)', 'a.fAUKm1ewwo._2Ar8-aEUTq']
    review_list = list()
    star_ratings = list()

    while count < stop:
        for pagenum in next_btn:
            driver.find_element_by_css_selector('#REVIEW > div > div._2y6yIawL6t > div > div.cv6id6JEkg > div > div > ' + str(pagenum) + '').send_keys(keys.ENTER)
            time.sleep(sleep)
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            page_review = soup.find_all('div', class_ = 'YEtwtZFLDz')
            page_rating_source = soup.find('div', class_ = 'cv6id6JEkg')
            page_rating = page_rating_source.find_all('em', class_ = '_15NU42F3kT')
        
            for i in range(len(page_review)):
                
                review = page_review[i].text
                rate = page_rating[i].text
                review = re.sub('\n|\t', ' ', review)
                review = re.sub(' +', ' ', review)
                review_list.append(review)
                star_ratings.append(rate)
        count += 1
    return review_list, star_ratings

def scraping_catalog(stop, sleep, driver):
    count = 0
    next_btn = ['a:nth-child(1)', 'a:nth-child(2)', 'a:nth-child(3)', 'a:nth-child(4)', 'a:nth-child(5)', 'a:nth-child(6)', 'a:nth-child(7)', 'a:nth-child(8)', 'a:nth-child(9)',
    'a:nth-child(10)', 'a.pagination_next__3ycRH']
    review_list = list()
    star_ratings = list()

    while count < stop:
        if count == 0:
            for pagenum in next_btn:
                #print(pagenum)
                driver.find_element_by_css_selector('#section_review > div.pagination_pagination__2M9a4 >' + str(pagenum) + '').send_keys(keys.ENTER)
                time.sleep(sleep)
                html = driver.page_source
                soup = BeautifulSoup(html, 'html.parser')
                page_source = soup.find('ul', class_ = 'reviewItems_list_review__1sgcJ')
                page_review = page_source.find_all('p', class_ = 'reviewItems_text__XIsTc')
                page_rating = page_source.find_all('span', class_ = 'reviewItems_average__16Ya-')

                for i in range(len(page_review)):
                    
                    review = page_review[i].text
                    rate = page_rating[i].text[-1]
                    review = re.sub('\n|\t', ' ', review)
                    review = re.sub(' +', ' ', review)
                    review_list.append(review)
                    star_ratings.append(rate)
            count += 1
        else:
            for pagenum in next_btn:
                driver.find_element_by_css_selector('#section_review > div.pagination_pagination__2M9a4 >' + str(pagenum) + '').send_keys(keys.ENTER)
                time.sleep(sleep)
                html = driver.page_source
                soup = BeautifulSoup(html, 'html.parser')
                page_source = soup.find('ul', class_ = 'reviewItems_list_review__1sgcJ')
                page_review = page_source.find_all('p', class_ = 'reviewItems_text__XIsTc')
                page_rating = page_source.find_all('span', class_ = 'reviewItems_average__16Ya-')

                for i in range(len(page_review)):
                    
                    review = page_review[i].text
                    rate = page_rating[i].text[-1]
                    review = re.sub('\n|\t', ' ', review)
                    review = re.sub(' +', ' ', review)
                    review_list.append(review)
                    star_ratings.append(rate)
            count += 1
    return review_list, star_ratings

def export(reviews, ratings, product):
    cnt = len(reviews)
    with open('NshopReview_{}_{}.txt'.format(product, cnt), 'w') as f:
        for review, rate in zip(reviews, ratings):
            f.write(review + '\t')
            f.write(rate + '\n')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', type=str)
    parser.add_argument('--max_count', type=int, default=5) # 20 + 200*k reviews
    parser.add_argument('--tsleep', type=int, default=2)
    parser.add_argument('--path_chrome', type=str, default='/Users/jonas/github/N_shop_scraper/chromedriver')
    parser.add_argument('--product', type=str, default='noname')
    parser.add_argument('--style', type=str) # 'product', 'catalog'
    args = parser.parse_args()
    
    keys = Keys()
    driver = webdriver.Chrome(args.path_chrome)
    driver.get(args.url)
    time.sleep(2)
    if args.style == 'product' or args.style == 'p':
        reviews, ratings = scraping_product(args.max_count, args.tsleep, driver)
    else:
        reviews, ratings = scraping_catalog(args.max_count, args.tsleep, driver)
    print('scraping finished, # of reviews: {:,}'.format(len(reviews)))    
    export(reviews, ratings, args.product)

# for insert mode

'''
python review_scraper.py --style c --product 갤워치액티브2_알루미늄_44mm --max_count 13 --url https://search.shopping.naver.com/catalog/20551835244

'''