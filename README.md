# Comparación de Algoritmos de Parsing: CYK vs Bison 

## ¿Para que se usan?

Cuando se trabaja con lenguajes formales, una tarea fundamental es determinar si una cadena de texto pertenece o no a un lenguaje. Para eso existen los parsers. En este proyecto se comparan dos enfoques muy distintos para hacer exactamente lo mismo:

- **CYK**: un algoritmo clásico basado en programación dinámica
- **Bison**: una herramienta profesional que genera parsers en C, usada en compiladores reales

El lenguaje que ambos deben reconocer es `aⁿbⁿ`, es decir, cadenas como `ab`, `aabb`, `aaabbb`, y así sucesivamente. Es un lenguaje sencillo pero suficiente para comparar el rendimiento de ambos enfoques.

---

## ¿Cómo funciona cada uno?

### CYK

CYK recibe la gramática convertida a un formato estricto llamado Forma Normal de Chomsky y construye una tabla donde va anotando qué partes de la cadena puede generar cada símbolo de la gramática. Al final revisa si el símbolo inicial logra cubrir toda la cadena. Es un proceso exhaustivo que revisa todas las combinaciones posibles, lo que lo hace lento pero muy general: funciona con cualquier gramática libre de contexto, incluso las ambiguas.

Su complejidad es **O(n³)**, lo que significa que si la cadena crece, el tiempo sube de forma cúbica.

### Bison 

Bison toma la gramática escrita de forma natural y genera automáticamente un programa en C que reconoce el lenguaje. Ese programa usa una pila y una tabla de decisiones precalculada para procesar la cadena de izquierda a derecha en un solo recorrido. Es el mismo mecanismo que usan los compiladores de lenguajes como C, Python o Java.

Su complejidad es **O(n)**, lo que significa que el tiempo crece de forma proporcional a la longitud de la cadena, sin importar cuánto crezca.

---

## Resultados obtenidos

Estas son las mediciones reales obtenidas al ejecutar ambos algoritmos:

## Bison

<img width="808" height="575" alt="imagen" src="https://github.com/user-attachments/assets/58e4aa9b-f548-4b91-9d16-b40c4d4d98a6" />

## CYK

<img width="824" height="507" alt="imagen" src="https://github.com/user-attachments/assets/3dc1fe6d-34f9-4266-a819-bf9e7fd1848f" />

## Resultado

| n | Longitud | CYK (ms) | Bison (ms) | Bison es más rápido por... |
|---|----------|----------|------------|---------------------------|
| 1 | 2 | 0.001713 | 0.000049 | 35x |
| 2 | 4 | 0.006891 | 0.000067 | 103x |
| 3 | 6 | 0.017687 | 0.000062 | 285x |
| 5 | 10 | 0.069117 | 0.000054 | 1280x |
| 8 | 16 | 0.242548 | 0.000125 | 1940x |
| 10 | 20 | 0.461241 | 0.000156 | 2957x |
| 13 | 26 | 0.995166 | 0.000201 | 4951x |
| 17 | 34 | 2.466508 | 0.000256 | 9635x |

Ambos algoritmos aceptaron correctamente todas las cadenas válidas. La diferencia está únicamente en la velocidad.

<img width="2084" height="741" alt="cyk_vs_bison" src="https://github.com/user-attachments/assets/5124a80c-2c88-498c-b14c-c186047d0d40" />

---

## ¿Qué explica esa diferencia tan grande?

Hay dos factores combinados:

**El algoritmo.** CYK revisa todas las formas posibles de dividir y combinar la cadena, lo que genera muchísimo trabajo cuando la cadena crece. Bison en cambio procesa cada símbolo una sola vez y toma decisiones inmediatas gracias a la tabla que construyó al compilar.

**El lenguaje de implementación.** CYK está escrito en Python, que es un lenguaje interpretado. Bison genera código C compilado con optimización, que es mucho más cercano al hardware. Esta diferencia por sí sola puede ser de 50x a 100x, y se suma a la diferencia algorítmica.


---

## Conclusión

El experimento muestra de forma clara que Bison supera a CYK en velocidad por varios órdenes de magnitud, especialmente a medida que las cadenas crecen. Esto se debe a que Bison usa un algoritmo lineal ejecutado en código compilado, mientras CYK usa un algoritmo cúbico ejecutado en Python.

---

## Cómo ejecutar el proyecto

```bash
# 1. Instalar dependencias
sudo apt install bison flex gcc python3 python3-venv -y

# 2. Crear entorno virtual
python3 -m venv venv
source venv/bin/activate
pip install matplotlib

# 3. Compilar y ejecutar Bison
bison -d parser.y
gcc -O2 parser.tab.c -o bison_parser -lm
./bison_parser

# 4. Ejecutar CYK
python3 cyk_parser.py

# 5. Generar comparación y gráfica
python3 compare.py
```
