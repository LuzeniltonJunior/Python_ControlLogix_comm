
#importando as bibliotecas
import csv
import time
from pylogix import PLC
from datetime import datetime

#local e nome do arquivo
output_directory = r"C:\\Users\\ALIEN\\Desktop\\SP_ANALISE"  # Altere para o caminho desejado
output_file = f"{output_directory}\\dataset.csv"

#base de tempo para a leitura
TEMPO = 0.5

#criando o arquivo CSV ja com os cabeçalhos
with open(output_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['D_MV_T0', 'D_MV_T1', 'D_MV_T2', 'D_MV_T3', 
                     'D_MV_ATUAL', 'D_PV_T0', 'D_PV_T1', 
                     'D_PV_T2', 'D_PV_T3', 'D_PV_ATUAL'])

#instanciando o nosso plc
plc = PLC()
plc.IPAddress = "192.168.0.100"
plc.ProcessorSlot = 1

#pegando o horário em que o script foi iniciado
start_time = datetime.now()

try:
    #loop
    while True:

        #tenta ler as 10 posições do vetor DATASET_VALUES[]
        dataset_values = []
        for i in range(10):  #vetor de 10 posições
            tag_name = f'DATASET_VALUES[{i}]'  #formato da tag
            value = plc.Read(tag_name)  #lê o valor da tag
            dataset_values.append(value.Value)  #adiciona o valor a lista

        #adicione os valores ao dataset
        with open(output_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(dataset_values)  #escreve os valores no arquivo

        #conta quantas entradas já foram escritas
        with open(output_file) as file:
            num_lines = sum(1 for line in file) - 1  #subtrai 1 pelo cabeçalho

        #imprime na tela
        formatted_values = [f'{value:.3f}' for value in dataset_values]
        print(f"Valores lidos: {formatted_values}")
        print(f"Total de entradas já escritas: {num_lines}")
        print(f"Script iniciado em: {start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        #aguarda um intervalo antes da próxima leitura
        time.sleep(TEMPO) 

except KeyboardInterrupt:
    print("Script interrompido.") #interrupção pelo teclado

finally:
    plc.Close()  #fechando a conexao
