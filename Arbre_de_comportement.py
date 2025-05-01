
from graphviz import Digraph

dot = Digraph(comment='Architecture de Comportements - Subsomption')
dot.attr(rankdir='TB')

# Niveaux
dot.node('A', 'Comportement Exploratoire (random_walker)')
dot.node('B', 'Évitement de murs (hate_wall)', style='filled', fillcolor='lightblue')
dot.node('C', 'Poids optimisés (genetic)', style='filled', fillcolor='lightgreen')

# Priorités
dot.node('P', 'Subsomption: Priorités', shape='diamond')

dot.edge('A', 'P', label='base')
dot.edge('B', 'P', label='si obstacle')
dot.edge('C', 'P', label='si robot 0')

dot.node('R', 'Commandes moteur', shape='box')
dot.edge('P', 'R')

# Exporter
dot.render('subsumption_behavior_tree', format='png', cleanup=True)
