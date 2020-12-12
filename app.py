import numpy as np
from flask import Flask, render_template, request

import re
import nltk
import random
import string
import spacy


def read_file(fpath):
    '''
    retorna str
    '''
    with open(fpath, encoding="utf8") as f:
        text = f.read()
    return text


paragrafos = read_file('respostas.txt')

conteudo = ''
for p in paragrafos:
  conteudo += p
conteudo = conteudo.lower()
lista_sentencas = nltk.sent_tokenize(conteudo)

pln = spacy.load('pt_core_news_sm')
stop_words = spacy.lang.pt.stop_words.STOP_WORDS

def preprocessamento(texto):
  # URLs
  texto = re.sub(r"https?://[A-Za-z0-9./]+", ' ', texto)

  # Espaços em branco
  texto = re.sub(r" +", ' ', texto)

  documento = pln(texto)
  lista = []
  for token in documento:
    lista.append(token.lemma_)

  lista = [palavra for palavra in lista if palavra not in stop_words and palavra not in string.punctuation]
  lista = ' '.join([str(elemento) for elemento in lista if not elemento.isdigit()])

  return lista

lista_sentencas_preprocessada = []

for i in range(len(lista_sentencas)):
  lista_sentencas_preprocessada.append(preprocessamento(lista_sentencas[i]))

for _ in range(5):
  i = random.randint(0, len(lista_sentencas) - 1)

textos_boas_vindas_entrada = ('hey', 'olá', 'tudo bem', 'oi', 'eae')
textos_boas_vindas_respostas = ('hey', 'olá', 'oi')
'olá tudo bem'.split()

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

frases_teste = lista_sentencas_preprocessada[:3]
frases_teste.append(frases_teste[0])

vetores_palavras = TfidfVectorizer()
palavras_vetorizadas = vetores_palavras.fit_transform(frases_teste)
palavras_vetorizadas.todense()

palavras_vetorizadas[0].todense()
cosine_similarity(palavras_vetorizadas[0], palavras_vetorizadas[1])
cosine_similarity(palavras_vetorizadas[0], palavras_vetorizadas[2])
similaridade = cosine_similarity(palavras_vetorizadas[0], palavras_vetorizadas)
similaridade.argsort()
i = similaridade.argsort()[0][-2]
i = i.flatten()


def responder_saudacao(texto):
  for palavra in texto.split():
    if palavra.lower() in textos_boas_vindas_entrada:
      return random.choice(textos_boas_vindas_respostas)


'''def responder(texto_usuario):
  resposta_chatbot = ''
  lista_sentencas_preprocessada.append(texto_usuario)

  tfidf = TfidfVectorizer()
  palavras_vetorizadas = tfidf.fit_transform(lista_sentencas_preprocessada)

  similaridade = cosine_similarity(palavras_vetorizadas[-1], palavras_vetorizadas)

  indice_sentenca = similaridade.argsort()[0][-2]
  vetor_similar = similaridade.flatten()
  vetor_similar.sort()
  vetor_encontrado = vetor_similar[-2]

  if (vetor_encontrado == 0):
    resposta_chatbot = resposta_chatbot + 'Desculpe, eu não entendi.'
    return resposta_chatbot
  else:
    resposta_chatbot = resposta_chatbot + lista_sentencas[indice_sentenca]
    return resposta_chatbot'''


app = Flask(__name__)


@app.route("/")
def index():
     return render_template("chatbot.html") #to send context to html


@app.route("/get")
def get_bot_response():
     texto_usuario = request.args.get("msg") #get data from input,we write js  to chatbot.html
     resposta_chatbot = ''
     lista_sentencas_preprocessada.append(texto_usuario)

     tfidf = TfidfVectorizer()
     palavras_vetorizadas = tfidf.fit_transform(lista_sentencas_preprocessada)

     similaridade = cosine_similarity(palavras_vetorizadas[-1], palavras_vetorizadas)

     indice_sentenca = similaridade.argsort()[0][-2]
     vetor_similar = similaridade.flatten()
     vetor_similar.sort()
     vetor_encontrado = vetor_similar[-2]

     if (vetor_encontrado == 0):
         resposta_chatbot = resposta_chatbot + 'Desculpe, eu não entendi.'
         return str(resposta_chatbot)
     else:
         resposta_chatbot = resposta_chatbot + lista_sentencas[indice_sentenca]
         return str(resposta_chatbot)

'''@app.route("/get")
def conversar():
    print('Olá, eu sou o Babel, o chatbot do Instituto de Letras. Eu posso responder perguntas relacionadas à graduação como:'
          '\nCalendário Acadêmico;'
          '\nConcessão de Créditos;'
          '\nMatrícula;'
          '\nMonitoria;'
          '\nMenção;'
          '\nEmissão de documentos;'
          '\nAtendimento com Coordenadores.')
    resposta = ''
    texto_usuario = request.args.get("msg")
    if responder_saudacao(texto_usuario) != None:
        resposta = 'Babel: ' + responder_saudacao(texto_usuario)
    else:
        resposta = responder(preprocessamento(texto_usuario))
        lista_sentencas_preprocessada.remove(preprocessamento(texto_usuario))
    return str(resposta())
#conversar()
'''

if __name__ == '__main__':
    app.run(host="https://chat-com-html.herokuapp.com/", debug=True)

