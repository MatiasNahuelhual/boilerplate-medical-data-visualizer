import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Add 'overweight' column
df['overweight'] = (df['weight'] / (df['height']/100)**2).apply(lambda x: 1 if x > 25 else 0)

# Normalice los datos haciendo que 0 sea siempre bueno y 1 siempre malo. Si el valor de 'colesterol' o 'gluc' es 1, establezca el valor en 0. Si el valor es mayor que 1, establezca el valor en 1.
df['cholesterol'] = df['cholesterol'].apply(lambda x: 0 if x == 1 else 1)
df['gluc'] = df['gluc'].apply(lambda x: 0 if x == 1 else 1)


# Draw Categorical Plot
# Draw Categorical Plot
def draw_cat_plot():
    # Crear DataFrame para el catplot usando `pd.melt` con solo los valores de 'cholesterol', 'gluc', 'smoke', 'alco', 'active' y 'overweight'.
    df_cat = pd.melt(df, id_vars='cardio', var_name='variable', value_vars=['alco', 'active', 'cholesterol', 'gluc', 'overweight', 'smoke'])
    
    # Agrupar y reformatear los datos para dividirlos por 'cardio'. Mostrar los recuentos de cada característica. Debes renombrar una de las columnas para que el catplot funcione correctamente.
    df_cat = pd.melt(df, var_name='variable', value_vars=['active', 'alco', 'cholesterol', 'gluc', 'overweight', 'smoke'], id_vars='cardio')
    
    # Dibujar el catplot con 'sns.catplot()'
    fig = sns.catplot(data=df_cat, kind="count", x="variable", hue="value", col="cardio", palette="Set2").set_axis_labels("variable", "total")
    fig = fig.fig
    
    # No modificar las dos líneas siguientes
    fig.savefig('catplot.png')
    return fig


def draw_heat_map():
    # Limpiar los datos
    df_heat = df[(df['ap_lo'] <= df['ap_hi']) &
                 (df['height'] >= df['height'].quantile(0.025)) &
                 (df['height'] <= df['height'].quantile(0.975)) &
                 (df['weight'] >= df['weight'].quantile(0.025)) &
                 (df['weight'] <= df['weight'].quantile(0.975))
                ]

    # Calcular la matriz de correlación
    corr = df_heat.corr()

    # Generar una máscara para el triángulo superior
    mask = np.triu(np.ones_like(corr, dtype=bool))

    # Configurar la figura de matplotlib
    fig, ax = plt.subplots(figsize=(7, 5))

    # Dibujar el mapa de calor con 'sns.heatmap()'
    sns.heatmap(corr, mask=mask, cmap='coolwarm', fmt='.1f', vmax=.3, linewidths=.5, square=True, cbar_kws={'shrink': 0.5}, annot=True, center=0)

    # No modificar las dos líneas siguientes
    fig.savefig('heatmap.png')
    return fig
