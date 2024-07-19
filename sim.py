import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('ambient_temperature.csv')

temperatura_interna_inicial = 20.0
limite_superior = 22.0
limite_inferior = 18.0
z1 = 0.001
z2 = 0.005  # Cambiado a 0.5%
temperatura_agua_fria = -6.0
amplitud_bomba = 10

temperatura_interna = temperatura_interna_inicial
bomba_abierta = False
estados_bomba = []
temperaturas = []

for index, row in df.iterrows():
    temperatura_ambiente = row['temperature']
    
    if index < 7 * 24 * 60:
        if index < 6 * 24 * 60:
            temperatura_interna += 0.01
        else:
            dia = index // (24 * 60)
            minutos_restantes = (24 * 60) - (index % (24 * 60))
            factor_reduccion = minutos_restantes / (24 * 60)
            aumento_diario = 0.01 * factor_reduccion
            temperatura_interna += aumento_diario
    
    diferencia = temperatura_ambiente - temperatura_interna
    
    temperatura_interna += z1 * diferencia
    
    if temperatura_interna > limite_superior:
        bomba_abierta = True
    elif temperatura_interna < limite_inferior:
        bomba_abierta = False
    
    if bomba_abierta:
        temperatura_agua = temperatura_agua_fria
        temperatura_interna += z2 * (temperatura_agua - temperatura_interna)
    
    estados_bomba.append(1 if bomba_abierta else 0)
    temperaturas.append(temperatura_interna)

plt.figure(figsize=(15, 10))

plt.plot(df['minute'], df['temperature'], label='Temperatura Ambiente', linestyle='--', alpha=0.7)

plt.plot(df['minute'], temperaturas, label='Temperatura Interna', alpha=0.8)

plt.axhline(y=limite_superior, color='r', linestyle='--', label='Límite Superior')
plt.axhline(y=limite_inferior, color='g', linestyle='--', label='Límite Inferior')

estados_bomba = np.array(estados_bomba)
bomba_time = np.repeat(df['minute'], 2)[1:]
bomba_states_plot = np.repeat(estados_bomba, 2)[:-1] * amplitud_bomba
plt.step(bomba_time, bomba_states_plot, where='post', label='Estado de la Bomba')

plt.xlabel('Minuto')
plt.ylabel('Temperatura (°C)')
plt.title('Simulación de Control de Temperatura del Fermentador')
plt.ylim(0, 50)
plt.grid(True)
plt.legend()

plt.savefig('simulacion_temperatura_fermentador_limites_permisivos.png')

plt.show()
