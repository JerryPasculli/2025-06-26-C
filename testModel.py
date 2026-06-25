from model.model import Model

self_model = Model()
t1 = self_model.creaGrafo(1993, 1998)
print(t1)
t2 = self_model.output()
print(t2)
t3 = self_model.percorso(4, 6)
print(t3)