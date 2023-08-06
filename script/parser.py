class Parser:
  def __init__(self, i: int, j: int):
    self.instance = {}
    file = open("./miconic/miconic-s" + str(i) + "-" + str(j) + ".sas", "r")
    lines = file.read().splitlines()

    index = 0
    index = self.version(lines, index)
    index = self.metric(lines, index)
    index = self.variables(lines, index)
    index = self.mutex(lines, index)
    index = self.initial_state(lines, index)
    index = self.goal_state(lines, index)
    index = self.operators(lines, index)
    index = self.axiom_section(lines, index)
    file.close()

  def version(self, lines: list, i: int):
    if(lines[i] != "begin_version"):
      raise Exception("Invalid SAS format")
    i += 1
    self.instance["version"] = lines[i]
    return i+2

  def metric(self, lines: list, i: int):
    if(lines[i] != "begin_metric"):
      raise Exception("Invalid SAS format")
    i += 1
    if(lines[i] == "0"):
      self.instance["equalCost"] = True
    else:
      self.instance["equalCost"] = False
    return i+2

  def variables(self, lines: list, i: int):
    numberOfVariables = int(lines[i])
    i += 1
    self.instance["variables"] = []
    for j in range (numberOfVariables):
      if(lines[i] != "begin_variable"):
        raise Exception("Invalid SAS format")
      i += 1
      name = lines[i]
      i += 1
      if(lines[i] != "-1"):
        raise Exception("Axiom layers not equals to -1 are not supported")
      i += 1
      maxValue = int(lines[i]) - 1
      self.instance["variables"].append({
        "name": name,
        "maxValue": maxValue
      })
      # ignoring range PDDL names
      while(lines[i] != "end_variable"):
        i += 1
      i += 1
    return i

  def mutex(self, lines: list, i: int):
    numberOfMutex = int(lines[i])
    i += 1
    for j in range (numberOfMutex):
      # mutex not implemented yet
      while(lines[i] != "end_mutex_group"):
        i += 1
      i += 1
    return i

  def initial_state(self, lines: list, i: int):
    if(lines[i] != "begin_state"):
      raise Exception("Invalid SAS format")
    i += 1
    for variable in self.instance["variables"]:
      variable["initialValue"] = int(lines[i])
      i += 1
    i += 1
    return i

  def goal_state(self, lines: list, i: int):
    if(lines[i] != "begin_goal"):
      raise Exception("Invalid SAS format")
    i += 1
    goalNumbers = int(lines[i])
    i += 1
    self.instance["goals"] = {}
    for j in range (goalNumbers):
      values = lines[i].split()
      self.instance["goals"]["var"+values[0]] = int(values[1])
      i += 1
    i += 1
    return i
      
  def operators(self, lines: list, i: int):
    numberOfOperators = int(lines[i])
    i += 1
    self.instance["operators"] = []
    for j in range (numberOfOperators):
      operator = {
        "name": "",
        "preconditions": {},
        "effects": {},
        "cost": 0
      }
      if(lines[i] != "begin_operator"):
        raise Exception("Invalid SAS format")
      i += 1
      operator["name"] = lines[i]
      i += 1
      numberOfPrevails = int(lines[i])
      i += 1
      for k in range (numberOfPrevails):
        values = lines[i].split()
        operator["preconditions"]["var"+values[0]] = int(values[1])
        operator["effects"]["var"+values[0]] = int(values[1])
        i += 1
      numberOfEffects = int(lines[i])
      i += 1
      for k in range (numberOfEffects):
        values = lines[i].split()
        if(values[0] != "0"):
          raise Exception("Only 0 effect conditions is supported")
        operator["preconditions"]["var"+values[1]] = int(values[2])
        operator["effects"]["var"+values[1]] = int(values[3])
        i += 1
      operator["cost"] = 1 if self.instance["equalCost"] else int(lines[i])
      i += 2
      self.instance["operators"].append(operator)
    
    return i

  def axiom_section(self, lines: list, i: int):
    if(lines[i] != "0"):
      raise Exception("Axiom section different from 0 not supported")
    return i + 1
  
  def get_instance(self):
    return self.instance