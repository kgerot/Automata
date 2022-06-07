import format_print as fp
import manual_input

''' State Structure
  current State # : ( accepting ,  { symbol : next State # } )
'''

def theorem44(F, dfa, alphabet) -> bool:
  ''' 
    1. Mark the start state of A
    2. Repeat until no new states get marked
    3. Mark any state that has a transition coming into it from
      any state that is already marked
    4. If no accept state is marked, ACCEPT; otherwise REJECT
    #### parameters
    dfa, alphabet
    #### returns
    True or False (Accept/Reject)
  '''
  print('\n>=== Theorem 4.4 ===<')
  marked = {}
  start_state = list(dfa.items())[0]
  marked.update({start_state[0]: start_state[1][0]})  # mark start state
  
  mark_search(start_state[0], marked, dfa, alphabet)

  R = set(marked.keys())
  SF = set(F)
  F_intersect_R = set(SF).intersection(R)

  print('Reachable states ', fp.unicode['R'], ' = ', R, sep='')
  print('Accepting (final) states ', fp.unicode['F'], ' = ', \
        fp.unicode['empty'] if len(SF) == 0 else SF, sep='')
  print(fp.unicode['F'], fp.unicode['cap'], fp.unicode['R'], ' = ', \
        fp.unicode['empty'] if len(F_intersect_R)==0 else F_intersect_R, sep='')

  return len(F_intersect_R) == 0
      



def mark_search(state, marked, dfa, alphabet) -> None:
  '''
    #### parameters
    - state: current state
    - marked: currently marked states
    - dfa
    - alphabet
  '''
  for c in alphabet:
    trans_state = dfa[state][1][c]
    accepting = dfa[trans_state][0]
    if not trans_state in marked:
      marked.update({trans_state: accepting})
      mark_search(trans_state, marked, dfa, alphabet)


def standardize(name: str, M, alphabet, dfa):
  '''
    alters M to be proper form and prints that form
    if desired
    #### parameters
    - name: Name of the DFA
    - M: 
    - alphabet
    - dfa
  '''
  M.update({'Q':list(dfa.keys())}) # states
  M.update({'Sigma':list(alphabet)}) # alphabet
  M.update({'delta':dfa}) # transitions
  M.update({'q0':list(dfa.items())[0][0]}) # initial state
  F = []
  for state, info in dfa.items():
    if(info[0]): 
      F.append(state)
  M.update({'F':F}) # accepting states

  print( 'DFA', name, '= (' )

  fp.dfa_item(fp.unicode['Q'], M['Q'])
  fp.dfa_item(fp.unicode['Sigma'], M['Sigma'])
  fp.transitions(fp.unicode['delta'], M['delta'], alphabet)
  print('\t', fp.unicode['q0'], '= ', M['q0'], sep='')
  fp.dfa_item(fp.unicode['F'], M['F'])

  print(')')

  return M['Q'], M['Sigma'], M['delta'], M['q0'], M['F']

def xor(x, y) -> bool:
    return bool((x and not y) or (not x and y))

def read_file(file, eq = False):
  dfaA = {}
  alphabet = ''
  
  lines = file.read().splitlines()
  num_states = int(lines[0])
  alphabet_raw = lines[1]
  alphabet = ''.join(dict.fromkeys(alphabet_raw))

  for i in range(0, num_states):
    line = lines[2+i].split(' ')
    state = 'S' + str(i)
    transitions = {}        
    accepting = True if line[0] == 'y' else False
    j = 0
    for c in alphabet:
      val = 'S' + line[j+1]
      transitions.update({c:val})
      j+=1
    info = (accepting, transitions)
    dfaA.update({state: info})
  print(eq)
  if eq:
    dfaB = {}
    start = num_states+2
    print(lines[start])
    num_states = int(lines[start])
    alphabet_raw = lines[start+1]
    alphabetB = ''.join(dict.fromkeys(alphabet_raw))
  
    for i in range(start, num_states+start):
      line = lines[2+i].split(' ')
      state = 'S' + str(i)
      transitions = {}        
      accepting = True if line[0] == 'y' else False
      j = 0
      for c in alphabetB:
        val = 'S' + line[j+1]
        transitions.update({c:val})
        j+=1
      info = (accepting, transitions)
      dfaB.update({state: info})
    
    alphabet = ''.join(dict.fromkeys(alphabetB))
    return dfaA, dfaB, alphabet
  else:
    return dfaA, alphabet

