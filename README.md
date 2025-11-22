# RoundRobinPIBEX
Sistema de Distribuição de Bolsas: realiza a distribuição de bolsas com base nas regras dos editais PIBEX/UEFS de 2025, garantindo as bolsas reservadas para ações afirmativas, considerando o limite de bolsas por orientador e por projeto.

Input Format
The program expects a CSV with at least the following columns:

Column	Description
Matricula Discente	Student ID
Nota Final do pedido de bolsa	Final score (float or string with comma decimal)
Ação Afirmativa	Type of affirmative action or "Ampla Concorrência"
CONSEPE	Project identifier
Tipo	"Programa" or "Projeto"
Orientador do Plano de Trabalho	Advisor name
Eliminado do processo?	Mark if eliminated
Resultado	Will be filled by the program

Must have two separate calls for scholarship. Specific call must be named including substring "espec"

How the Algorithm Works
The selection occurs in rounds:

1st Round
One candidate per CONSEPE
Any type (Programa/Projeto)
Must satisfy advisor/project limits

2nd Round
One per CONSEPE
Only candidates from Programa
Same global constraints

from the 3rd Round on
according to score (ranking)
Same global constraints

The algorithm enforces:
One scholarship per project/program in each round (unless it is a specific call — projects with a predefined number of scholarships)
Max 4 scholarships per Projeto, or 6 for Programa
Max 6 scholarships per advisor
No duplicate students

After the selection, non-selected candidates default to: Cadastro Reserva, Aprovado or Não Aprovado

python -m venv myenv
source myenv/bin/activate
pip install pandas
python3 roundrobin.py <filename>.csv n1 n2
exemplo: python3 roundrobin.py entrada.csv 50 320
