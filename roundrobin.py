'''
RoundRobin PIBEX – Sistema de Distribuição de Bolsas
Desenvolvido por Profa. Dra. Pamela Michele Candida Cortez, UEFS-BA
Contato: pamela@uefs.br

Realiza a distribuição de bolsas com base nas regras dos editais PIBEX/UEFS de 2025, garantindo as bolsas reservadas para ações afirmativas, considerando o limite de bolsas por orientador e por projeto.
rodada 1 = 1 por consepe
rodada 2 = 1 por consepe se Programa
rodada 3 = ranking

Desempate:
a) Maior nota no Plano de Trabalho; coluna: Nota do Plano de Trabalho pós-recurso
b) Maior nota de Currículo Docente; coluna: Currículo Docente pós-recurso
c) Maior nota de Currículo Discente. coluna: Currículo Discente pós-recurso

Instruções de Uso
O usuário fornece: nome do arquivo CSV, número de bolsas para o edital específico (n1), número de bolsas para o edital geral (n2)
O programa retorna: arquivo CSV “resultado.csv” com o status de cada plano na última coluna. Arquivos auxiliares “projetos.csv” e “professores.csv” com a quantidade de bolsas para cada projeto e orientador.

Para executar no VS Code:
python -m venv myenv
source myenv/bin/activate
pip install pandas
python3 roundrobin.py <nome do arquivo>.csv n1 n2
exemplo: python3 roundrobin.py entrada.csv 50 320

Exemplo de saída, considerando os editais PIBEX de 2025:
Edital PIBEX 02/2025 - Programas Específicos
Ações afirmativas  outros  : 1 rodadas, nota de corte = 8.40, bolsas =   3, aprovados =   2/  2, total =   2
Ações afirmativas não negro: 1 rodadas, nota de corte = 8.15, bolsas =   5, aprovados =   5/  5, total =   7
Ações afirmativas   negro  : 1 rodadas, nota de corte = 7.25, bolsas =  18, aprovados =  16/ 21, total =  23
Ações afirmativas   ampla  : 1 rodadas, nota de corte = 7.05, bolsas =  27, aprovados =  25/ 66, total =  48
Edital PIBEX 01/2025 - Geral
Ações afirmativas  outros  : 3 rodadas, nota de corte = 7.85, bolsas =  16, aprovados =  12/ 12, total =  60
Ações afirmativas não negro: 3 rodadas, nota de corte = 8.70, bolsas =  32, aprovados =  28/ 28, total =  88
Ações afirmativas   negro  : 3 rodadas, nota de corte = 7.10, bolsas = 112, aprovados = 106/135, total = 194
Ações afirmativas   ampla  : 3 rodadas, nota de corte = 8.65, bolsas = 176, aprovados = 176/444, total = 370
Total de aprovados: 48 + 322 = 370

É vedada a reprodução, total ou parcial, com ou sem alterações, sem a devida citação da fonte.
'''

import sys
import math
import pandas as pd
from functools import reduce

N_PROFESSOR = 6 # limite de bolsas por professor
N_PROGRAM = 6   # limite de bolsas por programa
N_PROJECT = 4   # limite de bolsas por projeto
N_SPECIFIC_PROJECTS = 5 # número de projetos no edital específico - considera-se que todos recebem a mesma qtde de bolsas
cotas = {"outros": 0.1, "não negro" : 0.2, "negro" : 0.7, "ampla": 0.0} # porcentagens. Não usar "-" entre as palavras na coluna Ação Afirmativa no csv de entrada

def roundRobin(df, nscholarships, project, professor, students):
    min_mark = 128    
    approvals = 0
    
    for i in range(1,4):
        for index, row in df.iterrows():
            #print(index, " ", row["Nota Final do pedido de bolsa"])
            edital     = row["Edital"]
            consepe    = row["CONSEPE"]
            orientador = row["Orientador do Plano de Trabalho"]
            aluno      = row["Matricula Discente"]
            tipo       = row["Tipo"]
            
            #studentResult = None if dftemp is None else dftemp.loc[dftemp["Matricula Discente"] == aluno, "Resultado"]
            #studentResult = "" if studentResult is None or studentResult.empty or pd.isna(studentResult.item()) else str(studentResult)
            """ if consepe == 782025:
                print(aluno not in students)
                print(tipo)
                print(edital)
                print(professor[orientador])
                print(project[consepe]) """
                
            if aluno not in students and professor[orientador] < N_PROFESSOR and (i != 2 or tipo == "Programa") and\
                ( ("espec" in edital.lower() and project[consepe] < n1//N_SPECIFIC_PROJECTS) or ( ((tipo == "Programa" and project[consepe] < N_PROGRAM) or project[consepe] < N_PROJECT) and\
                (i > 2 or project[consepe] < max(i - (0 if tipo == "Programa" else 1), 1)) ) ):

                df.loc[index, "Resultado"] = f"Convocado na rodada {i}"
                project[consepe] += 1
                professor[orientador] += 1

                students.add(aluno)
                if i > 2 and min_mark > row["Nota Final do pedido de bolsa"]:
                    min_mark = row["Nota Final do pedido de bolsa"]
                #print(project[consepe], " ", max(i - (0 if tipo == "Programa" else 1), 1))

                approvals += 1
                if approvals == nscholarships:
                    return approvals, i, min_mark, df
    
    return approvals, i, min_mark, df

