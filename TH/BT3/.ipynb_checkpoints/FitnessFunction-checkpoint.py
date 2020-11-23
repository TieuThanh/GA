import math

def Rastrigin(particle):
    A = 10
    d = particle.shape[0]
    return A*d + sum([particle[i]**2 - A*math.cos(2*math.pi*particle[i]) for i in range(d)])

def Rosenbrock(particle):
    return sum([100*(particle[i+1] - particle[i]**2)**2 + (1 - particle[i])**2 for i in range(particle.shape[0]-1)])

def Eggholder(particle):
    x = particle[0]
    y = particle[1]
    
    return -(y + 47)*math.sin(math.sqrt(abs(x/2 + y + 47))) - x*math.sin(math.sqrt(abs(x - y - 47)))

def Ackley(particle):
    x = particle[0]
    y = particle[1]
    return -20*math.exp(-0.2*math.sqrt(0.5*(x**2 + y**2))) - math.exp(0.5*(math.cos(2*math.pi*x) + math.cos(2*math.pi*y))) + math.e + 20

