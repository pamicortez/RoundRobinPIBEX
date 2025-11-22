# RoundRobinPIBEX
Sistema de Distribuição de Bolsas: realiza a distribuição de bolsas com base nas regras dos editais PIBEX/UEFS de 2025, garantindo as bolsas reservadas para ações afirmativas, considerando o limite de bolsas por orientador e por projeto.<br>
<br>
Input Format<br>
O programa deve receber o nome de um arquivo CSV com pelo menos as seguintes colunas (nome das colunas não podem ser alteradas):
<br>
<table>
    <thead>
        <tr>
            <th>Nome da coluna</th>
            <th>Descrição / Notas</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Matricula Discente</td>
            <td>Identificador único do estudante (Student ID).</td>
        </tr>
        <tr>
            <td>Nota Final do pedido de bolsa</td>
            <td>Pontuação final (valor numérico ou string com vírgula como separador decimal).</td>
        </tr>
        <tr>
            <td>Ação Afirmativa</td>
            <td>Tipo de ação afirmativa ou "Ampla Concorrência" (General Admission).</td>
        </tr>
        <tr>
            <td>CONSEPE</td>
            <td>Identificador do projeto no sistema CONSEPE (Project Identifier).</td>
        </tr>
        <tr>
            <td>Tipo</td>
            <td>Indica se é "Programa" ou "Projeto".</td>
        </tr>
        <tr>
            <td>Orientador do Plano de Trabalho</td>
            <td>Nome do orientador ou supervisor do plano de trabalho (Advisor Name).</td>
        </tr>
        <tr>
            <td>Eliminado do processo?</td>
            <td>Razão pela qual o candidato foi eliminado do processo seletivo, célula vazia caso contrário.</td>
        </tr>
        <tr>
            <td>Resultado</td>
            <td>Coluna criada e preenchida pelo programa (status final).</td>
        </tr>
    </tbody>
</table>
<br>
CSV deve conter os dois editais. O edital de chamadas específico deve conter a substring "espec"<br>
Exemplo:<br>
Edital PIBEX 02/2025 - Programas Específicos<br>
Edital PIBEX 01/2025 - Geral<br>
<br>
How the Algorithm Works<br>
The selection occurs in rounds:<br>
<br>
1st Round<br>
One candidate per CONSEPE<br>
Any type (Programa/Projeto)<br>
Must satisfy advisor/project limits<br>
<br>
2nd Round<br>
One per CONSEPE<br>
Only candidates from Programa<br>
Same global constraints<br>
<br>
from the 3rd Round on<br>
according to score (ranking)<br>
Same global constraints<br>
<br>
The algorithm enforces:<br>
One scholarship per project/program in each round (unless it is a specific call — projects with a predefined number of scholarships)<br>
Max 4 scholarships per Projeto, or 6 for Programa<br>
Max 6 scholarships per advisor<br>
No duplicate students<br>
<br>
After the selection, non-selected candidates default to: Cadastro Reserva, Aprovado or Não Aprovado<br>
<br>
<br>
Constants block (edit as needed)<br>
N_PROFESSOR = 6 # limite de bolsas por professor<br>
N_PROGRAM = 6   # limite de bolsas por programa<br>
N_PROJECT = 4   # limite de bolsas por projeto<br>
N_SPECIFIC_PROJECTS = 5 # número de projetos no edital específico - considera-se que todos recebem a mesma qtde de bolsas<br>
cotas = {"outros": 0.1, "não negro" : 0.2, "negro" : 0.7, "ampla": 0.0} # porcentagens. Não usar "-" entre as palavras na coluna Ação Afirmativa no csv de entrada<br>
python -m venv myenv<br>
source myenv/bin/activate<br>
pip install pandas<br>
python3 roundrobin.py <filename>.csv n1 n2<br>
exemplo: python3 roundrobin.py entrada.csv 50 320<br>
