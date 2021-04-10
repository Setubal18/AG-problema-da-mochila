from random import randrange
import random

def _gerarIndividuo():
    numero = str(random.random()).split('.')[1]
    pessoa = bin(int(numero)).split('b')[1]
    return pessoa[0:6]

def gerarPopulacao(quantidade=6):
    populacao = []
    for i in range(quantidade):
        populacao.append(_gerarIndividuo())
    return populacao

def fitness(populacao):
    aptidao =  [[5,7], [8,8], [3,4], [2,10], [7,4], [9,6], [4,4]]
    fit = []
    for numero,gene in enumerate(populacao):
        beneficio,custo = 0,0
        for i,g in enumerate(gene):
            if(g == '1'):
                beneficio+=aptidao[i][0]
                custo+=aptidao[i][1]
        nota = calculaFit(custo,beneficio)
        print(f'custo:{custo}; Beneficio: {beneficio}; nota: {nota}; Gene: {gene}')
        fit.append([gene,nota])
    return fit

def calculaFit(custo,beneficio):
    if(beneficio ==0 ):
        return 0
    else:
        if(custo>22):
            nota = custo/beneficio
            return round(nota,2)
        else:
            nota = (custo/beneficio) + 0.10
            return round(nota,2)

def cruzamento(lista):
    filhos = []
    for i in range(len(lista)):
        if(i+1 == len(lista)):
            filhos.append(lista[i][:3] + lista[i-1][3::])
            filhos.append(lista[i-1][:3] + lista[i][3::])
        else:
            filhos.append(lista[i][:3] + lista[i+1][3::])
            filhos.append(lista[i+1][:3] + lista[i][3::])
    return filhos

def mutacao(lista):
    novaLista = []
    for cromo in lista:
        novoGene = ''
        change = randrange(0,5)
        for i,gene in enumerate(cromo):
            if(i == change):
                gene = trocaCromossomo(gene)
            novoGene += gene
        novaLista.append(novoGene)
    return novaLista

def melhores(listaOrdenada):
    top3 = []
    for i,g in enumerate(listaOrdenada[:3]):
        top3.append(g[0])
    return top3, listaOrdenada[:3]
    
def trocaCromossomo(gene):
    if(gene == '1'):
        return '0'
    else:
        return '1'

def historico(lista):
    geracoes[len(geracoes)+1] = lista

populacao = gerarPopulacao()
geracoes = {}

print('populacao:',populacao)

for _ in range(100):
    fit = fitness(populacao)
    listaOrdenada = sorted(fit, key = lambda x: x[1],reverse=True)
    top3 , geracao = melhores(listaOrdenada)
    print('_________________')
    print('top 3:',top3)
    populacao = cruzamento(top3)
    populacao = mutacao(populacao)
    print('_________________')
    print(populacao)
    historico(geracao)
    print('_________________')
    print(geracoes)
    print('==============================')
