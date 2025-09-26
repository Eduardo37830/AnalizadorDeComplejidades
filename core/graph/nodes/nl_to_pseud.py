import requests
import json
from ..state import GraphState

def convert_to_pseudocode(state: GraphState) -> GraphState:
    """
    Convierte lenguaje natural a pseudocódigo estructurado y corrige pseudocódigo existente.
    Usa LLM local en localhost:1234 con convenciones específicas de pseudocódigo Pascal.
    """
    input_text = state.get("pseudocode", "") or state.get("code", "")

    if not input_text.strip():
        state["errors"].append("No se proporcionó texto para procesar")
        return state

    try:
        # Configurar el prompt del sistema para el LLM con convenciones específicas
        system_prompt = """Eres un experto en análisis de algoritmos. Tu tarea es convertir texto a pseudocódigo usando EXACTAMENTE estas convenciones:

SINTAXIS OBLIGATORIA:
- Asignación: usar "🡨" (ejemplo: x 🡨 5)
- Comentarios: usar "►" al final de línea
- FOR: for variableContadora 🡨 valorInicial to limite do begin ... end
- WHILE: while (condicion) do begin ... end  
- REPEAT: repeat ... until (condicion)
- IF: if (condicion) then begin ... end else begin ... end
- Arreglos: A[i], A[1..j] para rangos
- Objetos: Casa {Area color propietario}, acceso con objeto.campo
- Llamadas: CALL nombre_subrutina(parametros)
- Booleanos: T (true), F (false)
- Operadores booleanos: and, or, not
- Operadores relacionales: <, >, ≤, ≥, =, ≠
- Operadores matemáticos: +, -, *, /, mod, div, ┌┐(techo), └┘(piso)

ESTRUCTURA DE ALGORITMO:
algorithm nombre_algoritmo
begin
    ► declaraciones locales aquí
    accion 1
    accion 2
    ...
end

EJEMPLOS:
- for i 🡨 1 to n do begin
- while (i ≤ n) do begin  
- if (A[i] > max) then begin max 🡨 A[i] end
- CALL ordenar_burbuja(A[1..n])

Convierte el texto a pseudocódigo usando EXACTAMENTE esta sintaxis. NO uses sintaxis de otros lenguajes."""

        # Preparar la petición al LLM local
        payload = {
            "model": "google/gemma-3n-e4b",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Convierte este texto a pseudocódigo usando las convenciones especificadas: {input_text}"}
            ],
            "temperature": 0.2,  # Temperatura muy baja para máxima consistencia
            "max_tokens": 1500,
            "stream": False
        }

        # Llamar al LLM local
        response = requests.post(
            "http://localhost:1234/v1/chat/completions",
            headers={"Content-Type": "application/json"},
            json=payload,
            timeout=120
        )

        if response.status_code == 200:
            result = response.json()
            corrected_pseudocode = result["choices"][0]["message"]["content"].strip()

            # Validar que usa las convenciones correctas
            if "🡨" in corrected_pseudocode or "begin" in corrected_pseudocode.lower():
                # El LLM siguió las convenciones
                state["pseudocode"] = corrected_pseudocode
                state["code"] = corrected_pseudocode
            else:
                # El LLM no siguió las convenciones, agregar advertencia
                state["errors"].append("Advertencia: El LLM no siguió completamente las convenciones de pseudocódigo")
                state["pseudocode"] = corrected_pseudocode
                state["code"] = corrected_pseudocode

        else:
            error_msg = f"Error en LLM local: {response.status_code} - {response.text}"
            state["errors"].append(error_msg)
            # Usar el texto original si falla el LLM
            state["pseudocode"] = input_text
            state["code"] = input_text

    except requests.exceptions.RequestException as e:
        error_msg = f"Error de conexión con LLM local: {str(e)}"
        state["errors"].append(error_msg)
        # Usar el texto original si falla la conexión
        state["pseudocode"] = input_text
        state["code"] = input_text
    except Exception as e:
        error_msg = f"Error inesperado en procesamiento LLM: {str(e)}"
        state["errors"].append(error_msg)
        state["pseudocode"] = input_text
        state["code"] = input_text

    return state
