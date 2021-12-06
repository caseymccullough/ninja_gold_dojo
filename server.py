from flask import Flask, render_template, request, redirect, session
from random import randint

app = Flask(__name__)
app.secret_key = "myverysecretkey"

options = {
   'farm': (10, 20),
   'cave': (5, 10),
   'house': (2, 5),
   'casino': (-50, 50)
}

def getRandNum(min, max):
   return randint(min, max)

@app.route('/')
def default():
   print('default route')
   if "gold" not in session:
      print('creating session variables')
      session['gold'] = 0
      session['activities'] = []
   return render_template('index.html')

@app.route('/process_money', methods = ['POST'])
def process_money():
   print(f"** Processing money {session['gold']}")
   building_selected = request.form['building']
   minMaxTuple = options[building_selected]
   gold_adjust = getRandNum(minMaxTuple[0], minMaxTuple[1])
   print(gold_adjust)
   session['gold'] += gold_adjust

   activity_str = "<li"
   if gold_adjust > 0:
      activity_str += ' class= "win"> '
   elif gold_adjust < 0:
      activity_str += ' class= "loss"> '
   activity_str += f"{building_selected} for {gold_adjust} for new total of {session['gold']} </li>"
   
   print ("new activity", activity_str)
   session['activities'].append(activity_str)
   return redirect('/')

@app.route("/reset")
def reset():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
   app.run(debug=True)

