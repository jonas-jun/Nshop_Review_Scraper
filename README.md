# Nshop_Review_Scraper
쇼핑 리뷰 크롤러

**N 쇼핑 상품 리뷰와 평점을 크롤링합니다**  
자세한 설명은 넣지 않겠습니다. 해당 회사의 소중한 데이터일 수 있으니  


@args
- --url: 크롤링할 페이지의 url입니다.  
- --max_count: 최대 몇 개의 리뷰를 크롤링할지? 숫자 1당 11페이지(=220개의 리뷰를 저장합니다)  
- --tsleep: 한페이지 체류 시간. 기본은 2초입니다.  
- --path_chrome: Chrome driver 파일의 abstract path. folderA에 들어있다면 folderA/chromedriver 까지 넣어줘야 합니다.  
- --product: txt파일로 뽑아낼 때 파일명에 사용됩니다.  
- --style: 두 가지 형태의 페이지가 있습니다.  product 페이지와 catalog 페이지. {p, c}  
- --process: 데이터 전처리 여부입니다. 아래 data_process.py 설명과 같은 처리가 이뤄집니다. {True, False}, default=True

**data_process.py**  
- '한달사용기', '재구매' 리뷰는 리뷰 본문에서 해당 텍스트를 제거하고 별도의 column으로 1 표기 하도록 했습니다.
- 연속된 리뷰들이 완전히 동일할 경우 (한번에 여러 상품을 구매 후 같은 리뷰를 동시에 업로드할 때 이런 케이스가 발생하는 것 같습니다) 하나만 남기도록 했습니다.  


***
**update**  
- 210729 max_count가 일관적이지 않아 수정했습니다. 20(1페이지) + 200*max_count 만큼 스크래핑 됩니다. ex. max_count=3이라면 620개 (1~31페이지)  
- 210730 review를 스크래핑할 때 \n, \t가 여러 개 붙어있는 경우에도 잘 제거할 수 있도록 re.sub를 수정했습니다. 이후 txt 파일에 write할 때 문제가 발생할 수 있기 때문.  
- 210730 data_process.py를 추가하고 review_scraper.py 에서 실행될 수 있도록 했습니다.
