# -*- coding: utf-8 -*-
"""
Created on Sat Sep 21 19:02:42 2019

@author: EJ
"""

# -*- coding: utf-8 -*-

import requests
from flask import Flask, request, Response
from festival import festival_list_date
from openpyxl import load_workbook

EXCEL_FILE_NAME = 'Database.xlsx'
db = load_workbook(filename=EXCEL_FILE_NAME)
tuto_db = db['fv']

API_KEY = '975231772:AAEFSZRTH1hrpYV4c-9esIR4i5I1JIId874'

app = Flask(__name__)


def write_with_index(fv_user_pick_list):

    tuto_db['A1'].value = fv_user_pick_list
    db.save(EXCEL_FILE_NAME)
    print('엑셀파일에 저장되었따 리스트가')
 
def write_user_choice_num(user_choice_num):

    tuto_db['A5'].value = user_choice_num
    db.save(EXCEL_FILE_NAME)
    print('엑셀파일에 저장되었따 유저가 선택한 번호가 ')
    
def write_with_index_all(user_festival_list):

    tuto_db['A3'].value = user_festival_list
    db.save(EXCEL_FILE_NAME)
    print('엑셀파일에 저장되었따 원데이타가!')
    
    
def read_with_index(loc):
    read_result = tuto_db[loc].value
    return read_result
    
def parse_message(data):
    chat_id = data['message']['chat']['id']
    msg = data['message']['text']
    
    return chat_id, msg

def pick_list_back(pick_list):
    return pick_list

