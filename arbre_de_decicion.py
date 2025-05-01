from graphviz import Digraph

tree = Digraph(comment='Arbre de Décision - Paint Wars')
tree.attr(rankdir='TB')

tree.node('Start', 'Start')
tree.node('R0', 'robotId == 0 ?')
tree.node('R1', 'robotId == 1 ?')
tree.node('Wall', 'Obstacle détecté ?')
tree.node('Opti', 'Comportement optimisé')
tree.node('Rand', 'Exploration aléatoire')
tree.node('Avoid', 'Évitement mur')
tree.node('Mix', 'Mix exploration/évitement')

tree.edge('Start', 'R0')
tree.edge('R0', 'Opti', label='Oui')
tree.edge('R0', 'R1', label='Non')
tree.edge('R1', 'Rand', label='Oui')
tree.edge('R1', 'Wall', label='Non')
tree.edge('Wall', 'Avoid', label='Oui')
tree.edge('Wall', 'Mix', label='Non')

tree.render('decision_tree_paintwars', format='png', cleanup=True)
