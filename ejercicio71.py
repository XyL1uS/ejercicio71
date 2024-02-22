
import os
import pandas as pd
import matplotlib.pyplot as plt
import random

# Ruta del archivo
carpeta = "C:/proyectos/matplotlib/ejercicio71"
fichero = "madrid-airbnb-listings-apartado6.csv"
ruta = os.path.abspath(os.path.join(carpeta, fichero))

# Crear DataFrame del CSV
alojamientos = pd.read_csv(ruta, sep=';', decimal=',')
alojamientos['precio_persona'] = alojamientos['precio_persona'].round(2).convert_dtypes()
alojamientos['distrito'] = alojamientos['distrito'].astype(str)

# Definición de la función para generar colores aleatorios
def random_color():
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))

# Función para diagrama de barras con el número de alojamientos por distritos
def barras_alojamientos_distritos(alojamientos):
    fig, ax = plt.subplots()
    counts = alojamientos.distrito.value_counts()
    counts.plot(kind='bar', ax=ax, color=[random_color() for _ in range(len(counts))])
    ax.set_title('Número de alojamientos por distrito', loc="center", fontdict={'fontsize': 14, 'fontweight': 'bold', 'color': 'tab:blue'})
    ax.grid(axis='y', color='lightgray', linestyle='dashed')
    plt.xticks(rotation=45, ha='right')  # Rotar y ajustar etiquetas de distrito
    plt.savefig(os.path.join(carpeta, "diagrama_1.png"))
    plt.show()

barras_alojamientos_distritos(alojamientos)


# Función de diagrama de barras con los porcentajes acumulados de tipos de alojamientos por distritos
def barras_tipos_alojamientos_distritos(alojamientos):
    fig, ax = plt.subplots(figsize=(10, 6))
    alojamientos_tipo_distrito = alojamientos.groupby(['distrito', 'tipo_alojamiento']).size().unstack()
    
    # Definir un diccionario para almacenar los colores aleatorios para cada tipo de alojamiento
    tipos_alojamiento = alojamientos.tipo_alojamiento.unique()
    colores = {tipo: random_color() for tipo in tipos_alojamiento}
    
    # Utilizar colores aleatorios en el gráfico
    alojamientos_tipo_distrito.plot(kind='bar', stacked=True, ax=ax, color=[colores[tipo] for tipo in tipos_alojamiento])
    
    ax.set_title('Tipos de alojamiento por distrito (%)', loc="center", fontdict={'fontsize': 14, 'fontweight': 'bold', 'color': 'tab:blue'})
    ax.set_xlabel('Distrito')
    ax.set_ylabel('Número de alojamientos')
    ax.grid(axis='y', color='lightgray', linestyle='dashed')
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.7, box.height])
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
    plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))
    plt.savefig(os.path.join(carpeta, "diagrama_2.png"))
    plt.show()

barras_tipos_alojamientos_distritos(alojamientos)


# Función para diagrama de sectores con la distribución del número de alojamientos por anfitrión de unos tipos y en unos distritos dados
def sectores_tipos_alojamientos_anfitrion(alojamientos, distritos, tipos):
    fig, ax = plt.subplots()
    alojamientos_filtrados = alojamientos[alojamientos.distrito.isin(distritos) & alojamientos.tipo_alojamiento.isin(tipos)]
    counts = alojamientos_filtrados.anfitrion.value_counts(normalize=True)
    colors = [random_color() for _ in range(len(counts))]
    counts.plot(kind='pie', ax=ax, colors=colors, wedgeprops=dict(edgecolor='black'))
    ax.set_title('Distribución del número de alojamientos por anfitrión\nDistritos de ' + ', '.join(distritos) + '\nTipos de alojamiento' + ','.join(tipos), loc="center", fontdict={'fontsize':14, 'fontweight':'bold', 'color':'tab:blue'})
    ax.set_ylabel('')
    plt.savefig(os.path.join(carpeta, "diagrama_3.png"))
    plt.show()

sectores_tipos_alojamientos_anfitrion(alojamientos, ['Villaverde', 'Vicálvaro'], ['Entire home/apt', 'Hotel room'])


# Función que dibuja un diagrama de barras por distritos con los precios medios por persona y día de cada día
def barras_precios_medios_persona(alojamientos):
    fig, ax = plt.subplots(figsize=(10, 6))
    alojamientos.groupby('distrito').precio_persona.mean().plot(kind='bar', ax=ax, color=[random_color() for _ in range(len(alojamientos.distrito.unique()))])
    ax.set_title('Precio medio por persona y noche', loc="center", fontdict={'fontsize': 14, 'fontweight': 'bold', 'color': 'tab:blue'})
    ax.set_xlabel('Distrito')
    ax.set_ylabel('Precio medio')
    ax.grid(axis='y', color='lightgray', linestyle='dashed')
    plt.xticks(rotation=45, ha='right')
    plt.savefig(os.path.join(carpeta, "diagrama_4_y_6.png"))
    plt.show()

barras_precios_medios_persona(alojamientos)


# Función para diagrama de dispersión con el precio por noche y persona y la puntuación en unos distritos dados
def precios_puntuacion_distritos(alojamientos, distritos):
    fig, ax = plt.subplots()
    alojamientos_filtrados = alojamientos[alojamientos.distrito.isin(distritos)]
    alojamientos_filtrados['precio_persona'] = (alojamientos_filtrados.precio * alojamientos_filtrados.noches_minimas + alojamientos_filtrados.gastos_limpieza) / (alojamientos_filtrados.noches_minimas + alojamientos_filtrados.plazas)
    ax.scatter(alojamientos_filtrados['precio_persona'], alojamientos_filtrados['puntuacion'], color=[random_color() for _ in range(len(alojamientos_filtrados))])
    ax.set_title('Precios vs Puntuación\nDistritos de ' + ', '.join(distritos), loc="center", fontdict={'fontsize': 14, 'fontweight': 'bold', 'color': 'tab:blue'})
    ax.set_xlabel('Precio en €')
    ax.set_ylabel('Puntuación')
    plt.savefig(os.path.join(carpeta, "diagrama_5.png"))
    plt.show()

precios_puntuacion_distritos(alojamientos, ['Arganzuela', 'Centro'])