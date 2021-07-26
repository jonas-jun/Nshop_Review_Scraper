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
