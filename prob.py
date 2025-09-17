from problog.program import PrologString  # Permite crear modelos Problog desde texto
from problog import get_evaluatable        # Función para ejecutar inferencia sobre el modelo

# Datos históricos de clima para dos semanas (lunes a domingo)
clima_semana1 = {
    'lunes': 'soleado',
    'martes': 'lluvioso',
    'miércoles': 'nublado',
    'jueves': 'lluvioso',
    'viernes': 'soleado',
    'sábado': 'lluvioso',
    'domingo': 'soleado'
}

clima_semana2 = {
    'lunes': 'nublado',
    'martes': 'soleado',
    'miércoles': 'soleado',
    'jueves': 'lluvioso',
    'viernes': 'nublado',
    'sábado': 'soleado',
    'domingo': 'soleado'
}

# Función que construye hechos probabilísticos para un día específico según los datos de ambas semanas
# Utiliza notación 'p::hecho.' de Problog para asignar la probabilidad p al hecho
def construir_hechos(dia, clima1, clima2):
    if clima1 == clima2:
        prob = 1.0  # Si ambos climas coinciden, asigna probabilidad 1 (certeza)
        return f"{prob}::clima({dia},{clima1})."
    else:
        # Si los climas son diferentes, asigna probabilidad 0.5 a cada uno, modelando incertidumbre
        return f"0.5::clima({dia},{clima1}). 0.5::clima({dia},{clima2})."

# Lista de días válidos para la predicción
dias = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo']

# Entrada del usuario para seleccionar el día que desea predecir
dia_elegido = input("Ingrese el día a predecir (lunes a domingo): ").lower()

if dia_elegido not in dias:
    print("Día no válido.")
else:
    # Construir el hecho probabilístico para el día elegido
    hecho = construir_hechos(dia_elegido, clima_semana1[dia_elegido], clima_semana2[dia_elegido])
    
    # Construir el modelo Problog completo en texto, combinando los hechos y las consultas (queries)
    modelo_problog = f"""
    {hecho}

    % Consultas que piden la probabilidad de cada tipo de clima para el día seleccionado
    query(clima({dia_elegido}, soleado)).
    query(clima({dia_elegido}, lluvioso)).
    query(clima({dia_elegido}, nublado)).
    """
    
    # Evaluar el modelo: realiza inferencia probabilística con Problog
    # get_evaluatable().create_from() crea un evaluador que procesa el modelo
    # evaluate() ejecuta la consulta y devuelve un diccionario con términos y sus probabilidades
    resultado = get_evaluatable().create_from(PrologString(modelo_problog)).evaluate()

    # Procesar resultados: extraer la probabilidad de cada clima
    # 'term' es un objeto Term de Problog; se obtiene el segundo argumento que es el tipo de clima
    resultados_clima = {}
    for term, prob in resultado.items():
        if prob > 0:
            clima_tipo = str(term.args[1])
            resultados_clima[clima_tipo] = prob
    
    # Mostrar las probabilidades calculadas para el día seleccionado
    print(f"Probabilidades para el día {dia_elegido}:")
    for clima, prob in resultados_clima.items():
        print(f"- {clima}: {prob:.2f}")

    # Determinar cuál(es) clima(s) tiene(n) la probabilidad más alta para identificar la mejor opción
    max_prob = max(resultados_clima.values())
    mejores_climas = [c for c, p in resultados_clima.items() if p == max_prob]

    # Mostrar resultado: si hay empate entre varios climas con la probabilidad máxima, mostrar todos
    if len(mejores_climas) > 1:
        print("Mejor opción: empate entre")
        for c in mejores_climas:
            print(f"- {c} con probabilidad {max_prob:.2f}")
    else:
        print(f"Mejor opción: {mejores_climas[0]} con probabilidad {max_prob:.2f}")
