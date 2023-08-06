from termios import TIOCPKT_DOSTOP
from parser import Parser
from re import U
import sys
from pyomo.environ import *
import pyomo.environ as pyo
from time import time
import pprint


from solmap import*
#from solmap import SolMap

# Creating state variables
def variables(model):
  vars = []
  for variable in model.parser["variables"]:
    vars.append(variable["name"])
  return vars

# Creating action domain
def actions_def(model):
  operators = []
  for action in model.parser["operators"]:
    operators.append(action["name"])
  return operators

# Creating y domains
def y_domains(model):
  domain = []
  for var in model.stateVars:
    for val1 in model.map_domains[var]:
      for val2 in model.map_domains[var]:
        domain.append((var, val1, val2))
  return domain

# Creating domain for initial state constraints
def initial_state_domain(model):
  domain = []
  for var in model.stateVars:
    for val in model.map_domains[var]:
      domain.append((var, val))
  return domain

# Adding costs parameters
def actions_costs(model, actionName):
  for action in model.parser["operators"]:
    if(action["name"] == actionName):
      return action["cost"]
  return -1

# Defining objective function
def obj_func(model):
  return sum(model.costs[j] * sum(model.z[j,i] for i in model.time) for j in model.actions)

# Initial y values
def initial_state(model, varName, val1):
  initialValue = 0
  for variable in model.parser["variables"]:
    if variable["name"] == varName:
      initialValue = variable["initialValue"]
  if(val1 == initialValue):
    return sum(model.y[varName, val1, j, 1] for j in model.map_domains[varName]) == 1
  else:
    return sum(model.y[varName, val1, j, 1] for j in model.map_domains[varName]) == 0

# Defining goal state
def goal_state(model, varName):
  if varName in model.parser["goals"]:
    goal = model.parser["goals"][varName]
    return sum(model.y[varName, j, goal, model.T] for j in model.map_domains[varName]) == 1
  return Constraint.Skip

# Defining arcs consistency
def arcs(model, varName, val1, val2, time):
  if(time == 1):
    return Constraint.Skip
  return (
    sum(model.y[varName, j, val1, time-1] for j in model.map_domains[varName]) == sum(model.y[varName, val1, i, time] for i in model.map_domains[varName])
  )

# Defining state changes effects
def state_changes(model, varName, val1, val2, time):
  if(val1 == val2):
    return Constraint.Skip
  suitable_actions = []
  for action in model.parser["operators"]:
    if varName in action["preconditions"]:
      if action["preconditions"][varName] == val1 and action["effects"][varName] == val2:
        suitable_actions.append(action["name"])
  return (model.y[varName, val1, val2, time] == sum(model.z[j, time] for j in suitable_actions))

# Defining prevails constraint
def state_prevails(model, varName, val1, val2, actionName, time):
  if(val1 != val2):
    return Constraint.Skip
  for action in model.parser["operators"]:
    if action["name"] == actionName:
      if(varName in action["preconditions"] and action["preconditions"][varName] == val1 and action["effects"][varName] == val1):
        return model.y[varName, val1, val1, time] >= model.z[actionName, time]
      else:
        return Constraint.Skip


#Stub function, get good operators from file sol
def getSolOperators(model,i,j):
  goodOperators = actions(i,j)
  return goodOperators

def getV(model,time):
  state = {}
  value = []
  for tempo in time:
    for var in model:
      value.append(var)
    state[tempo] = value
    value.clear()
      
  return state

def setValue(dizionario,index,valore):
  dizionario[list(dizionario.keys())[index]] = valore

def getValue(dizionario,index):
  return dizionario[list(dizionario.keys())[index]]

def getKey(dizionario):
  return list(dizionario.keys())





  
    

