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

***
**update**  
- 210729 max_count가 일관적이지 않아 수정했습니다. 20(1페이지) + 200*max_count 만큼 스크래핑 됩니다. ex. max_count=3이라면 620개 (1~31페이지)  
- 210730 review를 스크래핑할 때 \n, \t가 여러 개 붙어있는 경우에도 잘 제거할 수 있도록 re.sub를 수정했습니다. 이후 txt 파일에 write할 때 문제가 발생할 수 있기 때문.  
