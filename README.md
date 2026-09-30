# Gestor Inteligente de Clientes (GIC)

Sistema de gestión de clientes desarrollado en Python bajo el paradigma de **Programación Orientada a Objetos (POO)**. El sistema integra interfaz gráfica (Tkinter), persistencia relacional y no relacional (SQLite, JSON, CSV), manejo de excepciones personalizadas, registros de actividad (logging) e integración simulada con servicios API externos.

---

## 🚀 Características Principales

* **Interfaz Gráfica (GUI):** Formulario dinámico y tabla interactiva con capacidades de alta, consulta, modificación y eliminación (CRUD).
* **Principios POO:**
  * **Encapsulamiento:** Atributos privados con acceso controlado vía propiedades (`@property`).
  * **Herencia y Polimorfismo:** Clase base `Cliente` extendida por `ClienteRegular`, `ClientePremium` y `ClienteCorporativo`.
  * **Sobrecarga de Métodos Especiales:** Implementación de `__str__` para representación formateada y `__eq__` para comparación por identidad de cliente (`id_cliente`).
* **Persistencia Multi-formato:**
  * Base de datos **SQLite** relacional.
  * Exportación masiva a formatos **JSON** y **CSV**.
* **Manejo de Errores e Integraciones:**
  * Excepción personalizada `ValidacionError` para gestión de inputs erróneos.
  * Consumo simulado de APIs web vía solicitudes HTTP.
  * Registro automatizado de eventos del sistema en `gic_sistema.log`.
