import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from sympy import symbols, diff, lambdify, sin, cos, tan, exp, log

def newton_raphson(function, derivative, initial_guess, tolerance, max_iterations):
    x = initial_guess
    iteration = 0

    while abs(function(x)) > tolerance and iteration < max_iterations:
        x = x - function(x) / derivative(x)
        iteration += 1

    if abs(function(x)) <= tolerance:
        return x
    else:
        return None

def plot_function(function, xlim):
    x_vals = np.linspace(xlim[0], xlim[1], 1000)
    y_vals = function(x_vals)

    fig, ax = plt.subplots()
    ax.plot(x_vals, y_vals)
    ax.set_xlabel('x')
    ax.set_ylabel('f(x)')
    ax.set_title('Gráfico de la función')
    ax.grid(True)

    return fig, ax

def main():
    st.title("Método de Newton-Raphson")

    # Input de la función
    st.subheader("Ingrese la función f(x):")
    function_text = st.text_input("f(x)", "log(x) - 2")

    # Calcular la derivada de la función
    x = symbols('x')
    try:
        function_expr = eval(function_text)
        derivative_expr = diff(function_expr, x)
        derivative = lambdify(x, derivative_expr)
        function = lambdify(x, function_expr)
    except Exception as e:
        st.error("Error al calcular la derivada: " + str(e))
        return

    # Gráfico de la función
    fig, ax = plot_function(function, xlim=(-10, 10))
    st.pyplot(fig)

    # Input del valor inicial
    st.subheader("Ingrese el valor inicial:")
    initial_guess = st.number_input("Valor inicial", value=0.0)

    # Input de la tolerancia
    st.subheader("Ingrese la tolerancia:")
    tolerance = st.number_input("Tolerancia", value=1e-6)

    # Input del número máximo de iteraciones
    st.subheader("Ingrese el número máximo de iteraciones:")
    max_iterations = st.number_input("Iteraciones máximas", value=100)

    # Botón para ejecutar el método
    if st.button("Ejecutar"):
        try:
            # Ejecutar el método de Newton-Raphson
            result = newton_raphson(function, derivative, initial_guess, tolerance, max_iterations)

            if result is not None:
                st.success(f"La raíz encontrada es: {result}")

                # Gráfico con las raíces
                fig, ax = plot_function(function, xlim=(-10, 10))
                roots = [result]
                x_vals = np.linspace(-10, 10, 1000)
                y_vals = function(x_vals)
                ax.plot(x_vals, y_vals, label='Función')
                ax.scatter(roots, [function(root) for root in roots], color='red', label='Raíz encontrada')
                ax.legend()
                ax.grid(True)
                st.pyplot(fig)

            else:
                st.error("El método no convergió. Intente con otro valor inicial o ajuste los parámetros.")
        except Exception as e:
            st.error("Error: " + str(e))

if __name__ == "__main__":
    main()
