# festival_search_with_telegram
텔레그램봇 페스티벌 검색 봇

### 1. 텔레그램 botFather 에서 토큰 얻기 

### 2. ngrok.exe 실행후
<code>ngrok http 5000 --region ap</code> 
실행 후 https주소 복사

### 3. 텔레그램 봇파더에서 얻은 토큰과, ngrok에서 받은 서버주소로 웹훅연결 
<code>bot_set_webhook_call()</code>
### 4. alone_festival.py 실행
