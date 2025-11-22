# RoundRobinPIBEX
Sistema de Distribuição de Bolsas: realiza a distribuição de bolsas com base nas regras dos editais PIBEX/UEFS de 2025, garantindo as bolsas reservadas para ações afirmativas, considerando o limite de bolsas por orientador e por projeto.

📥 Input Format
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

🧠 How the Algorithm Works
The selection occurs in rounds:

1st Round
One candidate per CONSEPE (unless it is a specific call — projects with a predefined number of scholarships)
Any type (Programa/Projeto)
Must satisfy advisor/project limits

2nd Round
One per CONSEPE (unless it is a specific call — projects with a predefined number of scholarships)
Only candidates from Programa
Same global constraints

from the 3rd Round on
according to score (ranking) (unless it is a specific call — projects with a predefined number of scholarships)
Same global constraints

The algorithm enforces:
Max 4 scholarships per Projeto, or 6 for Programa
Max 6 scholarships per advisor
No duplicate students

No reuse of a CONSEPE within the same round

After the selection, non-selected candidates default to:
Cadastro Reserva
Aprovado
Não Aprovado

python -m venv myenv
source myenv/bin/activate
pip install pandas
python3 roundrobin.py <nome do arquivo>.csv n1 n2
exemplo: python3 roundrobin.py entrada.csv 50 320
