m = 20
g = 9.8
c = 0.01
V = 0  
t = 0  
dt = 2 

for i in range(20):
    print(f"V{t}={V}")
    V= V+(g -(c/m)*V)*dt  
    t=t+dt  