def send_message(chat_id, text='bla-bla-bla'):
    """
    Chat-id 와 text를 변수로 받아 메세지를 보내주는데
    params 안에 키보드를 설정해서 같이 보내주는 방법
    
    https://core.telegram.org/bots/api#keyboardbutton
    """
    url = 'https://api.telegram.org/bot{token}/sendMessage'.format(token=API_KEY)   #sendMessage
    keyboard = {                                        # Keyboard 형식
            'keyboard':[[{
                    'text': '기간'
                        },
                    {'text': '종류'
                        }]
                    ],
            'one_time_keyboard' : True
            }
    
    
    if text[5:].isdigit():
        print('###@@@###사용자가날짜를입력했다.###### #####')
        params = {'chat_id':chat_id, 'text': text}
        requests.post(url, json=params)
    elif (text=='기간') & (len(text)==2):                           
        print('#######기간버튼누름###########')
        params = {'chat_id':chat_id, 'text': '입력방식=[기간검색!+원하는 기간]을 입력 예)기간검색!2019080120191230  오타 조심..' }
        requests.post(url, json=params)
    elif (text=='종류') & (len(text)==2):
        undercon='누가 종류를 눌렀는가..누르지 말라고 했거늘..종류는 아직 준비중일세;'
        keyboard = {
            'keyboard':[[{'text': '여기를 클릭하시오 ....;;'}]],
            'one_time_keyboard' : True
            }    
        text=text+undercon
        params = {'chat_id':chat_id, 'text': text, 'reply_markup' : keyboard}
        requests.post(url, json=params)
        return 0 
    elif len(text)>100: #기간입력하면 여기서 리스트 뿌려줌.
        #엑셀에 쓴다. 
        write_with_index(text)      
        print('100개이상이니까 출력해줌')
        text=' 번호 하나 선택 바람, 입력방식=[원하는번호+번] 예)2번 '+'\n'+text
        params = {'chat_id':chat_id, 'text': text}
        requests.post(url, json=params)
    elif len(text)==2 : # 리스트중 한개선택했다면
        print('리스트중 번호하나 선택했으면')
        write_user_choice_num(text) #선택한 번호 엑셀에 저장하였다.         
        read_result=read_with_index('A1') #엑셀에서 읽어 들어온다    
        print('엑셀서읽어들어왔따.')      
        show_list=read_result.split('\n') # 줄바꿈으로 구분자해서 리스트로 바꿔준다. 
        for item in show_list:
            if text in item:
                final_decision_title=item
                print(final_decision_title)               
        keyboard = {
            'keyboard':[[{'text': '네'},
                         {'text': '아니요'}]],
            'one_time_keyboard' : True
            }    
        #params = {'chat_id':chat_id, 'text': '"'+final_decision_title+'"'+'이라.. 탁월한 선택이군..상세정보도 원하는가?  네 라고 답해야만 한다네..흠', 'reply_markup' : keyboard}
        params = {'chat_id':chat_id, 'text': '탁월한 선택이군..상세정보도 원하는가?  네 라고 답해야만 한다네..흠', 'reply_markup' : keyboard}
        requests.post(url, json=params)
    elif text=='네': #디테일정보 뿌려줌 이 축제가 맞다고 하면
        print('네 라고했다!!')
        read_result_all=read_with_index('A3') #엑셀에서 읽어 들어온다  
        print('엑셀서읽어들어왔따 모든데이타를!.')
        show_list_detail=read_result_all.split('\n') # 줄바꿈으로 구분자해서 리스트로 바꿔준다. 
        print('show_list_detail.',show_list_detail)
        read_user_num=read_with_index('A5')#엑셀에서 읽어 들어온다 사용자가 선택한 넘버를
        for item in show_list_detail:
            if read_user_num in item:
                final_decision_detail=item
               # print(final_decision_detail)
                final_decision_detail=final_decision_detail+'.....이게 내가 가진 모든 정보라네.. 더이상은 무리야..축제에서 즐거운 시간 보내길 바라.. 흠흠..그럼 난 이만 도봉산으로 퇴근 총총..날 다시 부르려면 [나와라]라고 입력해줘...'
        params = {'chat_id':chat_id, 'text': final_decision_detail}
        requests.post(url, json=params)
    elif text=='나와라':
        params = {'chat_id':chat_id, 'text': '누가 날 부르는가...축제를 가려나보구먼..여기서는 축제를 기간 또는 종류로 검색할 수 있다네. 아니다. 종류는 아직 준비중이다 기간 클릭하시게.. . ', 'reply_markup' : keyboard}
        requests.post(url, json=params)
    elif text=='아니요':
        params = {'chat_id':chat_id, 'text': '아니라니...대화가 종료되었다네... 날 다시 부르려면 [나와라]라고 입력하시오..'}
        requests.post(url, json=params)
    else:
        params = {'chat_id':chat_id, 'text': '누가 날 부르는가...축제를 가려나보구먼..여기서는 축제를 기간 또는 종류로 검색할 수 있다네. 아니다. 종류는 아직 준비중이다 기간 클릭하시게.. . ', 'reply_markup' : keyboard}
        requests.post(url, json=params)
    # 변수들을 딕셔너리 형식으로 묶음
    #params = {'chat_id':chat_id, 'text': '호잇', 'reply_markup' : keyboard}
    
    # Url 에 params 를 json 형식으로 변환하여 전송
    # 메세지를 전송하는 부분
    #response = requests.post(url, json=params)
    
    return 0
    
# 경로 설정, URL 설정
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        message = request.get_json()

                     
        chat_id, msg = parse_message(message)
        send_message(chat_id, msg)
        
        if msg[:5] == "기간검색!":  
            userDate = msg[5:] #userDate= 2019090920191010
            print(userDate,'=====userdate ,기간검색!으로 찾았으니까 함수불러')
            festivalListShow,user_festival_list =  festival_list_date(userDate)
            #원데이타를 엑셀에써준다.
            #원데이타가 리스트라 엑셀에 안써져서 str로 바꾼뒤 써줌 
            user_all_data=''
            i = 1
            for item in user_festival_list:
                user_all_data = user_all_data + f'{i}'+'번 '+ item['title'] +item['firstimage']+'  '+' 주 소 : '+item['addr1']+'  축제기간 : '+str(item['eventstartdate'])+'~'+str(item['eventenddate'])+'.'+ '\n'
                i += 1
               
            write_with_index_all(user_all_data)#엑셀에 작성하는 코드 
            
            send_message(chat_id, festivalListShow)
            
        return Response('ok', status=200)
    else:
        return 'Hello World!'


# Python 에서는 실행시킬때 __name__ 이라는 변수에
# __main__ 이라는 값이 할당
if __name__ == '__main__':
    app.run(port = 5000)
