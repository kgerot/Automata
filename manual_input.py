''' Manual DFA
manually input dfa 
'''
def dfa():
  num_states = 0
  dfa = {}

  while True:
    try:
      num_states = int(input('How many states? '))
      break
    except ValueError:
      print('Invalid Input (not a number)')

  alphabet_raw = input('What is your alphabet? Type all the symbols in a string: ')

  # removes duplicate symbols
  alphabet = ''.join(dict.fromkeys(alphabet_raw))

  for i in range(0, num_states):
    state = 'S' + str(i)
    transitions = {}
    accepting = False

    print('')
    if (i == 0):
      print('\tState 0 (start state) :')
    else:
      print('\tState', i, ':')
    
    while True:
      raw = input("\t\t\tIs this state accepting? (y/n): ")

      if (raw == 'y' or raw == 'n'):
        accepting = True if raw == 'y' else False
        break
      else:
        print('\t\t\tInvalid input (must be y or n)')

    print('\t\t=> Transitions <=')

    for c in alphabet:
      while True:
        try:
          print(
            '\t\t\t State ( 0 -',
            num_states - 1, 
            ') transitioned to over',
            c,
            '?'
          )
          val = int(input('\t\t\t > '))
          if (val in range(0, num_states)):
            break
          else:
            print('\t\t\tInvalid Input, choose a number within the given range')
        except ValueError:
          print('\t\t\tInvalid Input (not a number)')

      val_altered = 'S' + str(val)
      transitions.update({c: val_altered})

    info = (accepting, transitions)
    dfa.update({state: info})
  return dfa, alphabet