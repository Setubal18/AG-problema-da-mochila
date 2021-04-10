from random import randrange,random


def get_itens():
    return {
        0:{'name':'Cachorro-Quente','values':[3,4]}, 
        1:{'name':'Chambari','values':[8,5]}, 
        2:{'name':'Cuscuz','values':[7,4]}, 
        3:{'name':'Guarana Jesus','values':[3,7]}, 
        4:{'name':'Hamburger','values':[6,6]}, 
        5:{'name':'Pizza','values':[6,5]}, 
        6:{'name':'Sarapatel','values':[5,3]}, 
        7:{'name':'Tapioca','values':[5,4]}
        }

#nessa funcao eu apenas pego numeros decimais aleatorios e transform em binarios com 8 espaços
def _gerarIndividuo():
    numero = str(random()).split('.')[1]
    pessoa = bin(int(numero)).split('b')[1]
    return pessoa[0:8]

#aqui defini qual a quantidade total da minha população
def gerarPopulacao(quantidade=8):
    populacao = []
    for i in range(quantidade):
        populacao.append(_gerarIndividuo())
    return populacao

#No fit defini que cada '1' no cromosso seria que o usuário carrega e '0' ele não carrega.
def fitness(populacao):
    itens =  get_itens()
    fit = []
    for numero,gene in enumerate(populacao):
        grauDeDificuldade,bonus,carga = 0,0,''
        for i,g in enumerate(gene):
            if(g == '1'):
                grauDeDificuldade+=itens[i]['values'][0]
                bonus+=itens[i]['values'][1]
                carga = montarCarga(itens[i]["name"],carga)
        nota = calculaFit(bonus,grauDeDificuldade)
        print(f'A nota do gene {gene} foi de: {nota}, e dentro da caixa de transporte possui as seguinte carga: {carga}')
        fit.append([gene,nota,carga])
    return fit

#Já nessa função eu execulto o calculo do fit, sendo que caso o grau de dificuldade passe de 25 a nota receba uma penalização de 0.10
#Caso ele tenha exatos 25 de grau de dificuldade ele não recebe nenhum bonus, mas caso ele consiga menos ele recebe um bonus de 0.11
def calculaFit(bonus,grauDeDificuldade):
    if(grauDeDificuldade == 0 ):
        return 0
    else:
        if(grauDeDificuldade>25):
            nota = (bonus/grauDeDificuldade) - 0.10
            return round(nota,2)
        if (grauDeDificuldade == 25):
             nota = (bonus/grauDeDificuldade)
             return round(nota,2)
        else:
            nota = (bonus/grauDeDificuldade) + 0.11
            return round(nota,2)

#Apenas formata a string de carga 
def montarCarga(item,carga):
    if carga:
        carga += f' + {item}'
    else:
        carga = item
    return carga

#Seleciona apenas os melhores genes.
def melhores(listaOrdenada,qtd=3):
    top = []
    for i,g in enumerate(listaOrdenada[:qtd]):
        top.append(g[0])
    return top, listaOrdenada[:qtd]

#No cruzamento escolhi por utilizar 4 genes dos mais do inicio e final, depois realizo a mesma coisa ao contrario, sendo q cada par de pais geram dois filhos
#Sendo assim, no final gero denovo a mesma população inicial de 8 individuos
def cruzamento(lista):
    filhos = []
    for i in range(len(lista)):
        if(i+1 == len(lista)):
            filhos.append(lista[i][:4] + lista[i-1][4::])
            filhos.append(lista[i-1][:4] + lista[i][4::])
        else:
            filhos.append(lista[i][:4] + lista[i+1][4::])
            filhos.append(lista[i+1][:4] + lista[i][4::])
    return filhos

#A mutação corre apenas quando o numero randomico gerado for o.650(65.0%). Assim que um novo individuo e apto para ter a mutaçao
#um gene é escolhido aleatoriamente para ocorrer essa mutação.
def mutacao(lista):
    novaLista = []
    for cromo in lista:
        novoGene = ''
        if(round(random(),3)>0.650):
            change = randrange(0,7)
            for i,gene in enumerate(cromo):
                if(i == change):
                    gene = trocaCromossomo(gene)
                novoGene += gene
            novaLista.append(novoGene)
        else:
            novaLista.append(cromo)
    return novaLista
    
#Nessa funcao apenas ocorre a inversão de cromossomos. caso ele seja '1' ele vira '0' e virse versa.
def trocaCromossomo(gene):
    if(gene == '1'):
        return '0'
    else:
        return '1'

#mostra os melhores de cada geracao
def mostraGeracoes():
    for i in range(len(geracoes)):
        gen =  geracoes[i]
        print(f'GERAÇÃO  {i}:')
        for n in range(len(gen)):
            print(f'   Colocação {n+1}:')
            print(f'     Possui o seguinte genes: {gen[n][0]}; com o fit/nota de {gen[n][1]};')
            print(f'     Possui tambem a(s) seguinte(s) carga(s) {gen[n][2]}.')
        print(f'--------------------------------------------------------------------------------------------------')
populacao = gerarPopulacao()
geracoes = []

for _ in range(10):
    print(f'{_} populacao:',populacao)
    fit = fitness(populacao)
    #Aqui apenas ordeno pela nota deixando o com maior nota no topo
    listaOrdenada = sorted(fit, key = lambda x: x[1],reverse=True)
    top , geracao = melhores(listaOrdenada,qtd=4)
    geracoes.append(geracao)
    populacao = cruzamento(top)
    populacao = mutacao(populacao)
    print('==============================')
mostraGeracoes()
