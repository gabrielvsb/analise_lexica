# while i < 100 do i = i + j;

import csv
import sys

# ---------------LINGUAGEM------------------
linguagem1 = {
    'palavras_reservadas': ['while', 'do'],
    'operadores': ['<', '=', '+'],
    'identificadores': ['i', 'j'],
    'terminador': [';'],
    'numeros': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
}
# ------------------------------------------


class Analisador:
    def __init__(self, linguagem, entrada):
        self.linguagem = linguagem
        self.dicionario_token = []
        self.dicionario_simbolos = {}
        self.entrada = entrada
        self.lista = entrada.split(' ')
        self.verifica_simbolos(self.linguagem, self.dicionario_simbolos, self.lista)
        self.verifica_linguagem(self.lista, self.linguagem, self.dicionario_token)

        if len(self.dicionario_token) > 0:
            self.cria_csv_token(self.dicionario_token)
        else:
            print('O dicionario de tokens não pode ser criado.')
            sys.exit()
        if len(self.dicionario_simbolos) > 0:
            self.cria_csv_simbolos(self.dicionario_simbolos)
        else:
            print('O dicionario de simbolos não pode ser criado.')
            sys.exit()

    def verifica_linguagem(self, lista, lang, dicio):
        for le in lista:
            if le.isnumeric():
                if self.verifica_numero(le, lang):
                    self.adiciona_dicionario_token(le, dicio, 'Constante', True)
                else:
                    print('Este número não faz parte da base de números da linguagem')
                    sys.exit()
            else:
                if le in lang['palavras_reservadas']:
                    self.adiciona_dicionario_token(le, dicio, 'Palavra reservada', False)
                elif le in lang['operadores']:
                    self.adiciona_dicionario_token(le, dicio, 'Operador', False)
                elif le in lang['identificadores']:
                    self.adiciona_dicionario_token(le, dicio, 'Identificador', True)
                elif le in lang['terminador']:
                    self.adiciona_dicionario_token(le, dicio, 'Terminador', False)
                else:
                    print(f'{le} não faz parte do dicionario desta linguagem. Verifique a ortografia.')
                    sys.exit()

    @staticmethod
    def verifica_terminador(lista, lang):
        terminador = str(lista[-1][-1])
        if terminador in lang['terminador']:
            for item in lista:
                if terminador in item:
                    lista[lista.index(item)] = item.replace(';', '')
            lista.append(terminador)
            return True
        else:
            print(f'{terminador} não faz parte do dicionario desta linguagem. Verifique a ortografia')
            return False

    @staticmethod
    def verifica_posicao(item):
        global analise
        if item == 'i':
            pos = analise.find('i ')
            analise = analise.replace('i ', '£ ', 1)
        else:
            pos = analise.find(item)
        return pos

    @staticmethod
    def verifica_numero(item, lang):
        for n in item:
            if int(n) not in lang['numeros']:
                return False
        return True

    def adiciona_dicionario_token(self, item, dicio, idf, is_identificador):
        if is_identificador:
            identificador = f'[{idf}, {self.dicionario_simbolos[item]["index"]}]'
        else:
            identificador = idf
        dicio.append(
            {
                'token': item,
                'id': identificador,
                'tamanho': len(item),
                'posicao': f'(0, {self.verifica_posicao(item)})'
            }
        )

    @staticmethod
    def adiciona_dicionario_simbolos(index, simbolo, dicio):
        dicio[str(simbolo)] = {
            'index': index,
            'simbolo': str(simbolo),
        }

    @staticmethod
    def cria_csv_token(dicio):
        with open('csv_token.csv', mode='w', newline='') as csv_file:
            fieldnames = ["Token", "Identificação", "Tamanho", "Posição"]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for i in dicio:
                writer.writerow({"Token": i['token'],
                                 "Identificação": i['id'],
                                 "Tamanho": i['tamanho'],
                                 "Posição": i['posicao']})

    @staticmethod
    def cria_csv_simbolos(dicio):
        with open('csv_simbolos.csv', mode='w', newline='') as csv_file:
            fieldnames = ["Index", "Simbolo"]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for key in dicio.keys():
                writer.writerow({"Index": dicio[key]['index'],
                                 "Simbolo": dicio[key]['simbolo']
                                 })

    def verifica_simbolos(self, lang, dicio, lista):
        cont = 1
        aux = []
        if self.verifica_terminador(lista, lang):
            for item in lista:
                if item not in aux:
                    if item.isnumeric():
                        if self.verifica_numero(item, lang):
                            self.adiciona_dicionario_simbolos(cont, int(item), dicio)
                            aux.append(item)
                            cont += 1
                        else:
                            print('Este número não faz parte da base de números da linguagem')
                            return False
                    else:
                        if item in lang['identificadores']:
                            self.adiciona_dicionario_simbolos(cont, item, dicio)
                            aux.append(item)
                            cont += 1


# analise = 'while i < 100 do i = i + j;'
analise = str(input('Digite o codigo a ser analisado: '))
teste = Analisador(linguagem1, analise)
teste
