import numpy as np
import TablesHelper as tb

"""
Developer by Luiz Felipe da Silva Marian
RGA: 202021901036
Trabalho de Inteligencia Artificial para UFMT
=> Código responsavel pela Simulação
"""

class Agent:
    def __init__(self,n=5) -> None:
        self.dimension = n;
        self.RestartAgent()
       
    def RestartAgent(self):
        position = np.random.randint(0,self.dimension,2)
        self.x = position[0]
        self.y = position[1]

    def Get_perception(self,environment):      
        north,south,west,east = True,True,True,True
        dimension = environment.shape[0]

        if self.x == 0:
            west = False
        if self.x == dimension-1:
            east = False
        if self.y == 0:
            north = False
        if self.y  == dimension-1:
            south = False

        perception = {
            "north":north,
            "south":south,
            "west":west,
            "east":east
        }

        dirty = environment[self.x][self.y]
        return perception,dirty

    def Get_ReflexiveAnget(self,environment):   
        actions = ["north", "east", "west", "south","suck"]
        perception, dirty = self.Get_perception(environment) 
        while True:
            if dirty == True:
                return "suck"
            action = np.random.choice(actions)
            if(action == "north") and (perception["north"]):
                return "north"
            if(action == "south") and (perception["south"]):
                return "south"
            if(action == "aest") and (perception["east"]):
                return "aest"
            if(action == "west") and (perception["west"]):
                return "west"    
            return action

    def Get_SimpleAgent(self):   
        actions = ["north", "east", "west", "south","suck"]
        action = np.random.choice(actions)
        return action

    def Get_OptimizeAgent(self,environment):   
        AllLocalsDirty = []
        coast = 0
        num_cleaned = 0

        for i in range(self.dimension):
            for j in range(self.dimension):
                if (environment[i][j] == True): 
                    AllLocalsDirty.append([i,j])
    
        for ss in AllLocalsDirty:
            # print("Local Sujo", ss)
            # print("PlayerPos ",self.x,"x",self.y)
            xDirection = self.x - ss[0]
            YDirection = self.y - ss[1]
            # print("X", xDirection)
            # print("Y", YDirection)

            for i in range(abs(xDirection)):
                if(xDirection > 0):
                    self.x -= 1
                else:
                    self.x += 1
                coast +=1  
            for i in range(abs(YDirection)):
                if(YDirection > 0):
                    self.y -= 1  
                else:
                    self.y += 1
                coast +=1  
            
            self.Suck(environment)
            num_cleaned = num_cleaned + 1
            coast+=1
            #print("PlayerPos ",self.x,"x",self.y)

        return num_cleaned,coast

    def Move(self,action,environment):
    
        perception, dirty = self.Get_perception(environment) 

        if(action == "north") and (perception["north"]):
            self.y -=1 
            return True
        if(action == "south") and (perception["south"]):
             self.y +=1 
             return True
        if(action == "east") and (perception["east"]):
             self.x +=1
             return True       
        if(action == "west") and (perception["west"]):
             self.x -=1
             return True
        else: 
            return False    

    def GetPosition(self):
        return self.x,self.y

    def Suck(self,environment):
        perception, dirty = self.Get_perception(environment) 
        if(dirty):
            environment[self.x][self.y] = False
            return True
        else:
            return False

class EnvSimulation:
    def __init__(self,Agent,dimension = 5,prob=0.2) -> None:
        self.n = dimension
        self.prob = prob
        self.agent = Agent
        self.environment = None
        self.agentPositionX = 0
        self.agentPositionY =0
   
    def get_total_DirtyPositions(self):
        return np.sum(self.environment)

    def Create_Enviroment(self):

        def convert_to_bololean(x,prob = 0.2):
            return True if x < prob else False

        self.environment = np.random.random((self.n,self.n))
        func_vectorized = np.vectorize(convert_to_bololean)
        self.environment = func_vectorized(self.environment,self.prob)
        return self.environment

    def RunSimulation(self,type):

        self.Create_Enviroment()

        coast = 0
        num_cleaned = 0
        while(self.get_total_DirtyPositions() != 0):   
            action = None 

            if (type == 0):
                action = self.agent.Get_SimpleAgent()
            elif (type == 1):
                action = self.agent.Get_ReflexiveAnget(self.environment)

            if (action == "suck"): 
                if (self.agent.Suck(self.environment)):
                    num_cleaned += 1
                    coast+=1
            else:
                if(self.agent.Move(action,self.environment)):
                    coast+=1
        
        return num_cleaned,coast

    def RunSimulationForOptimizedAgent(self):
        self.Create_Enviroment()
        return self.agent.Get_OptimizeAgent(self.environment)

