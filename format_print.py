unicode = { 'Q' : '\U0001D4AC', 'Sigma' : '\u2211', 'delta' : '\u03b4', 'q0' : 'q\u2080', 'F' : '\U0001D439', 'R' : '\U0001D445', 'cap' : '\u2229', 'empty' : '\u2205'}

''' Print Formatted Transitions
formats delta
'''
def transitions(label, delta, alphabet):
  # delta = {state:(accepting,{symbol:state_to})}

  if(len(list(delta.keys())[0]) == 2):
    print('\t', label, ' =\t   |', sep='', end='')
    for c in alphabet:
      print('| ', c, end=' ')
    
    print('|\n', end='\t\t====')
    for c in alphabet:
      print('=====', end='')

    print('=')
    for state, info in delta.items():
      print('\t\t', state, sep='', end=' |')
      for symbol in info[1]:
        print('|', info[1][symbol], end=' ')
      print('|')
  if(len(list(delta.keys())[0]) == 4):
    print('\t', label, ' =\t\t |', sep='', end='')
    for c in alphabet:
      print('|  ', c, end='  ')
    
    print('|\n', end='\t\t======')
    for c in alphabet:
      print('=======', end='')

    print('=')
    for state, info in delta.items():
      print('\t\t', state, sep='', end=' |')
      for symbol in info[1]:
        print('|', info[1][symbol], end=' ')
      print('|')
    

''' Print Formatted
formats lists
'''
def dfa_item(label, items):
  if len(items) == 0:
    print('\t', label, ' = ', unicode['empty'], sep='')
  else:
    print('\t', label, ' = {', sep='', end='')
    for i in range(0,len(items)):
      if(i < len(items)-1):
        print(items[i], end=', ')
      else:
        print(items[i], '}', sep='')