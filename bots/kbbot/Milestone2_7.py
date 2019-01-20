import sys
from kb import KB, Boolean, Integer, Constant

# Define our propositional symbols
# J1 is true if the card with index 1 is a jack, etc
# You need to initialise all variables that you need for you strategies and game knowledge.
# Add those variables here.. The following list is complete for the Play Jack strategy.
J0 = Boolean('j0')
J1 = Boolean('j1')
J2 = Boolean('j2')
J3 = Boolean('j3')
J4 = Boolean('j4')
J5 = Boolean('j5')
J6 = Boolean('j6')
J7 = Boolean('j7')
J8 = Boolean('j8')
J9 = Boolean('j9')
J10 = Boolean('j10')
J11 = Boolean('j11')
J12 = Boolean('j12')
J13 = Boolean('j13')
J14 = Boolean('j14')
J15 = Boolean('j15')
J16 = Boolean('j16')
J17 = Boolean('j17')
J18 = Boolean('j18')
J19 = Boolean('j19')
PJ0 = Boolean('pj0')
PJ1 = Boolean('pj1')
PJ2 = Boolean('pj2')
PJ3 = Boolean('pj3')
PJ4 = Boolean('pj4')
PJ5 = Boolean('pj5')
PJ6 = Boolean('pj6')
PJ7 = Boolean('pj7')
PJ8 = Boolean('pj8')
PJ9 = Boolean('pj9')
PJ10 = Boolean('pj10')
PJ11 = Boolean('pj11')
PJ12 = Boolean('pj12')
PJ13 = Boolean('pj13')
PJ14 = Boolean('pj14')
PJ15 = Boolean('pj15')
PJ16 = Boolean('pj16')
PJ17 = Boolean('pj17')
PJ18 = Boolean('pj18')
PJ19 = Boolean('pj19')

A0 = Boolean('a0')
A1 = Boolean('a1')
A2 = Boolean('a2')
A3 = Boolean('a3')
A4 = Boolean('a4')
A5 = Boolean('a5')
A6 = Boolean('a6')
A7 = Boolean('a7')
A8 = Boolean('a8')
A9 = Boolean('a9')
A10 = Boolean('a10')
A11 = Boolean('a11')
A12 = Boolean('a12')
A13 = Boolean('a13')
A14 = Boolean('a14')
A15 = Boolean('a15')
A16 = Boolean('a16')
A17 = Boolean('a17')
A18 = Boolean('a18')
A19 = Boolean('a19')
PA0 = Boolean('pa0')
PA1 = Boolean('pa1')
PA2 = Boolean('pa2')
PA3 = Boolean('pa3')
PA4 = Boolean('pa4')
PA5 = Boolean('pa5')
PA6 = Boolean('pa6')
PA7 = Boolean('pa7')
PA8 = Boolean('pa8')
PA9 = Boolean('pa9')
PA10 = Boolean('pa10')
PA11 = Boolean('pa11')
PA12 = Boolean('pa12')
PA13 = Boolean('pa13')
PA14 = Boolean('pa14')
PA15 = Boolean('pa15')
PA16 = Boolean('pa16')
PA17 = Boolean('pa17')
PA18 = Boolean('pa18')
PA19 = Boolean('pa19')

K0 = Boolean('k0')
K1 = Boolean('k1')
K2 = Boolean('k2')
K3 = Boolean('k3')
K4 = Boolean('k4')
K5 = Boolean('k5')
K6 = Boolean('k6')
K7 = Boolean('k7')
K8 = Boolean('k8')
K9 = Boolean('k9')
K10 = Boolean('k10')
K11 = Boolean('k11')
K12 = Boolean('k12')
K13 = Boolean('k13')
K14 = Boolean('k14')
K15 = Boolean('k15')
K16 = Boolean('k16')
K17 = Boolean('k17')
K18 = Boolean('k18')
K19 = Boolean('k19')
PK0 = Boolean('pk0')
PK1 = Boolean('pk1')
PK2 = Boolean('pk2')
PK3 = Boolean('pk3')
PK4 = Boolean('pk4')
PK5 = Boolean('pk5')
PK6 = Boolean('pk6')
PK7 = Boolean('pk7')
PK8 = Boolean('pk8')
PK9 = Boolean('pk9')
PK10 = Boolean('pk10')
PK11 = Boolean('pk11')
PK12 = Boolean('pk12')
PK13 = Boolean('pk13')
PK14 = Boolean('pk14')
PK15 = Boolean('pk15')
PK16 = Boolean('pk16')
PK17 = Boolean('pk17')
PK18 = Boolean('pk18')
PK19 = Boolean('pk19')