def rrUtil(df, nscholarships, project, professor, students, surplus = 0):
    approvals = [0] * len(cotas)
    dftemp = [None] * len(cotas)
    i = 0
    qtype = list(cotas.keys())
    search_pattern = '|'.join(qtype)
    # print(search_pattern)
    
    for (key, value) in cotas.items():
        n = int(math.ceil(nscholarships/2*value)) if key != "ampla" else nscholarships + surplus - sum(approvals)
        mask = df["Ação Afirmativa"].str.contains(key if i else search_pattern, case=False, na=False, regex=True)
        df_i = df[mask if i else ~mask] if key != "ampla" else df
        approvals[i], round, min_mark, dftemp[i] = roundRobin(df_i, n, project, professor, students)
        
        print(f"Ações afirmativas {key:^9}: {round} rodadas, nota de corte = {dftemp[i]["Nota Final do pedido de bolsa"].min() if min_mark > 100 else min_mark:.2f}, bolsas = {n:3d}, "
              f"aprovados = {approvals[i]:3d}/{df_i.shape[0]:3d}, total = {len(students):3d}")# ({sum(professor.values()):3d}, {sum(project.values()):3d})")
        i += 1

    df.loc[df.index.isin(reduce(pd.Index.union,[d.index[d["Resultado"].str.contains("Convocado", case=False, na=False, regex=False)] for d in dftemp])), "Resultado"] = "Convocado"
    return sum(approvals), df

def saveDict(data, filename):
    # print(data)
    data = dict(sorted(data.items(), key=lambda item: item[1], reverse=True))
    df = pd.DataFrame(list(data.items()), columns=["nome", "quantidade"])
    df.to_csv(filename+".csv", sep=";", index=False)
    
def main(filename, n1, n2):
    df = pd.read_csv(
        filename,
        sep=",",
        quotechar='"',
        escapechar="\\",
        engine="python"
    )
    
    df["Nota Final do pedido de bolsa"] = df["Nota Final do pedido de bolsa"].str.replace(",", ".").astype(float)
    df["Nota do Plano de Trabalho pós-recurso"] = df["Nota do Plano de Trabalho pós-recurso"].str.replace(",", ".").astype(float)
    df["Currículo Docente pós-recurso"] = df["Currículo Docente pós-recurso"].str.replace(",", ".").astype(float)
    df["Currículo Discente pós-recurso"] = df["Currículo Discente pós-recurso"].str.replace(",", ".").astype(float)
    df = df.sort_values(
    by=[
        "Nota Final do pedido de bolsa",
        "Nota do Plano de Trabalho pós-recurso",
        "Currículo Docente pós-recurso",
        "Currículo Discente pós-recurso",
    ], ascending=[False, False, False, False]).reset_index(drop=True)

    df["Resultado"] = "Cadastro Reserva"

    mask_notapproved = (df["Nota Final do pedido de bolsa"] < 7) | (df["Eliminado do processo?"].fillna("").str.strip() != "")
    unapproved = df.loc[mask_notapproved].copy()
    unapproved["Resultado"] = "Não Aprovado"

    students = set()
    project = dict.fromkeys(df["CONSEPE"].unique(), 0)
    professor = dict.fromkeys(df["Orientador do Plano de Trabalho"].unique(), 0)
    
    calls = df["Edital"].unique()
    callForScholarships1 = next((s for s in calls if "espec" in s.lower()), None)
    callForScholarships2 = next((s for s in calls if s != callForScholarships1), None)
    mask_call1 = df["Edital"] == callForScholarships1
    
    df1 = df.loc[~mask_notapproved & mask_call1].copy()
    df2 = df.loc[~mask_notapproved & ~mask_call1].copy()
    print(callForScholarships1)
    approvals1, df1 = rrUtil(df1, n1, project, professor, students) # Edital PIBEX Programas Específicos (espec)
    print(callForScholarships2)
    approvals2, df2 = rrUtil(df2, n2, project, professor, students, n1 - approvals1) # Edital PIBEX 01/2025 - Geral
    print(f"Total de aprovados: {approvals1} + {approvals2} = {approvals1+approvals2}")# (Projects = {sum(project.values())}, Professors = {sum(professor.values())})")

    df = pd.concat([df1, df2, unapproved], ignore_index=True)
    #df.loc[~df["Matricula Discente"].isin(students), "Resultado"] = "Cadastro Reserva"
    #df = pd.concat([df, unapproved], ignore_index=True)
    
    df["Nota Final do pedido de bolsa"] = df["Nota Final do pedido de bolsa"].astype(str).replace(".", ",", regex=False)
    df["Edital"] = df["Edital"].str.replace(callForScholarships2, "#", regex=False)
    df["Edital"] = df["Edital"].str.replace(callForScholarships1, "@", regex=False)
    df = df.sort_values(by=['Edital', 'Orientador do Plano de Trabalho'], ascending=[True, True])
    df["Edital"] = df["Edital"].str.replace("#", callForScholarships2, regex=False)
    df["Edital"] = df["Edital"].str.replace("@", callForScholarships1, regex=False)
    df.to_csv("resultado.csv", sep=";", index=False)
    saveDict(project, "projetos")
    saveDict(professor, "professores")

try:
    n1 = int(sys.argv[2])
    n2 = int(sys.argv[3])
except ValueError:
    print("Number of scholarships in the Specific Call and number of scholarships in the General Call must be integers")
    sys.exit(1)
    
main(sys.argv[1], n1, n2)
