from flask import Flask, jsonify,request
import unicodedata
import requests
import os
from dotenv import load_dotenv, dotenv_values 
load_dotenv() 
from bs4 import BeautifulSoup
from flask_cors import CORS 
from flask_cors import cross_origin
app = Flask(__name__)
CORS(app)
session = requests.Session()

def log_in_sol(user: str, password: str) -> bool:
    url: str = 'https://aplikace.skolaonline.cz/SOL/Prihlaseni.aspx'
    data = {
        "__EVENTTARGET": "dnn$ctr994$SOLLogin$btnODeslat",
        "__EVENTARGUMENT": "",
        "__VIEWSTATE": "",
        "__VIEWSTATEGENERATOR": "",
        "__VIEWSTATEENCRYPTED": "",
        "__PREVIOUSPAGE": "",
        "__EVENTVALIDATION": "",
        "dnn$dnnSearch$txtSearch": "",
        "JmenoUzivatele": user,
        "HesloUzivatele": password,
        "ScrollTop": "",
        "__dnnVariable": "",
        "__RequestVerificationToken": ""
    }
    postLogin = session.post(url, data=data)
    return postLogin.status_code == 200

def scrape_data():
    username = str(os.getenv("USERBRRR")) #insert ur username here
    password = str(os.getenv("PASSWORD")) #insert ur password here
    print(username)
    print(password)
    if log_in_sol(username, password):
        base_url = "https://aplikace.skolaonline.cz"
        response = session.get(base_url + "/SOL/App/Hodnoceni/KZH001_HodnVypisStud.aspx#")
        
        if response.status_code == 200:
            html_content = response.text
            soup = BeautifulSoup(html_content, 'lxml')
            allsubject = soup.find_all('tr', {'class': 'ig_Alt igtbl_Alt'})
            subjects = []
            for i in range(len(allsubject) - 1):
                arr = allsubject[i + 1].find_all('td')
                arr = arr[:len(arr) - 3]
                for x in range(len(arr)):
                    if arr[x].text == '\xa0':
                        arr[x] = []
                    elif arr[x].text == '<td> </td>':
                        arr[x] = []
                    else:
                        if x == 0:
                            arr[x] = arr[x].text
                        else:
                            grades = arr[x].text.split()
                            for y in range(len(grades)):
                                if grades[y] == '-':
                                    grades.remove(grades[y])
                                else:
                                    grades[y] = int(grades[y])
                            arr[x] = grades
                subjects.append(arr)

            for z in range(len(subjects)):
                subject_name = unicodedata.normalize('NFKD', subjects[z][0]).encode('ascii', 'ignore').decode('utf-8')
                weight_10 = subjects[z][1] or []
                weight_8 = subjects[z][2] or []
                weight_6 = subjects[z][3] or []
                weight_4 = subjects[z][4] or []
                weight_2 = subjects[z][5] or []

                weighted_average = 0
                to_divide = 0
                if weight_10:
                    total = sum(c * 10 for c in weight_10)
                    weighted_average += total
                    to_divide += 10 * len(weight_10)

                if weight_8:
                    total = sum(c * 8 for c in weight_8)
                    weighted_average += total
                    to_divide += 8 * len(weight_8)

                if weight_6:
                    total = sum(c * 6 for c in weight_6)
                    weighted_average += total
                    to_divide += 6 * len(weight_6)

                if weight_4:
                    total = sum(c * 4 for c in weight_4)
                    weighted_average += total
                    to_divide += 4 * len(weight_4)

                if weight_2:
                    total = sum(c * 2 for c in weight_2)
                    weighted_average += total
                    to_divide += 2 * len(weight_2)

                if weighted_average == 0:
                    weighted_average = "No grades"
                else:
                    weighted_average = weighted_average / to_divide

                subjects[z].append(weighted_average)
            
            return subjects

    return []


@app.route('/api/grades', methods=['GET'])
@cross_origin()
def get_grades():
    data = scrape_data()
    return jsonify(data)
loggedIn = False
@app.route('/login', methods=['POST','GET'])
@cross_origin()
def login():
    username = request.form['username']
    password = request.form['password']
    global loggedIn
    if username == "admin" and password == "admin":
        loggedIn = True
        return jsonify({'success': True})
    else:
        loggedIn = False
        return jsonify({'success': False})
@app.route('/logout', methods = ['POST', 'GET'])
@cross_origin()
def logout():
    global loggedIn
    loggedIn = False
    return jsonify({'success': True})

@app.route('/get_login', methods = ['POST','GET'])
@cross_origin()
def get_login():
    global loggedIn
    return jsonify({'loggedIn': loggedIn})

if __name__ == '__main__':
    app.run(debug=True)