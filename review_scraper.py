'''
2021-07-26
by Jonas-Jun

2021-07-28
fix max_count
20 + 200*max_count
example:
max_count==1: scrap 1 to 11 page (220)
max_count==3: scrap 1 to 31 page (620)
'''

import argparse
import time
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def scraping_product(stop, sleep, driver):
    count = 0
    next_btn_temp = ['a:nth-child(2)', 'a:nth-child(3)', 'a:nth-child(4)', 'a:nth-child(5)', 'a:nth-child(6)', 'a:nth-child(7)', 'a:nth-child(8)', 'a:nth-child(9)',
    'a:nth-child(10)', 'a:nth-child(11)', 'a.fAUKm1ewwo._2Ar8-aEUTq']
    review_list = list()
    star_ratings = list()

    while count < stop:
        next_btn = next_btn_temp if count == 0 else next_btn_temp[1:]
        for pagenum in next_btn:
            try:
                driver.find_element_by_css_selector('#REVIEW > div > div._2y6yIawL6t > div > div.cv6id6JEkg > div > div > ' + str(pagenum) + '').send_keys(keys.ENTER)
            except: break
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
                if not re.search('[가-힣]', review): continue # 한글이 하나도 없을 경우 추가하지 않음
                if len(review.split())==1: continue # 띄어쓰기가 하나도 안 되어 있을 경우 추가하지 않음
                review_list.append(review)
                star_ratings.append(rate)
        count += 1
    return review_list, star_ratings

def scraping_catalog(stop, sleep, driver):
    count = 0
    next_btn_1 = ['a.pagination_now__gZWGP', 'a:nth-child(2)', 'a:nth-child(3)', 'a:nth-child(4)', 'a:nth-child(5)', 'a:nth-child(6)', 'a:nth-child(7)',
    'a:nth-child(8)', 'a:nth-child(9)', 'a:nth-child(10)', 'a.pagination_next__3ycRH']
    next_btn_2 = ['a:nth-child(3)', 'a:nth-child(4)', 'a:nth-child(5)', 'a:nth-child(6)', 'a:nth-child(7)', 'a:nth-child(8)',
    'a:nth-child(9)', 'a:nth-child(10)', 'a:nth-child(11)', 'a.pagination_next__3ycRH']
    review_list = list()
    star_ratings = list()

    while count < stop:
        next_btn = next_btn_1 if count == 0 else next_btn_2
        for pagenum in next_btn:
            try:
                driver.find_element_by_css_selector('#section_review > div.pagination_pagination__2M9a4 >' + str(pagenum) + '').send_keys(keys.ENTER)
            except: break
            time.sleep(sleep)
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            page_source = soup.find('ul', class_ = 'reviewItems_list_review__1sgcJ')
            page_review = page_source.find_all('p', class_ = 'reviewItems_text__XIsTc')
            page_rating = page_source.find_all('span', class_ = 'reviewItems_average__16Ya-')

            for i in range(len(page_review)):
                
                review = page_review[i].text
                rate = page_rating[i].text[-1]
                review = re.sub('\n+|\t+', ' ', review)
                review = re.sub(' +', ' ', review)
                if not re.search('[가-힣]', review): continue # 한글이 하나도 없을 경우 추가하지 않음
                if len(review.split())==1: continue # 띄어쓰기가 하나도 안 되어 있을 경우 추가하지 않음
                review_list.append(review)
                star_ratings.append(rate)
        count += 1
    return review_list, star_ratings

def export(reviews, ratings, product):
    cnt = len(reviews)
    raw_name = '[Raw]NshopReview_{}_{}.txt'.format(product, cnt)
    with open(raw_name, 'w') as f:
        for review, rate in zip(reviews, ratings):
            f.write(review + '\t')
            f.write(rate + '\n')
    print('file created: ', raw_name)
    return raw_name
    
if __name__ == '__main__':
    welcome = '''
    ====================
    Nshop_Review_Scraper has been run
    code by Junmay
    https://github.com/jonas-jun/Nshop_Review_Scraper
    ====================
    '''
    print(welcome)
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', type=str)
    parser.add_argument('--max_count', type=int, default=5) # 20 + 200*k reviews
    parser.add_argument('--tsleep', type=int, default=1.5)
    parser.add_argument('--path_chrome', type=str, default='/Users/jonas/github/N_shop_scraper/chromedriver')
    parser.add_argument('--product', type=str, default='noname')
    parser.add_argument('--style', type=str) # 'product', 'catalog'
    parser.add_argument('--process', type=bool, default=True)
    args = parser.parse_args()
    
    if args.style == 'catalog' or args.style == 'c':
        assert args.max_count < 10, 'when catalog style, maximum 2,000 reviews can be showed'

    keys = Keys()
    driver = webdriver.Chrome(args.path_chrome)
    driver.get(args.url)
    time.sleep(2)
    if args.style == 'product' or args.style == 'p':
        reviews, ratings = scraping_product(args.max_count, args.tsleep, driver)
    else:
        reviews, ratings = scraping_catalog(args.max_count, args.tsleep, driver)
    print('scraping finished, # of reviews: {:,}'.format(len(reviews)))    
    raw_name = export(reviews, ratings, args.product)

    if args.process:
        from data_process import load_reviews, drop_duplicates
        reviews, ratings, re_buy, a_month = load_reviews(raw_name)
        reviews, ratings, re_buy, a_month = drop_duplicates(reviews, ratings, re_buy, a_month)
        process_name = '[Process]NshopReview_{}_{}.txt'.format(args.product, len(reviews))
        with open(process_name, 'w') as f:
            # write header
            f.write('review\trating\tre-perchase\tmonthly_use\n')
            for review, rating, rebuy, month in zip(reviews, ratings, re_buy, a_month):
                f.write(review + '\t' + str(rating) + '\t')
                f.write(str(rebuy) + '\t' + str(month) + '\n')
        print('Processed file created: ', process_name)

# for insert mode
'''
python review_scraper.py --product 부르조아_벨벳펜슬_3_beautyshop --style p --max_count 15 --url https://smartstore.naver.com/beautyshop/products/4713083841
python review_scraper.py --product 하만카돈_AuraStudio3_카탈로그 --style c --max_count 8 --url https://search.shopping.naver.com/catalog/24067251522
'''
