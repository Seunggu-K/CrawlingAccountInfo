import requests
import json
import pandas as pd

def crawlingworklist():
    try:
        # response = requests.get("https://finance.naver.com/sise/sise_market_sum.naver?sosok=0")
        # html = response.text
        # soup = BeautifulSoup(html, 'html.parser')
        # titlelist = soup.select('a.tltle')

        # response2 = requests.get("https://finance.naver.com/sise/sise_market_sum.naver?sosok=1")
        # html2 = response2.text
        # soup2 = BeautifulSoup(html2, 'html.parser')
        # titlelist2 = soup2.select('a.tltle')

        # result = list(set([title.text for title in titlelist] + [title.text for title in titlelist2]))

        response = requests.get("https://comp.fnguide.com/SVO2/common/sp_read_json.asp?cmdText=menu_6_1&IN_U_CD=&IN_MARKET_GB=&IN_REPORT_GB=A&IN_SORT=7&_=1714804027264")

        # print(response.text[0:10])

        data = json.loads(response.text)

        arrtemp = [{'기업명': i['기업명'], 'GICODE': i['GICODE']} for i in data]

        result = pd.DataFrame(arrtemp)

        return result
    except Exception as e:
        return e