class ControllerSimulations:
    def __init__(self,memorySimulation) -> None:
        self.memorySimulation = memorySimulation
        pass

    def StartNewSimulation(self,amountOfSimualtions,DefEnvMoreLoad,DefSimuleMoreLoad):
        labelWithAllConsole =""
        iCount = 0
        for ss in amountOfSimualtions:
            keysList = list(amountOfSimualtions.keys())
            NewMemory = Memory(keysList[iCount]) 
            agent = Agent(amountOfSimualtions[ss][0])
            simulation = EnvSimulation(agent, dimension= amountOfSimualtions[ss][0])
            DefEnvMoreLoad(str(ss))
            labelWithAllConsole += "\n|---------- | Novo Ambiente | ----------|\n\nTamanho da Matriz: " + str(ss) + "\n"

            labelWithAllConsole += "\n\n-------------------------------------------------------------------------------------------------------------------------------------------\n\n"
            labelWithAllConsole += "Simulando =>  Agente Aleatório... \n"
            for irandoRuns in range(amountOfSimualtions[ss][1]):
                DefSimuleMoreLoad(str(irandoRuns+1))      
                agent.RestartAgent()
                num_cleaned, coast = simulation.RunSimulation(0)
                NewMemory.MemoryRandorizedAngent.append([num_cleaned,coast])
                labelWithAllConsole += "\nAmbiente: " + str(ss) + " | Simulação : " + str(irandoRuns+1) + " | Locais Limpos: " + str(num_cleaned) + " | Custo : " + str(coast) + " | Média: " + str(round(coast/num_cleaned if num_cleaned>0 else 1,2))

            labelWithAllConsole += "\n\n-------------------------------------------------------------------------------------------------------------------------------------------\n\n"
            labelWithAllConsole += "Simulando =>  Agente Reflexivel...\n"
            for irandoRuns in range(amountOfSimualtions[ss][1]):      
                agent.RestartAgent()
                num_cleaned, coast = simulation.RunSimulation(1)
                NewMemory.MemoryReflexiveAngent.append([num_cleaned,coast])
                labelWithAllConsole += "\nAmbiente: " + str(ss) + " | Simulação : " + str(irandoRuns+1) + " | Locais Limpos: " + str(num_cleaned) + " | Custo : " + str(coast) + " | Média: " + str(round(coast/num_cleaned if num_cleaned>0 else 1,2))
       
            labelWithAllConsole += "\n\n-------------------------------------------------------------------------------------------------------------------------------------------\n\n"
            labelWithAllConsole += "Simulando =>  Agente Otimizado...\n"
            for irandoRuns in range(amountOfSimualtions[ss][1]):                 
                agent.RestartAgent()
                num_cleaned, coast = simulation.RunSimulationForOptimizedAgent()
                NewMemory.MemoryOptimezedAgent.append([num_cleaned,coast])
                labelWithAllConsole += "\nAmbiente: " + str(ss) + " | Simulação : " + str(irandoRuns+1) + " | Locais Limpos: " + str(num_cleaned) + " | Custo : " + str(coast) + " | Média: " + str(round(coast/num_cleaned if num_cleaned>0 else 1,2))


            iCount+=1
            self.memorySimulation.memoryAllList.append(NewMemory)
        return labelWithAllConsole
        #self.memorySimulation.SetCreateDataFrame()
        
class MemorySimulation:
    def __init__(self,settigs,amountOfSimulations) -> None:
        self.memoryAllList = []
        self.settigs = settigs
        self.amountOfSimulations = amountOfSimulations     
        pass

    def SetCreateDataFrameTable(self):
        index = []
        for ss in self.amountOfSimulations:
            index.append(ss)

        tb.SetNewTableBaseOfData(self.GetTableMedias(),index)

    def SetCreateDataFrameGrafic(self):
        index = []
        for ss in self.amountOfSimulations:
            index.append(ss)

        tb.SetNewGraficBaseOfData(self.GetTableMedias(),index)

    def GetTableMedias(self):
        HelpWiltColum = []  
        listKeys = list(self.settigs.keys())

        count = 0
        for ss in self.settigs:
            temtListWithValues = []
            for jj in self.memoryAllList:
                temtListWithValues.append(jj.GetDataWithName(self.settigs[listKeys[count]]))          
            count+=1
            HelpWiltColum.append(temtListWithValues)

        valueFinal = {}
        for count in range(len(self.settigs)):
            valueFinal[listKeys[count]] = HelpWiltColum[count]

        return valueFinal

class Memory:
    def __init__(self,nameThis) -> None:
        self.nameThis = nameThis
        self.MemoryRandorizedAngent = []
        self.MemoryReflexiveAngent = []
        self.MemoryOptimezedAgent = []
        pass

    def GetDataFrame(self):
        return {self.nameThis:[self.GetMedia(self.MemoryRandorizedAngent),self.GetMedia(self.MemoryReflexiveAngent),self.GetMedia(self.MemoryOptimezedAgent)]}

    def GetDataWithName(self,intValue):
        if(intValue == 0):
            return self.GetMedia(self.MemoryRandorizedAngent)
        elif (intValue == 1):
            return self.GetMedia(self.MemoryReflexiveAngent)
        elif (intValue == 2):
            return self.GetMedia(self.MemoryOptimezedAgent)

    def GetMedia(self,dataBase):
        amountNeededClear = 0
        coastAll = 0
        for ss in range(len(dataBase)):
            amountNeededClear += int(dataBase[ss][0])
            coastAll += int(dataBase[ss][1])

        return round(coastAll / (1 if (amountNeededClear == 0) else amountNeededClear),2)

#Função que Inicializar a Simulação.
def StartSimulation(amountOfSimulations,DefEnvMoreLoad,DefSimuleMoreLoad):
    settigs = {"Agente Aleatorio":0,"Agente Reflexivel":1 ,"Agente Otimizado":2}
    memorySimulation = MemorySimulation(settigs,amountOfSimulations)
    controller = ControllerSimulations(memorySimulation)
    return controller.StartNewSimulation(amountOfSimulations,DefEnvMoreLoad,DefSimuleMoreLoad),memorySimulation




