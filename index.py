#pip install xlrd
from flask import Flask,render_template,request
import pandas as pd
import geopandas  as gpd
import contextily
import matplotlib.pyplot as plt



#per concludere l'es cerca su: https://towardsdatascience.com/web-visualization-with-plotly-and-flask-3660abf9c946
app = Flask(__name__)   #variabile che identifica il sito web


df = pd.read_excel('milano_housing_02_2_23.xlsx')

@app.route('/', methods=['GET'])  #sono tutte le possibili richieste del utente
def home():
    
    return render_template("indexHome.html")
################################Es1###########################
@app.route('/es1', methods=['GET'])  #sono tutte le possibili richieste del utente
def es1():
    
    return render_template("index1.html")

@app.route('/solEs1', methods = ['POST', 'GET'])  #sono tutte le possibili richieste del utente
def solEs1():
    quartiere = request.args.get('quartiere')
    dfInQurtieri = df[(df.neighborhood == quartiere) & (df.neighborhood == quartiere)].sort_values(by='date')

    return render_template("soluzione1.html",dfInQurtieri = dfInQurtieri.to_html())
################################Es2###########################
@app.route('/solEs2', methods = ['POST', 'GET'])  #sono tutte le possibili richieste del utente
def solEs2():
    sortedSe = list(set(df.neighborhood))
    sortedSeDF = pd.DataFrame(sortedSe, columns=['neighborhood'])
    PRsortedSeDF = sortedSeDF.sort_values('neighborhood')
    return render_template("soluzione2.html",PRsortedSeDF = PRsortedSeDF.to_html())
##############################Es3##################################
@app.route('/solEs3', methods=['GET'])  #sono tutte le possibili richieste del utente
def solEs3():
    ca = df.groupby(["neighborhood"]).count()[["energy_certification"]].reset_index().sort_values(by=["neighborhood"])
    ca2=ca.drop(['energy_certification'], axis = 1)
    return render_template("soluzione3.html", ca2 = ca2.to_html())
#############################Es4###################################
@app.route('/es4', methods=['GET'])  #sono tutte le possibili richieste del utente
def es4():
    
    return render_template("index4.html")

@app.route('/solEs4',  methods = ['POST', 'GET'])  #sono tutte le possibili richieste del utente
def solEs4():
    DfprezzoMedio = df.groupby("neighborhood")[["price"]].mean().reset_index().round(2)
    ricecaMidioPrezzoQ = request.args.get('ricecaMidioPrezzoQ')
    Se = DfprezzoMedio[(DfprezzoMedio.neighborhood == ricecaMidioPrezzoQ) & (DfprezzoMedio.neighborhood == ricecaMidioPrezzoQ)]
    return render_template("soluzione4.html", Se = Se.to_html())
#############################Es5###################################
@app.route('/solEs5',  methods = ['POST', 'GET'])  #sono tutte le possibili richieste del utente
def solEs5():
    DfprezzoMedio = df.groupby("neighborhood")[["price"]].mean().reset_index().round(2)
    DfDecrescente = DfprezzoMedio.sort_values(by=["price"],ascending=False)
    return render_template("soluzione5.html", DfDecrescente = DfDecrescente.to_html())
###############################Es6##################################
def euro_e_Yen(euro_Zip):
  convertitore = 123.04 # tasso di cambio fisso euro -> yen
  Yen_Zip = euro_Zip * convertitore
  return Yen_Zip


DfprezzoMedio = df.groupby("neighborhood")[["price"]].mean().reset_index().round(2)
DfDecrescente = DfprezzoMedio.sort_values(by=["price"],ascending=False)


@app.route('/solEs6',  methods = ['POST', 'GET'])  #sono tutte le possibili richieste del utente
def solEs6():
    dfYenizziamo = euro_e_Yen(DfDecrescente[["price"]])
    soluzione = pd.merge(left=dfYenizziamo, right=DfDecrescente, how='right', on='price')
    soluzione = [soluzione.price.notnull()].sort_values(by=["neighborhood"])
    return render_template("soluzione6.html", soluzione = soluzione.to_html())

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)    #fà partire il programma