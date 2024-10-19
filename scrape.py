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

def scrape_data(username, password): #insert ur password here
    print(username)
    print(password)
    if log_in_sol(username, password):
        base_url = "https://aplikace.skolaonline.cz"
        response = session.get(base_url + "/SOL/App/Hodnoceni/KZH001_HodnVypisStud.aspx#")
        
        if response.status_code == 200:
            html_content = response.text



            soup = BeautifulSoup(html_content, 'html.parser')

            # Selecting rows from the table body (adjust the selector according to your actual HTML structure)
            rows = soup.select("tr")

            grades_data = []

            for row in rows[2:]:  # Assuming the first two rows are headers, skip them
                columns = row.find_all("td")
                
                if len(columns) < 6:  # Skip rows that don't have the expected number of columns (subject + 5 weights)
                    continue
                
                subject_name = columns[0].get_text(strip=True)  # Get the subject name from the first column
                
                weights = []
                for i in range(1, 6):  # Process the next 5 columns (weights/grades)
                    grade_text = columns[i].get_text(strip=True)
                    if grade_text == "-" or not grade_text:
                        weights.append([])  # Empty array for missing grades
                    else:
                        try:
                            weights.append([int(grade_text)])  # Convert grade to an integer and wrap in a list
                        except ValueError:
                            weights.append([])  # Fallback in case of non-numeric values
                
                grades_data.append([subject_name] + weights)
            for i in range(4):
                grades_data.remove(grades_data[0])
            for i in range(2):
                grades_data.remove(grades_data[-1])
            # Display the structured grades data
            
            subjects=grades_data

            for z in range(len(subjects)):
                subject_name = unicodedata.normalize('NFKD', subjects[z][0]).encode('ascii', 'ignore').decode('utf-8')
                subjects[z][0] = subject_name
                
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
loggedIn = False
loggedInSOL = False
SOL_username = ""
SOL_password = ""
@app.route('/api/grades', methods=['GET'])
@cross_origin()
def get_grades():

    if loggedInSOL:
        data = scrape_data(SOLusername, SOLpassword)
        return jsonify(data)
    else:
        return jsonify({'success': False})
@app.route('/api/test_grades', methods=['GET'])
@cross_origin()
def test_get_grades():
    data = scrape_data(str(os.getenv("USERBRRR")),os.getenv("PASSWORD"))
    return jsonify(data)

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
    
@app.route('/login_sol', methods=['POST','GET'])
@cross_origin()
def login_SOL():
    global SOLusername
    global SOLpassword
    global loggedInSOL
    SOLusername = request.form['username']
    SOLpassword = request.form['password']
    if SOLusername != "" and SOLpassword != "":
        loggedInSOL = True
        return jsonify({'success': True})
    else:
        loggedInSOL = False
        return jsonify({'success': False})
    
@app.route('/logout', methods = ['POST', 'GET'])
@cross_origin()
def logout():
    global loggedInSOL
    global SOLusername
    global SOLpassword
    loggedInSOL = False
    SOLusername = ""
    SOLpassword = ""
    return jsonify({'success': True})

@app.route('/get_login', methods = ['POST','GET'])
@cross_origin()
def get_login():
    global loggedInSOL
    return jsonify({'loggedIn': loggedInSOL})

if __name__ == '__main__':
    app.run(debug=True)