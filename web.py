import streamlit as st
import requests
import xmltodict
import pandas as pd
import streamlit.components.v1 as components

st.set_page_config(
    page_title='구암고 점심식단',
    page_icon='',
    layout = 'wide'

)
menu = st.sidebar.selectbox('MENU',['일일식단','월별식단'])


if(menu=='일일식단'):

    신청주소 = 'https://open.neis.go.kr/hub/mealServiceDietInfo?'
    인증키 = 'KEY=e8558fb123fa49629fb523a81b325bfe&'
    문서타입 = 'Type=xml&'
    페이지수 ='pIndex1&'
    페이지당신청수 ='pSize=100&'
    시도교육청코드 ='ATPT_OFCDC_SC_CODE=D10&'
    표준학교코드 ='SD_SCHUL_CODE=7240056&'
    급식시작일자 ='MLSV_FROM_YMD=20230101&'
    급식종료일자 ='MLSV_TO_YMD=20230801'


    날짜선택 = st.date_input('날짜선택').strftime("%Y%m%d")

    url = 신청주소+인증키+문서타입+페이지수+페이지당신청수+시도교육청코드+표준학교코드+급식시작일자+급식종료일자

    response = requests.get(url)
    response = response.content

    xmlObject = xmltodict.parse(response)
    dict_data = xmlObject['mealServiceDietInfo']['row']
    df = pd.DataFrame(dict_data)
    df = df[['DDISH_NM','MLSV_YMD']]
    df = df[df['MLSV_YMD']==날짜선택]

    data = df.iloc[0]['DDISH_NM']
    list = data.split('<br/>')
    day = df.iloc[0]['MLSV_YMD']
    mon = day[4:6]+'월'
    day = day[6:8]+'일'

    st.header('구암고등학교 점식식단')
    st.subheader(mon+day)
    식단 = ''
    for value in list:
        식단 +='<li class="list-group-item">'+value+'</li>'

    components.html('''
    
    
    
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Bootstrap demo</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-KK94CHFLLe+nY2dmCWGMq91rCGa5gtU4mk92HdvYe+M/SXH301p5ILy+dN9+nJOZ" crossorigin="anonymous">
      <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/js/bootstrap.bundle.min.js" integrity="sha384-ENjdO4Dr2bkBIFxQpeoTz1HIcje39Wm4jDKdf19U8gI4ddQ3GYNS7NTKfAdVQSZe" crossorigin="anonymous"></script>
     
      </head>
      <body>
        <div class="card" style="width: 18rem;">
      <div class="card-header">
        '''+mon+day+'''
      </div>
      <ul class="list-group list-group-flush">
      '''+
      식단
                    +
    '''
      </ul>
    </div>
        </body>
    </html>
    
    
    
    
    
    ''',height=1200)
elif(menu=='월별식단'):
    신청주소 = 'https://open.neis.go.kr/hub/mealServiceDietInfo?'
    인증키 = 'KEY=e8558fb123fa49629fb523a81b325bfe&'
    문서타입 = 'Type=xml&'
    페이지수 = 'pIndex1&'
    페이지당신청수 = 'pSize=100&'
    시도교육청코드 = 'ATPT_OFCDC_SC_CODE=D10&'
    표준학교코드 = 'SD_SCHUL_CODE=7240056&'
    급식시작일자 = 'MLSV_FROM_YMD=20230501&'
    급식종료일자 = 'MLSV_TO_YMD=20230531'

    날짜선택 = st.date_input('날짜선택').strftime("%Y%m%d")

    url = 신청주소 + 인증키 + 문서타입 + 페이지수 + 페이지당신청수 + 시도교육청코드 + 표준학교코드 + 급식시작일자 + 급식종료일자

    response = requests.get(url)
    response = response.content

    xmlObject = xmltodict.parse(response)
    dict_data = xmlObject['mealServiceDietInfo']['row']
    df = pd.DataFrame(dict_data)


    df = df[['DDISH_NM', 'MLSV_YMD','CAL_INFO']]
    df = df[df['MLSV_YMD']>='20230508']
    df = df[df['MLSV_YMD'] <= '20230512']
    list = []
    식단 = ""
    for value in df['DDISH_NM']:

       value=value.split('<br/>')
       식단 = 식단 + f"<td>{str(value)}</td>"

  
  #  df = df[df['MLSV_YMD'] == '']
    components.html('''
    
    <!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Bootstrap demo</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-rbsA2VBKQhggwzxH7pPCaAqO46MgnOM80zW1RWuH61DGLwZJEdK2Kadq2F9CUG65" crossorigin="anonymous">
  </head>
  <body>
   
   
   

   <table class="table">
  <thead>
    <tr>
      <th scope="col">월요일</th>
      <th scope="col">화요일</th>
      <th scope="col">수요일</th>
      <th scope="col">목요일</th>
      <th scope="col">금요일</th>
    </tr>
  </thead>
  <tbody>
    <tr>
     
    </tr>
    <tr>
     
    </tr>
    <tr>
      '''
                    +식단+
                    '''
    </tr>
  </tbody>
</table>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-kenU1KFdBIe4zVF0s0G1M5b4hcpxyD9F7jL+jjXkk+Q2h455rYXK/7HAuoJl+0I4" crossorigin="anonymous"></script>
  </body>
</html>
    
    
    
    
    ''',height=1200)
