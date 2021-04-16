from flask import *
import os
import pandas as pd

def check(string, sub_str):
    if (string.find(sub_str) == -1):
        return False
    else:
        return True

app= Flask(__name__)



@app.route('/')
def validate():
    return render_template('index.html')

@app.route('/upload', methods = ['POST'])
def success():
    if request.method == 'POST':
        try:
            f = request.files['source']
            f.save(f.filename)
            os.rename(f.filename,'SOURCE-FILE.csv')
            f = request.files['presentList']
            f.save(f.filename)
            os.rename(f.filename, 'chat.txt')

            df = pd.read_csv(r"C:\Users\KIIT\PycharmProjects\pythonProject\Python Lab\Mini Project1.2\SOURCE-FILE.csv");
            f1 = open('chat.txt', 'r')
            df.set_index('Roll No.', inplace=True)
            present = []

            while True:
                line = f1.readline()
                if not line:
                    break;
                rollEntered = line.rsplit(": ", 1)[-1]
                rollEntered = rollEntered.strip()
                last3 = rollEntered[len(rollEntered) - 3:]
                line = line.rsplit(": ", 1)[-2]
                # print(rollEntered,line,check(line,rollEntered))
                if (rollEntered.isdigit()):
                    if (check(line, rollEntered) or check(line, last3) or check(line.upper(),
                                                                                df['Student Name'].loc[int(rollEntered)])):
                        present.append(rollEntered)

            print(present)
            present = list(set(present))
            print(present)
            f1.close()
            df['Attendance'] = 'Abs'
            for i in present:
                df.at[int(i), 'Attendance'] = 'Present'

            res=df[{'Student Name','Attendance'}].loc[df['Attendance'] == "Abs"]
            res.to_html('C:/Users/KIIT/PycharmProjects/pythonProject/Python Lab/Mini Project1.2/templates/success.html')

            return render_template("success.html")
        except:
            return render_template("error.html")

app.run(debug=True)