Q0 = Boolean('q0')
Q1 = Boolean('q1')
Q2 = Boolean('q2')
Q3 = Boolean('q3')
Q4 = Boolean('q4')
Q5 = Boolean('q5')
Q6 = Boolean('q6')
Q7 = Boolean('q7')
Q8 = Boolean('q8')
Q9 = Boolean('q9')
Q10 = Boolean('q10')
Q11 = Boolean('q11')
Q12 = Boolean('q12')
Q13 = Boolean('q13')
Q14 = Boolean('q14')
Q15 = Boolean('q15')
Q16 = Boolean('q16')
Q17 = Boolean('q17')
Q18 = Boolean('q18')
Q19 = Boolean('q19')
PQ0 = Boolean('pq0')
PQ1 = Boolean('pq1')
PQ2 = Boolean('pq2')
PQ3 = Boolean('pq3')
PQ4 = Boolean('pq4')
PQ5 = Boolean('pq5')
PQ6 = Boolean('pq6')
PQ7 = Boolean('pq7')
PQ8 = Boolean('pq8')
PQ9 = Boolean('pq9')
PQ10 = Boolean('pq10')
PQ11 = Boolean('pq11')
PQ12 = Boolean('pq12')
PQ13 = Boolean('pq13')
PQ14 = Boolean('pq14')
PQ15 = Boolean('pq15')
PQ16 = Boolean('pq16')
PQ17 = Boolean('pq17')
PQ18 = Boolean('pq18')
PQ19 = Boolean('pq19')

T0 = Boolean('t0')
T1 = Boolean('t1')
T2 = Boolean('t2')
T3 = Boolean('t3')
T4 = Boolean('t4')
T5 = Boolean('t5')
T6 = Boolean('t6')
T7 = Boolean('t7')
T8 = Boolean('t8')
T9 = Boolean('t9')
T10 = Boolean('t10')
T11 = Boolean('t11')
T12 = Boolean('t12')
T13 = Boolean('t13')
T14 = Boolean('t14')
T15 = Boolean('t15')
T16 = Boolean('t16')
T17 = Boolean('t17')
T18 = Boolean('t18')
T19 = Boolean('t19')
PT0 = Boolean('pt0')
PT1 = Boolean('pt1')
PT2 = Boolean('pt2')
PT3 = Boolean('pt3')
PT4 = Boolean('pt4')
PT5 = Boolean('pt5')
PT6 = Boolean('pt6')
PT7 = Boolean('pt7')
PT8 = Boolean('pt8')
PT9 = Boolean('pt9')
PT10 = Boolean('pt10')
PT11 = Boolean('pt11')
PT12 = Boolean('pt12')
PT13 = Boolean('pt13')
PT14 = Boolean('pt14')
PT15 = Boolean('pt15')
PT16 = Boolean('pt16')
PT17 = Boolean('pt17')
PT18 = Boolean('pt18')
PT19 = Boolean('pt19')

# Create a new knowledge base
kb = KB()

# GENERAL INFORMATION ABOUT THE CARDS
# This adds information which cards are Jacks
kb.add_clause(J4)
kb.add_clause(J9)
kb.add_clause(J14)
kb.add_clause(J19)
# Add here whatever is needed for your strategy.
kb.add_clause(A0)
kb.add_clause(A5)
kb.add_clause(A10)
kb.add_clause(A15)

kb.add_clause(Q3)
kb.add_clause(Q8)
kb.add_clause(Q13)
kb.add_clause(Q18)

kb.add_clause(K2)
kb.add_clause(K7)
kb.add_clause(K12)
kb.add_clause(K17)

kb.add_clause(T1)
kb.add_clause(T6)
kb.add_clause(T11)
kb.add_clause(T16)

# DEFINITION OF THE STRATEGY
# Add clauses (This list is sufficient for this strategy)
# PJ is the strategy to play jacks first, so all we need to model is all x PJ(x) <-> J(x),
# In other words that the PJ strategy should play a card when it is a jack
kb.add_clause(~J4, PJ4)
kb.add_clause(~J9, PJ9)
kb.add_clause(~J14, PJ14)
kb.add_clause(~J19, PJ19)
kb.add_clause(~PJ4, J4)
kb.add_clause(~PJ9, J9)
kb.add_clause(~PJ14, J14)
kb.add_clause(~PJ19, J19)
# Add here other strategies

kb.add_clause(~Q3, PQ3)
kb.add_clause(~Q8, PQ8)
kb.add_clause(~Q13, PQ13)
kb.add_clause(~Q18, PQ18)
kb.add_clause(~PQ3, Q3)
kb.add_clause(~PQ8, Q8)
kb.add_clause(~PQ13, Q13)
kb.add_clause(~PQ18, Q18)

kb.add_clause(~K2, PK2)
kb.add_clause(~K7, PK7)
kb.add_clause(~K12, PK12)
kb.add_clause(~K17, PK17)
kb.add_clause(~PK2, K2)
kb.add_clause(~PK7, K7)
kb.add_clause(~PK12, K12)
kb.add_clause(~PK17, K17)

kb.add_clause(~T1, PT1)
kb.add_clause(~T6, PT6)
kb.add_clause(~T11, PT11)
kb.add_clause(~T16, PT16)
kb.add_clause(~PT1, T1)
kb.add_clause(~PT6, T6)
kb.add_clause(~PT11, T11)
kb.add_clause(~PT16, T16)

kb.add_clause(~A0, PA0)
kb.add_clause(~A5, PA5)
kb.add_clause(~A10, PA10)
kb.add_clause(~A15, PA15)
kb.add_clause(~PA0, A0)
kb.add_clause(~PA5, A5)
kb.add_clause(~PA10, A10)
kb.add_clause(~PA15, A15)

kb.add_clause(~PA5)
# print all models of the knowledge base
for model in kb.models():
    print(model)

# print out whether the KB is satisfiable (if there are no models, it is not satisfiable)
print(kb.satisfiable())
