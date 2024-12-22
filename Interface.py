from PySimpleGUI import PySimpleGUI as sg
from Clear import StartSimulation

"""
Developer by Luiz Felipe da Silva Marian
RGA: 202021901036
Trabalho de Inteligencia Artificial para UFMT
=> Código responsavel pela Interface Grafica.
"""

#Class Controladora Geral da Interface
class UISimulationController:

    #Inicialização da Classe e das Variaveis.
    def __init__(self) -> None:
        self.GlobalNameEmpty = "Não Há Simulações Configuradas" 
        self.layoutWithSimulations = [self.GlobalNameEmpty]
        self.amountOfSimulations = {}
        self.SetDefineInit()
        self.CreateBasicInterface()
        self.amountEnv = 0
        self.amountSimule = 0
        self.amountSimuleAll = 0
        pass
    
    #Definir o Tema da Interface.
    def SetDefineInit(self):
        sg.theme('Reddit')

    #Criar os Menus da tela Inicial.
    def CreateBasicInterface(self):
       
        #Menu de para Adcionar Simulação.
        addFrameLoyout = [
            [sg.Text("Nova Simulação"),sg.Input(key='KeyEnvLeght',default_text="5",tooltip="Tamanho do Ambiente de Simulação",size=(3,1)),
            sg.Input(key='KeyAmountSimule',
                     default_text="100",
                     tooltip="Quantiade de Simulações",
                     size=(5,1)),
            sg.Button("Adcionar Simulação",
                      key="KeyButAddSimule"),
                      sg.Button("Remover",key="KeyRemove",visible=False,button_color="red")],
        ]

        #Menu informando dados básicos das simulações cadastradas.
        dataSimulation= [
            [sg.Text("Ambientes :",border_width=1,background_color='#d0d0d0'),sg.Text("",key="KeyTotalEnv"),
             sg.Text("Simulações por Agente :",border_width=1,background_color='#d0d0d0'),sg.Text("",key="KeyTotalSimule"),
             sg.Text("Total de Simulações :",border_width=1,background_color='#d0d0d0'),sg.Text("",key="KeyTotalSimuleAll"),
            ]
           
        ]
        
        #Menu de Lista com todas as Simulações cadastradas.
        addFrameList= [
            [sg.Frame('Dados dessa Simulação',dataSimulation,font='Any 10',border_width=2,visible=False,key="KeyFrameDataSimule")],
            [sg.Listbox(values=self.layoutWithSimulations,
                        size=(350,5),
                        key="KeyListWithSimulations",
                        background_color='#9FB8AD',
                        pad=(5,5),
                        font="italic",
                        enable_events=True,
                        tooltip="Lista com Todas as Simulações que serão executadas, para retida da Media"),]     
        ]

        #Layout Principal que será inicializado.
        layout = [
            [sg.Frame("Cadastro de Simulaçãoes",addFrameLoyout,font='Any 14'), sg.Button("INICIAR",size=(50,2),key="KeyStartSimulation",visible=False,button_color="green")],
            [sg.HorizontalSeparator(pad=None)],
            [sg.Frame('Simulações',addFrameList,font='Any 12',key="KeyFrameList")],
            [sg.HorizontalSeparator(pad=None)],
        ]

        return layout

    #Adcionar uma nova Simulação.
    def AddNewSimulation(self,envLeght,amountSimulation):

        #Verificar se é um numero válido
        def IsnotNumber(value):
            try:
                int(value)
            except ValueError:
                return True
            return False
      

        env = envLeght[0:3]
        amount = amountSimulation[0:3]

        if(len(env) == 0 or IsnotNumber(env) or IsnotNumber(amount)): return

        self.amountOfSimulations[env+"x"+env] = [int(env),int(amount)]

        return self.GetListWithSimulations()

    #Recuperar uma lista com as Simulações
    def GetListWithSimulations(self):
        self.amountEnv = len(self.amountOfSimulations)
        self.amountSimule = 0
        self.amountSimuleAll =0
        listTemp = []
        for ss in self.amountOfSimulations:
            self.amountSimule += (int)(self.amountOfSimulations[ss][1])
            self.amountSimuleAll += (int)(self.amountOfSimulations[ss][1])*3
            listTemp.append((ss," Simulações: " + str(self.amountOfSimulations[ss][1]) ))

        if(self.amountEnv == 0):
            listTemp.append(self.GlobalNameEmpty)
        return listTemp

    #Remove uma Simulação da Lista
    def RemoveSimulation(self,nameRemove): 
        self.amountOfSimulations.pop(nameRemove[0][0])

    #Atualizar dados basicos, Após a modificação da lista.
    def UpdateList(self,GlobalWindons):
        GlobalWindons["KeyEnvLeght"].update("")
        GlobalWindons["KeyTotalEnv"].update(self.amountEnv)
        GlobalWindons["KeyTotalSimuleAll"].update(self.amountSimuleAll)
        GlobalWindons["KeyTotalSimule"].update(self.amountSimule)
        GlobalWindons["KeyFrameDataSimule"].update(visible = True)

    #Inicializar Interface e App, Ficar Verificando interações do Usuário.
    def StartApp(self):
        GlobalWindons = sg.Window("Simulador de IA", self.CreateBasicInterface() ,size=(550,250))
        GlobalWindons.SetIcon()
        while True:
     
            events,values = GlobalWindons.read()              
            GlobalWindons["KeyRemove"].update(visible = False) 
            

            if(events == sg.WINDOW_CLOSED):
                break
            if events == "KeyButAddSimule":  
                GlobalWindons["KeyListWithSimulations"].update(self.AddNewSimulation(values['KeyEnvLeght'],values['KeyAmountSimule']))
                self.UpdateList(GlobalWindons)
            if events == "KeyListWithSimulations":
                GlobalWindons["KeyRemove"].update(visible = True if values["KeyListWithSimulations"][0] != self.GlobalNameEmpty else False) 
            if events == "KeyRemove":
                self.RemoveSimulation(values["KeyListWithSimulations"])
                GlobalWindons["KeyListWithSimulations"].update(self.GetListWithSimulations())
                self.UpdateList(GlobalWindons)
            if events == "KeyStartSimulation":
                GlobalLoad = UILoad()
                GlobalLoad.SetValuesMaxLoad(int(self.amountEnv),int(self.amountSimule))          
                showDate = UIShowData()
                values = GlobalLoad.StartLoad(self.amountOfSimulations)
                if(values != None):
                    showDate.StartApp(values) 
            GlobalWindons["KeyStartSimulation"].update(visible = True if len(self.amountOfSimulations)>0 else False) 

