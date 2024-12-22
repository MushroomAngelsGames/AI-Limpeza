import pandas as pd
import numpy as np  
import matplotlib.pyplot as plt


"""
Developer by Luiz Felipe da Silva Marian
RGA: 202021901036
Trabalho de Inteligencia Artificial para UFMT
=> Código responsavel pela Criação de Gráficos e Tabelas
"""

#Class que Controla os Gráficos e Tabelas.
class GeneratorDataWithPandas:

    #Inicializar Class
    def __init__(self) -> None:
        pass

    #Criar Grafico
    def CreateGrafic(self,baseOfDatas,rows):
        
        plt.figure(figsize = (12, 5 + len(rows)))
        bar_width = .15

        index1 = np.arange(len(rows)) 
        namesList = list(baseOfDatas.keys())

        count =0
        countName =0

        for ss in baseOfDatas:
              
                count+=1
                plt.barh(index1 - bar_width * count, 
                baseOfDatas[ss], 
                ec = "k", 
                alpha = .2 * count, 
                color = "royalblue", 
                height = bar_width,
                label = namesList[countName])
                countName+=1

                for i, v in enumerate(baseOfDatas[ss]):
                    plt.text(v, i - bar_width * count* 1.1 , str(v)) 
         

      
        plt.xlabel("Desempenho Médio (Custo Energético/Espaços Limpos)")
        plt.ylabel("Ambientes e Agentes")

        plt.yticks(index1 - bar_width, rows)
        plt.title("Desempenho Médio de Agentes em Ambientes Aleatórios")
      

        plt.legend()
        plt.show()
    
    #Criar Tabela
    def CreateTable(self,baseOfDatas,rows):
        genericDateFrame = pd.DataFrame(baseOfDatas,index=rows)
        fig, tableS = plt.subplots()
        fig.patch.set_visible(False)
        tableS.axis('off')
        tableS.axis('tight')
        tableS.table(cellText=genericDateFrame.values,colLabels=genericDateFrame.columns,rowLabels=rows,loc='center')

        plt.title("Desempenho Medio de Agentes em Ambientes Aleatórios")
        plt.text(0,-1,"O cálculo da Media = (Custo Energético/Espaços Limpos)")
        plt.show()

#Função para Criar Tabela da Simulação.
def SetNewTableBaseOfData(baseOfDatas,rows):
    generic = GeneratorDataWithPandas()
    generic.CreateTable(baseOfDatas,rows)

#Função para Criar Gráfico da Simulação
def SetNewGraficBaseOfData(baseOfDatas,rows):
    generic = GeneratorDataWithPandas()
    generic.CreateGrafic(baseOfDatas,rows)
