from selenium import webdriver
from bs4 import BeautifulSoup
#프로세스 정지시킬때 사용할 예정
import time
#정규표현식 regular expression, 주로 문자 찾을때 사용.
#매칭되는거 찾으면 반환, 매칭된 위치, 변환, 분할 등의 기능을 제공함
import re
#문자의 속성을 정의하는 유니코드 문자 데이터베이스에 대한 엑세스를 제공
import unicodedata

#####인스타그램 접속하기#####
#크롬드라이버 오픈
driver = webdriver.Chrome('./chromedriver')
#웹드라이버 사용. get()으로 url을 호출한다.
driver.get('https://www.instagram.com/')
#잠시 프로세스를 멈춘다고 생각하면됨. 그 이유는 웹드라이버가 켜지는 시간을 주기 위해서
time.sleep(2)

#####인스타그램 로그인#####
email = '94cogus@gmail.com'
#개발자도구 들어가서 찾는법 계속 공부/언급해야함
input_id = driver.find_elements_by_css_selector('input._2hvTZ.pexuQ.zyHYP')[0]
input_id.clear()
input_id.send_keys(email)

password = 'dlatl1'
input_pw = driver.find_elements_by_css_selector('input._2hvTZ.pexuQ.zyHYP')[1]
input_pw.clear()
input_pw.send_keys(password)
input_pw.submit()
time.sleep(3)

#####인스타그램 검색결과#####
def insta_searching(word):
    url = 'https://www.instagram.com/explore/tags/' + word
    return url

#####검색 결과 페이지 접속하기#####
word = '제주여행'
#인스타그램 검색결과 함수 호출
url = insta_searching(word)
#웹드라이버에 url 전달
driver.get(url)

def select_first(driver):
    first = driver.find_element_by_css_selector('div._9AhH0') 
    #find_element_by_css_selector 함수를 사용해 요소 찾기
    first.click()
    time.sleep(3) #로딩을 위해 3초 대기
    
select_first(driver)

#####게시글 정보 가져오기#####
def get_content(driver):
    # 1. 현재 페이지의 HTML 정보 가져오기
    # driver.page_source명령어로 현재 화면에 표시된 내용의 HTML 데이터를 가져올 수 있음
    html = driver.page_source
    # 파싱에 대한 개념언급
    # 파싱은 어떤 페이지에서 내가 원하는 데이터를 특정 패턴이나 순서로 추출해 가공하는 것을 의미
    # beautifulSoup 라이브러리 설명
    soup = BeautifulSoup(html, 'html.parser')
    
    #try except 문법언급 : 예외처리
    
    # 2. 본문내용 가져오기
    try:
        #게시물 본문 내용의 클래스가 C4VMK태그
        content = soup.select('div.C4VMK > span')[0].text
        #태그명이 div, class가 C4VMK태그 아래에 있는 span 태그를 모두 선택
        #[0] 첫번째 태그를 선택
        #.text 해당 태그의 텍스트
        content = unicodedata.normalize('NFC', content)
        #macOS에서 작성된 글의 경우 한글 자음/모음이 분리되는 현상 => unicodedata를 이용해 자음/모음을 합쳐서 한글을 처리하는 방식추가
    except:
        content = ' ' 
        
    # 3. 본문 내용에서 해시태그 가져오기(정규표현식 활용)
    tags = re.findall(r'#[^\s#,\\]+', content)
    # 해시태그를 별도로 표시하지 않고 본문 중에서 어느곳이나 # 기호를 붙여 해시태그 사용가능
    # 따라서 크롤링을 진행할 때 해시태그만 골라서 가져올 수가 없음.
    # 그래서 본문 내용을 먼저 수집한 뒤에, 해시태그만 선별하는 작업이 필요함
    # 정규표현식에 사용되는 re 라이브러리 사용
    # #으로 시작하고, # 뒤에 연속된 문자(공백이나 #, \ 기호가 아닌 경우를 모두 찾아서 리스트 형태로 tags 변수에 저장)
    
    # 4. 작성 일자 가져오기
    # 1일 전으로 보이더라도, HTML 내에서는 '년월일-시간'형태로 입력되어 있음
    # 1일 전과 같은 데이터를 들고올 수 있지만, 데이터분석에서 사용되기에는 적절하지 않은 데이터임
    try:
        date = soup.select('time._1o9PC.Nzb55')[0]['datetime'][:10]
        #앞에서부터 10자리 글자를 들고오면 년월일만 들고오게됨
    except:
        date = ''
        
    # 5. 좋아요 수 가져오기
    try:
        like = soup.select('div.Nm9Fw > a')[0].text[4:-1] 
        #좋아요라는 글자와 띄어쓰기 한칸까지 포함해서 숫자에 대한하는 부분은 인덱스값이 4부터이며, 마지막 개 글자를 제외하기 위해 -1로 슬라이싱값 설정
    except:
        like = 0
        #좋아요를 하나도 못받은 게시물이 있을 수 있기 때문에 예외처리
        
    # 6. 위치 정보 가져오기
    try:
        place = soup.select('div.M30cS')[0].text
        place = unicodedata.normalize('NFC', place)
    except:
        place = ''
        #위치 정보가 입력되지 않은 경우 에러가 발생하기 때문에 예외처리 해줘야함
        
    # 7. 수집한 정보 저장하기
    data = [content, date, like, place, tags]
    return data

get_content(driver)

def move_next(driver):
    right = driver.find_element_by_css_selector('div.l8mY4 > button')
    right.click()
    time.sleep(3)
    
move_next(driver)
results = []
target = 10

for i in range(target):
    try:
        data=get_content(driver)
        results.append(data)
        move_next(driver)
    except:
        time.sleep(2)
        move_next(driver)
        
print(results[:2])