#Class Controladora da Janela Final, que Informa os resultados.
class UIShowData:

    #Inicializar Class
    def __init__(self) -> None:
        pass   
        
    #Criar Interface da Janela
    def CreateBasicInterface(self,valueMedias):
        
        listKeys = list(valueMedias.keys())
     
        frameButton =[
           [sg.Button("Gerar Tabela de Dados",size=(36,1),key="keyCreateTable")],
           [sg.HorizontalSeparator()],
           [sg.Button("Gerar Grafico",size=(36,1),key="keyCreateGrafic")],
        ] 

        addOutput = [
            [sg.Output(size=(500,10),key="KeyOutput")],
        ]

        def GetMediaAgent(valueMedia):
            return [[sg.Text("Media: "),sg.Text(str(valueMedia),font='bold')]]
      
        def GetMediaSun(value):
            sun = 0
            for ss in value:
                sun += ss
            return round(sun/len(value),2)


        addOutputCompare = [
            [sg.Frame('Agente Aleatório',GetMediaAgent(GetMediaSun(valueMedias[listKeys[0]])),font='Any 10'),
             sg.Frame('Agente Reflexivel',GetMediaAgent(GetMediaSun(valueMedias[listKeys[1]])),font='Any 10'),
             sg.Frame('Agente Otimizado',GetMediaAgent(GetMediaSun(valueMedias[listKeys[2]])),font='Any 10')],
        ]

        layout = [
            [sg.HorizontalSeparator(pad=None)],
            [sg.Frame('Dados da Simulação',addOutput,font='Any 12')],
            [sg.HorizontalSeparator(pad=None)],
            [sg.Frame('Comparação Entre os Agentes',addOutputCompare,font='Any 12',size=(400,90)), sg.Frame('Exportar Dados',frameButton,font='Any 12')],
            [sg.HorizontalSeparator(pad=None)],
        ]

        return layout

    #Execultar Janela e Ficar Verificando Interações. 
    def StartApp(self,valueOutput):
        GlobalWindons = sg.Window("Dados da Simulação", self.CreateBasicInterface(valueOutput[1].GetTableMedias()) ,size=(650,350),modal=True)
     
        for i in range(1):
                events,values = GlobalWindons.read(timeout=10)  
                print(valueOutput[0])

        while True:

            events,values = GlobalWindons.read(timeout=10)  
            if(events == sg.WINDOW_CLOSED):
                break
            if events == "keyCreateTable":
                valueOutput[1].SetCreateDataFrameTable()
            if events == "keyCreateGrafic":
                valueOutput[1].SetCreateDataFrameGrafic() 
         
            
        GlobalWindons.close()

