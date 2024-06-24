# -*- coding: utf-8 -*-
"""
Created on Fri Jun 21 17:55:45 2024

@author: gh00616
"""

from pyomo.environ import ConcreteModel, Param, Var, Constraint, Objective, minimize, maximize
from pyomo.opt import SolverFactory

m = ConcreteModel()

m.name = 'Example: Alkylation process'

# Variables
m.x = Var(range(10), initialize=0.)
m.x[0].setlb(0)
m.x[0].setub(2000)
m.x[1].setlb(0)
m.x[1].setub(16000)
m.x[2].setlb(0)
m.x[2].setub(12)
m.x[3].setlb(0)
m.x[3].setub(5000)
m.x[4].setlb(0)
m.x[4].setub(2000)
m.x[5].setlb(85)
m.x[5].setub(93)
m.x[6].setlb(90)
m.x[6].setub(95)
m.x[7].setlb(3)
m.x[7].setub(12)
m.x[8].setlb(1.2)
m.x[8].setub(4)
m.x[9].setlb(145)
m.x[9].setub(162)

# Constraints
m.c1 = Constraint(expr = m.x[3] == m.x[0] * (1.12 + (0.12167*m.x[7]) -(0.0067 * (m.x[7]**2))))
m.c2 = Constraint(expr = m.x[6] == 86.35 + (1.098 * m.x[7]) - (0.038 * (m.x[7]**2)) + (0.325 * (m.x[5] - 89)))
m.c3 = Constraint(expr = m.x[8] == 35.28 - (0.222 * m.x[9]))
m.c4 = Constraint(expr = m.x[9] == (3 * m.x[6]) - 133)
m.c5 = Constraint(expr = m.x[7] * m.x[0] == m.x[1] + m.x[4])
m.c6 = Constraint(expr = m.x[4] == (1.22 * m.x[3]) - m.x[0])
m.c7 = Constraint(expr = m.x[5] * ((m.x[3] * m.x[8]) + (1000 * m.x[2])) == 98000 * m.x[2])


# Objective
m.obj = Objective(expr = (-1) * ((0.063 * m.x[3] * m.x[6]) - (5.04 * m.x[0]) - (0.035 * m.x[1]) - (10 * m.x[2]) - (3.36 * m.x[4])), sense=minimize)

# Solver configuration
#solver = SolverFactory('ipopt') 
solver = SolverFactory('gams') # using suitable solver from GAMS
result = solver.solve(m, tee = True)

print(f'Optimal Profit: {(0.063 * m.x[3].value * m.x[6].value) - (5.04 * m.x[0].value) - (0.035 * m.x[1].value) - (10 * m.x[2].value) - (3.36 * m.x[4].value)}')
print(f'Olefin feed, x1: {m.x[0].value}')
print(f'Fresh Acid feed, x3: {m.x[2].value}')
print(f'Isobutane feed, x5: {m.x[4].value}')
print(f'Alkylate field yield, x4: {m.x[3].value}')
print(f'External isobutane to olefin ratio, x8: {m.x[7].value}')
print(f'Motor octane number of the alkylate, x7: {m.x[6].value}')
print(f'Acid strength, x6: {m.x[5].value}')
print(f'Acid dilution factor, x9: {m.x[8].value}')
print(f'F-4 performance number, x10: {m.x[9].value}')