def symmetric_difference(QA, dA, q0A, FA, QB, dB, q0B, FB, E):
  ''' 
    Symmetric Difference
    The Symmetric difference DFA C of DFAs A, B:
      L(C) = 
        L(A) intersect L'(B)
        union
        L'(A) intersect L(B)
    The complement of a DFA is acheived by taking the complement of
    the set of final states F.
    
    Thus the DFA C can be constructed as follows:
      Q     = Q_A X Q_B
      Sigma = Sigma_A union Sigma_B
      delta = <delta_A(q_A, a), delta_B(q_B, a)>
      q0    = <q0_A, q0_B>
      F     = <q_A, q_B>
          s.t. q_A in F_A XOR q_B in F_B
  '''
  dfa = {}
  for qa in QA:
    for qb in QB:
      state = qa + qb
      transitions = {}
      qaFA = qa in FA
      qbFB = qb in FB
      accepting = xor(qaFA, qbFB)
      for c in E:
        trans_A = dA[qa][1][c]
        trans_B = dB[qb][1][c]
        trans = trans_A + trans_B
        transitions.update({c:trans})
      info = (accepting, transitions)
      dfa.update({state: info})
  
  M = {}
  QC, EC, dC, q0C, FC = standardize('C', M, E, dfa)
  return dfa, FC

def test_emptiness(file = None) -> bool:
  dfa = {}
  alphabet = ''
  choice = None
  M= {}

  if file: choice = '2'
  while choice != '2':
    choice = input('Import DFA (0) or Manually Input DFA (1)? ')
    if(choice == '0' or choice == '1'):
      break
    else:
      print('Invalid input (must be 0 or 1)')
  if(choice == '0'):
    try: file = open(input('Filename: '))
    except FileNotFoundError:
      print('The file specified does not exist')
      quit()
    dfa, alphabet = read_file(file)
  if(choice == '1'):
    dfa, alphabet = manual_input.dfa()
  if(choice == '2'):
    try: file = open(file)
    except FileNotFoundError:
      print('The file specified does not exist')
      quit()
    dfa, alphabet = read_file(file)

  Q, E, d, q, F = standardize('M', M, alphabet, dfa)

  T_accept = theorem44(F, dfa, alphabet)
  print('ACCEPTED' if T_accept else 'REJECTED')
  print('\n>=== Result ===<')
  print('DFAs are', '' if T_accept else 'not', 'equivalent')
  return T_accept

def test_equivalence(file = None) -> bool:
  dfa_a = {}
  dfa_b = {}
  alphabet = ''
  choice = None
  M_a = {}
  M_b = {}

  if file: choice = '2'
  while choice != '2':
    choice = input('Import DFA (0) or Manually Input DFA (1)? ')
    if(choice == '0' or choice == '1'):
      break
    else:
      print('Invalid input (must be 0 or 1)')
  if(choice == '0'):
    try: file = open(input('Filename: '))
    except FileNotFoundError:
      print('The file specified does not exist')
      quit()
    dfa_a, dfa_b, alphabet = read_file(file, True)
  if(choice == '1'):
    print('DFA A')
    dfa_a, alphabet_a = manual_input.dfa()
    print('DFA B')
    dfa_b, alphabet_b = manual_input.dfa()
    alphabet = ''.join(dict.fromkeys((alphabet_a + alphabet_b)))
  if(choice == '2'):
    try: file = open(file)
    except FileNotFoundError:
      print('The file specified does not exist')
      quit()
    dfa_a, dfa_b, alphabet = read_file(file, True)

  Qa, Ea, da, qa, Fa = standardize('A', M_a, alphabet, dfa_a)
  Qb, Eb, db, qb, Fb = standardize('B', M_b, alphabet, dfa_b)

  print('\n>=== Constructed DFA C ===<')
  dfa_s, F = symmetric_difference(Qa, da, qa, Fa, Qb, db, qb, Fb, alphabet)

  T_accept = theorem44(F, dfa_s, alphabet)
  print('ACCEPTED' if T_accept else 'REJECTED')
  print('\n>=== Result ===<')
  print('DFA is', '' if T_accept else 'not', 'empty')
  

  return T_accept

''' Main
'''
if __name__ == '__main__':
  while True:
    choice = input('Test Emptiness (0) or Test Equivalence (1)? ')
    if(choice == '0' or choice == '1'):
      break
    else:
      print('Invalid input (must be 0 or 1)')
  if choice == '0':
    test_emptiness()
  else:
    test_equivalence()