#Class Controladora da Janela de Load.
class UILoad:

    #Inicializar Class.
    def __init__(self) -> None:

        self.loadEnvAmountNeedMax = 0
        self.loadEnvcurrectCount = 0

        self.loadSimulationAmountNeedMax = 0
        self.loadSimulationcurrectCount = 0

        pass     

    #Atribuir valores de Maximos, para as barras de Progresso. 
    def SetValuesMaxLoad(self,envMax,SimuleMax):
        self.loadEnvAmountNeedMax = envMax    
        self.loadSimulationAmountNeedMax = SimuleMax   

    #Criar Iterface.
    def GetLayout(self):

        frameButton =[
           [sg.Button("Simular",key="KeySimuleNow",size=(300,10))],
        ] 

        frameLoads =[
            [sg.Text('Simulando no Ambiente : '),sg.Text('',key="keyNameEnv")],[sg.ProgressBar(self.loadEnvAmountNeedMax, orientation='h', size=(300, 20), key='progressbarEnv')],
            [sg.HorizontalSeparator(pad=None)],
            [sg.Text('Criando Simulação : '),sg.Text('',key="keyNameSimlue")],[sg.ProgressBar(self.loadSimulationAmountNeedMax, orientation='h', size=(300, 20), key='progressbarSimule')],

        ]    

        return [
            [sg.Frame('Clique para Simular',frameButton,font='Any 10',size=(300,50))],
            [sg.Frame('Progresso da Simulação',frameLoads,font='Any 12',size=(300,150))],
            ]
       
    #Atualizar Barra de Progresso dos Ambientes.
    def SetUpdateLoadEnv(self,nameEnv):
        self.window["keyNameEnv"].update(nameEnv)
        self.loadEnvcurrectCount+=1
        self.EnvProgress_bar.UpdateBar(self.loadEnvcurrectCount)

    #Atualizar Barra de Progresso das Simulações.
    def SetUpdateLoadSimlue(self,nameSimule):
        self.window["keyNameSimlue"].update(nameSimule)
        self.loadSimulationcurrectCount +=1
        self.SimuleProgress_bar.UpdateBar(self.loadSimulationcurrectCount)

    #Execultar Janela e Ficar Verificando Interações.
    def StartLoad(self,amountOfSimulations):
            
        valueOutpute = None
        self.window = sg.Window('Simulando Agora, Espere!', self.GetLayout(), size=(300,200))
        self.EnvProgress_bar = self.window['progressbarEnv']
        self.SimuleProgress_bar = self.window['progressbarSimule']
       
        while (self.loadEnvcurrectCount < self.loadEnvAmountNeedMax) and (self.loadSimulationcurrectCount < self.loadSimulationAmountNeedMax):  
             events,values = self.window.read()       
             if(events == sg.WINDOW_CLOSED):
                break   
             if(events == "KeySimuleNow"):
                valueOutpute = StartSimulation(amountOfSimulations,self.SetUpdateLoadEnv,self.SetUpdateLoadSimlue)
             
        self.window.close() 
        return valueOutpute

#Criar e Chamar a Class Principal.      
App = UISimulationController()
App.StartApp()


            