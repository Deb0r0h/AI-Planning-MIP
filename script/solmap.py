# def action(i,j):
#     file = open("./miconic_sol/miconic-s" + str(i) + "-" + str(j) + ".sol", "r")
#     lines = file.read().splitlines()
#     numberOfActions = len(lines)-1
#     action = []
#     for i in range(numberOfActions):
#         action.append(lines[i])
#         action[i] = action[i].strip("()")
#     file.close()
#     return action

# class SolMap:
#     def __init__(self, i:int, j:int):
#         self.instance = []
#         file = open("./miconic_sol/miconic-s" + str(i) + "-" + str(j) + ".sol", "r")
#         lines = file.read().splitlines()
#         #numberOfActions = len(lines)-1
#         index = 0
#         index = self.actions(lines,index)
#         file.close()

#     def actions(self,lines:list,i:int):
#         numberOfActions = len(lines)-1
#         action = []
#         for k in range(numberOfActions):
#             action.append(lines[k])
#             action[k] = action[k].strip("()")
#         return i
      
#     def get_instance(self):
#         return self.instance

def actions(i,j):
    file = open("./miconic_sol/miconic-s" + str(i) + "-" + str(j) + ".sol", "r")
    lines = file.read().splitlines()
    numberOfActions = len(lines)-1
    action = []
    for i in range(numberOfActions):
        action.append(lines[i])
        action[i] = action[i].strip("()")
    file.close()
    return action





    
