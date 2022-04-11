from flask import Flask, request, redirect
import json
import datetime
import subprocess
import sys
app = Flask(__name__)

@app.route("/say", methods= ['POST'])
def say():
    data = request.form.to_dict()["speech"]
    print()
    if sys.platform == 'linux':
        command = ["espeak", "-v", "mb-en1", f'" - ... - {data}"', "-p65", "-s180"]
    elif sys.platform == 'darwin':
        command = ["say", f'" - ... - {data}"']
    subprocess.Popen(command)
    return redirect("/")

@app.route("/", methods = ['GET', 'POST'])
def main():
    with open("people.json", "r") as file:
        people = json.load(file)

    if request.method == 'POST':
        data = request.form.to_dict()
        for mac in data.keys():
            people[mac]["name"] = data[mac]
        with open("people.json", "w") as file:
            file.write(json.dumps(people, indent=4))

    html_string = """
    <body>
     <h1>Gjester</h1>
     <form method="post">
     <table style="border: 1px solid black;">
      <tr>
       <th>Navn</th>
       <th>IP</th>
       <th>MAC</th>
       <th>First seen</th>
       <th>Last seen</th>
      </tr>
    """

    for mac in people.keys():
        html_string += f"""
        <tr>
         <th><input name={mac} type="text" value="{people[mac]["name"]}"></input></th>
         <th>{people[mac]["ip"]}</th>
         <th>{mac}</th>
         <th>{datetime.datetime.fromtimestamp(people[mac]["first_seen"]).strftime('%Y-%m-%d %H:%M:%S')}</th>
         <th>{datetime.datetime.fromtimestamp(people[mac]["last_seen"]).strftime('%Y-%m-%d %H:%M:%S')}
        </tr>
        """
    html_string += """
      </table>
      <button type="submit">Lagre</button>
     </form>
     <h1>Make the screen say something</h1>
     <form action="/say" method="post">
     What should the screen say: <input type="text" name="speech"></input>
     </form>
    </body>
    """
    return html_string