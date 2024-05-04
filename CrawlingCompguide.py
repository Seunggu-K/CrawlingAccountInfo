import requests
from bs4 import BeautifulSoup
import re

def crawlingcompguide(gicode):
    try:
        # print(1)
        response = requests.get("https://comp.fnguide.com/SVO2/ASP/SVD_Main.asp?gicode="+gicode)
        # print(2)
        html = response.text
        # print(3)
        soup = BeautifulSoup(html, 'html.parser')
        # print(4)
        # capitalization = soup.select_one('#svdMainGrid1 > table > tbody > tr:nth-child(5) > td:nth-child(2)').text
        capitalization = re.sub('[^0-9]', '', soup.select_one('#svdMainGrid1 > table > tbody > tr:nth-child(5) > td:nth-child(2)').text)
        # print(5)
        response2 = requests.get("https://comp.fnguide.com/SVO2/ASP/SVD_Finance.asp?gicode="+gicode)
        # print(6)
        html2 = response2.text
        # print(7)
        soup2 = BeautifulSoup(html2, 'html.parser')
        # print(8)
        # current_assets = soup2.select_one('#p_grid2_2 > td.r.cle').text
        current_assets = re.sub('[^0-9]', '', soup2.select_one('#p_grid2_2 > td.r.cle').text)
        # print(9)
        # total_debt = soup2.select_one('#divDaechaY > table > tbody > tr:nth-child(29) > td.r.cle').text
        total_debt = re.sub('[^0-9]', '', soup2.select_one('#divDaechaY > table > tbody > tr:nth-child(29) > td.r.cle').text)
        # print(10)
        return int(capitalization), int(current_assets), int(total_debt)
    except Exception as e:
        # print(e)
        return 0