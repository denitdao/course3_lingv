class Stack:
     def __init__(self):
          self.items = []

     def isEmpty(self):
          return self.items == []

     def push(self, item):
          self.items.append(item)

     def pop(self):
          if not self.isEmpty():
               return self.items.pop()
          else:
               return False

     def print(self):
          sx = ""
          for x in self.items:
               sx += str(x) + '\t'
          print('STACK:[ {0} '.format(sx))
          return True
