from flask import Flask, render_template, request
import googlemaps
from src.mygooglemap import allFunction
from src.forms import RouteForm

api_key = 'AIzaSyC4my9ZMi0RiUXYdWqsexT4JSwSbULFnLE'
gmaps = googlemaps.Client(key=api_key)

app = Flask(__name__)
app.secret_key = 'development key'


@app.route('/', methods=['GET', 'POST'])
def home():
    form = RouteForm()
    choices = []
    choices.insert(0, "Please enter your choice of route.")
    for i in range(len(allPath)): #length of all path =10
        choices.append('Option:_' + str(i+1).zfill(2)) #option  1->10
    choices.append("Shortest_Path_" + str(len(allPath)+1).zfill(2)) #11
    choices.append("Algo_Recommended_Route_" +str(len(allPath)+2).zfill(2)) #12
    form.route.choices = choices
    if request.method == 'POST':
        form.route.data = request.form['route']
        if request.form['route'] == "Please":
            form.route.data = 'None'
        if form.route.data != 'None':
            if int(form.route.data[-2:]) <= len(allPath):  # If route 1 -> 10
                dist = program.plotPath(allPath[int(form.route.data[-1])-1])# 0=1 , 1=2 .... 9 = 10
                form.route.dist = dist;
            elif int(form.route.data[-2:]) == len(allPath)+1: #if route = 11
                dist = program.plotPath(program.getShortest());
                form.route.dist = dist;
            elif int(form.route.data[-2:]) == len(allPath)+2: #if route = 12
                dist = program.plotPath(program.getAlgoReco());
                form.route.dist = dist;
        else:
            program.plotPath()
        return render_template('project.html', form=form)
    elif request.method == 'GET':
        program.plotPath()
        return render_template('project.html', form=form)

@app.route('/sentiment_analysis', methods=['GET', 'POST'])
def sentiment_analysis():
    return render_template('sentiment_analysis.html')


if __name__ == '__main__':
    program = allFunction(gmaps, api_key)
    allPath = program.getAllPath()
    program.plotPath()
    app.run(debug=True)
