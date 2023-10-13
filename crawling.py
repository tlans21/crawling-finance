from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
import datetime
import time


def main():
    # 입력
    startPage = int(input("검색 시작 Page: "))
    endPage = int(input("검색 마지막 Page: "))

    # 서치 시작 함수
    getKospiSerachAndtoCsv(startPage, endPage+1)
    
    return   

def getKospiSerachAndtoCsv(start, end):
    baseURL = "https://finance.naver.com/sise/sise_market_sum.naver"
    
    result = []

    for i in range(start, end):
        parameters = "?page=%s" %(i)
        
        URL = baseURL + parameters
        
        print("%d번째 페이지" %(i))
        # 네이버 증권 서버에 요청
        
        getRequestUrl(URL, result)

    toCsv(result)
    return


def getRequestUrl(url, result):
    # 네이버 증권 서버에 요청
    req = urllib.request.Request(url)
    html = urllib.request.urlopen(req)
    soupCB = BeautifulSoup(html, 'html.parser', from_encoding='cp949')
    
    time.sleep(4)
    tag_div_box_type_l = soupCB.select("#newarea div.box_type_l")
    
    tag_table_list = tag_div_box_type_l[0].find_all('table', attrs={"summary":"코스피 시세정보를 선택한 항목에 따라 정보를 제공합니다."})
    # tag_table_list은 리스트로 반환되었기 때문에 리스트를 벗겨주고 사용해야한다.
    tag_table = tag_table_list[0]
    
    # find는 하나의 리스트를 대상으로 목표를 찾는다.
    target_tag_tbody= tag_table.find('tbody')
     
    target_tag_trs = target_tag_tbody.find_all('tr', attrs={"onmouseover":"mouseOver(this)"})
    # target_tag_trs는 tr속성을 갖고있는 리스트들로 반환되었습니다. 
    for tag_tr in target_tag_trs:
        tag_td = tag_tr.find_all('td')
        fi_number = tag_td[0].string
        fi_name = tag_td[1].string
        fi_currentPrice = tag_td[2].string
        fi_preDayExpenses = tag_td[3].find('span').string.strip()
        
        
        # 만약에 전일비가 0이면 상승, 하락도 없기 때문에 조건 처리
        if fi_preDayExpenses == '0': 
            UpAndDownOfpreDayExpenses = ""
        else:
            try:
                UpAndDownOfpreDayExpenses = tag_td[3].find("img")['alt']
            except Exception as e:
                UpAndDownOfpreDayExpenses = ""

        fi_preDayExpenses = fi_preDayExpenses+ " " + UpAndDownOfpreDayExpenses
        fi_fluctuationRate = tag_td[4].find('span').string.strip()
        fi_faceValue = tag_td[5].string
        fi_market_capitalization= tag_td[6].string
        fi_NumberOfShares= tag_td[7].string
        fi_Foreigner_Ratio= tag_td[8].string
        fi_TradingVolume= tag_td[9].string
        fi_PER = tag_td[10].string
        fi_ROE = tag_td[11].string

        
        print("번호: ", fi_number)
        print("종목명: ", fi_name)
        print("현재가: ", fi_currentPrice)
        print("전일비: ", fi_preDayExpenses)
        print("등락률: ", fi_fluctuationRate)
        print("액면가: ", fi_faceValue)
        print("시가총액: ", fi_market_capitalization)
        print("상장주식수: ", fi_NumberOfShares)
        print("외국인비율: ", fi_Foreigner_Ratio)
        print("거래량: ", fi_TradingVolume)
        print("PER: ", fi_PER)
        print("ROE: ", fi_ROE)
        print('============구분선===============')
        result.append([fi_number]+[fi_name]+[fi_currentPrice]+[fi_preDayExpenses]+[fi_fluctuationRate]+[fi_faceValue]+[fi_market_capitalization]+[fi_NumberOfShares]+[fi_Foreigner_Ratio]+[fi_TradingVolume]+[fi_PER]+[fi_ROE])
    
    return

def toCsv(result):
    finance = pd.DataFrame(result, columns=('번호','종목명','현재가','전일비','등락률','액면가','시가총액','상장주식수','외국인비율','거래량','PER','ROE'))
    finance.to_csv('./finance.csv', encoding='cp949', mode='w', index=True)
    del result[:]


if __name__ == '__main__':
    main()