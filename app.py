from flask import Flask, render_template, request
from uuid import uuid4
import pandas as pd
import csv

app = Flask(__name__)

# Faz a leitura do filmes.csv e manda para home.html
@app.route('/')
def index():
    with open('filmes.csv', 'rt') as file_in:
        filmes = csv.DictReader(file_in)
        return render_template('home.html', filmes=filmes)

# Para a criação da variável
@app.route('/create')
def create():
    return render_template('create.html')

#Salva os dados do forms em uma row no filmes.csv
@app.route('/save', methods=['POST'])
def save():

    #Puxa os dados do forms
    name = request.form['name']         
    avaliacao = request.form['avaliacao'] 
   
    #Cria uma id para os dados
    entrada= []
    entrada.append([uuid4(), name, avaliacao]) 

    #Adiciona uma nova row no filmes.csv
    with open('filmes.csv', 'a') as file_out:
        escritor = csv.writer(file_out)
        escritor.writerows(entrada)
   
    #Manda para o '/'
    with open('filmes.csv', 'rt') as file_in:
        filmes = csv.DictReader(file_in)
        return render_template('home.html', filmes=filmes)

#Deleta rows pelo Id dos dados
@app.route('/delete/<id>')
def delete(id):

    #Abre o filmes.csv pelo pandas 
    data = pd.read_csv("filmes.csv") 

    #Seta o index valeu para a columm 'Id'
    data = data.set_index("Id") 

    #dropa toda row que tiver a mesma variavel 'id' na columm index
    data.drop(id, axis='index', inplace=True) 
    
    #Salva o novo dataset
    data.to_csv('filmes.csv')  

    #Faz a leitura dos arquivos e envia os dados para o Html 
    with open('filmes.csv', 'rt') as file_in:
        filmes = csv.DictReader(file_in)
        return render_template('home.html', filmes=filmes)
    
#Puxa os dados da row que o usuário quer editar e coloca dentro dos forms
@app.route('/edit/<id>/<name>/<avaliacao>')
def update(id,name,avaliacao):

    #Cria uma lista para facilitar
    lista = [id,name,avaliacao]

    #Manda para o edit.html
    return render_template('edit.html', lista=lista) 

#Salva os forms editados no /saveEdit
@app.route('/saveEdit', methods=['POST'])
def saveedit():

    #Pede os novos dados
    id = request.form['Id'] 
    name = request.form['name']         
    avaliacao = request.form['avaliacao'] 
 
    #Abre os dadtaframe do filmes.csv
    data = pd.read_csv("filmes.csv")

    #Cria um novo dataframe apartir dos novos dados
    new_df = pd.DataFrame({'Id': [id],'Name': [name],'Avaliacao': [avaliacao]})

    #Coloca os index's para a coluna 'Id'
    data = data.set_index("Id")
    new_df = new_df.set_index("Id")

    #Atualiza os dados do dataframe
    data.update(new_df)

    #Salva o novo dataset
    data.to_csv('filmes.csv')

    #Manda para o '/'
    with open('filmes.csv', 'rt') as file_in:
        filmes = csv.DictReader(file_in)
        return render_template('home.html', filmes=filmes)

app.run(debug=True)
