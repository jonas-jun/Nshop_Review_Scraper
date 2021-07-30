# 잘못 크롤링된 데이터는 빼고 load
def load_reviews(file):
    with open(file, 'r') as f:
        lines = f.readlines()
    reviews, ratings, re_buy, a_month = list(), list(), list(), list()
    for idx in range(len(lines)):
        line = lines[idx].split('\t')
        if len(line) !=2: continue
        review, rating = line[0], line[1]

        # 한달사용기
        if review.startswith('한달사용기'):
            review = review[5:]
            a_month.append(1)
        else:
            a_month.append(0)
        
        # 재구매
        if review.startswith('재구매'):
            review = review[3:]
            re_buy.append(1)
        else:
            re_buy.append(0)
        
        reviews.append(review)
        ratings.append(rating.strip())
    
    return reviews, ratings, re_buy, a_month

def drop_duplicates(reviews, ratings, re_buy, a_month):
    before = len(reviews)
    i = 0
    while i < len(reviews)-1:
        if reviews[i] == reviews[i+1]:
            reviews.pop(i)
            ratings.pop(i)
            re_buy.pop(i)
            a_month.pop(i)
            continue
        i += 1
    after = len(reviews)
    print(' >> {:,} reviews are removed (continuous duplicates)'.format(before-after))
    return reviews, ratings, re_buy, a_month