def buildModel(parser: Parser, maxTime: int,action_sol:list):
  map_domains = {}
  instance = parser.get_instance()
  # Creating custom set of data for indexes
  for variable in instance["variables"]:
    map_domains[variable["name"]] = list(range(0, variable["maxValue"] + 1))
  
  undefined_vars = {}
  for i in range(len(instance["operators"])):
    action = instance["operators"][i]
    baseName = action["name"]
    for entry in action["preconditions"]:
      if action["preconditions"][entry] == -1:
        if not(action["name"] in undefined_vars):
          undefined_vars[action["name"]] = []
        undefined_vars[action["name"]].append(entry)
  
  for action in undefined_vars:
    for var in undefined_vars[action]:
      for domain_value in map_domains[var]:
        for originalAction in instance["operators"]:
          if (action in originalAction["name"]) and (var in originalAction["preconditions"]) and originalAction["preconditions"][var] == -1:
            actionCopy = originalAction.copy()
            preconditions = actionCopy["preconditions"].copy()
            preconditions[var] = domain_value
            actionName = "{}_{}_{}".format(actionCopy["name"], var, domain_value)
            actionCopy["name"] = actionName
            actionCopy["preconditions"] = preconditions
            instance["operators"].append(actionCopy)
            
  
  for i in reversed(range(len(instance["operators"]))):
    for var in instance["operators"][i]["preconditions"]:
      if instance["operators"][i]["preconditions"][var] == -1:
        del instance["operators"][i]
        break


 
 
 
  
  # SIMULO PROCESSO SAPENDO SOL DAL PLANNER E RICAVO VALORE VARIABILI PER OGNI AZIONE, POI MAPPO SOLUZIONI SOL IN MA
  variabili = instance["variables"].copy()
  azioni = instance["operators"].copy()
  
  tempo = []
  for step in range(maxTime):
    step = step + 1
    tempo.append(step)

  valore_attuale = {}
  for i in range(len(variabili)):
    valore_attuale[variabili[i]['name']] = variabili[i]['initialValue']

  status = 0
  for t in tempo:
    for azione in azioni:
      if action_sol[t-1] in azione['name']:
        precondizione = azione['preconditions']
        effetto = azione['effects']
        lista_chiavi = getKey(precondizione)
        for k in lista_chiavi:
          if precondizione[k] == valore_attuale[k]:
            valore_attuale[k] = effetto[k]
            status = 1
          else:
            status = 0
        if status == 1:
          action_sol[t-1] = azione['name']
  


  model = ConcreteModel()
  model.parser = instance
  model.map_domains = map_domains
  model.T = maxTime
  # Sets
  model.time = RangeSet(model.T) # time set
  model.stateVars = Set(initialize=variables)
  model.actions = Set(initialize=actions_def)
  model.Y = Set(initialize=y_domains)
  model.varVal = Set(initialize=initial_state_domain)
  # Variables
  model.y = Var(model.Y, model.time, domain=Binary)
  model.z = Var(model.actions, model.time, domain=Binary, initialize=0)
  # Params
  model.costs = Param(model.actions,initialize=actions_costs,domain=NonNegativeIntegers)
  # Constraints
  model.initial_state = Constraint(model.varVal, rule=initial_state)
  model.goal_state = Constraint(model.stateVars, rule=goal_state)
  model.arcs = Constraint(model.Y, model.time, rule=arcs)
  model.effects = Constraint(model.Y, model.time, rule=state_changes)
  model.prevails = Constraint(model.Y, model.actions, model.time, rule=state_prevails)
  # Objective
  model.obj = Objective(rule=obj_func, sense=minimize)

  return model



def write_to_file(model, i:int, j:int, timeSpent):
  solution = {}
  for k in range(1, maxTime+1):
    solution[k] = []
  for action in model.z:
    actionName, time = action
    val = value(model.z[action])
    if(val > 0.5):
      solution[time].append(actionName)
  file = open("./results_MA/miconic-s{}-{}.txt".format(i, j), "w")
  count = 0
  for time in sorted(solution.keys()):
    actions = solution[time]
    for action in actions:
      file.write(action + ", ")
      if not("forget" in action):
          count += 1
    if len(actions) > 0:
      file.write("\n")
  file.write("Total of {} steps required\n".format(count))
  file.write("{} seconds elapsed".format(timeSpent))
  file.close()

def get_max_time(i:int, j:int):
  correctLog = open("./miconic_logs/miconic-s{}-{}.sas_0.log".format(i, j), "r")
  correctLines = correctLog.readlines()
  correctSteps = 0
  for line in correctLines:
    if line.count("Plan length"):
      arr = line.split(" ")
      index = arr.index("step(s).\n")
      correctSteps = arr[index-1]
  return int(correctSteps)


# Main based on best solution by fastforward
if __name__ == "__main__":
  print("Starting solver with MA method")
  i = sys.argv[1]
  j = sys.argv[2]
  maxTime = get_max_time(i, j)
  

  # list with solution
  azioni = actions(i,j)
  

  print("Starting solver for file {},{} with max time = {}".format(i, j, maxTime))
  print()
  print("creo modello")
  model = buildModel(Parser(i, j), maxTime,azioni)
  print("modello creato")
  print()
 

  
  tupla_action = 0
  tupla_time = 1
  for step in model.time:
    bestAction = azioni[step-1]
    for azione in model.z:
      if azione[tupla_time] == step and bestAction == azione[tupla_action]:
        model.z[azione] = 1
        
  opt = SolverFactory("cplex_persistent")
  opt.set_instance(model)

  opt.options['timelimit'] = 600

  startTime = time()
  result = opt.solve(warmstart=True,tee=True, logfile="./ma_cplex_logs/miconic-s{}-{}_cplex.log".format(i, j))
  #if(result.solver.status == SolverStatus.ok):
  endTime = time()
  write_to_file(model, i, j, endTime-startTime)
  print("Solved instance file {},{} with time limit of {} in {} seconds".format(i, j, maxTime, (endTime - startTime)))
  #if(result.solver.status != SolverStatus.ok):
    #print("Cannot solve problem {},{} with time limit of {}".format(i, j, maxTime))

