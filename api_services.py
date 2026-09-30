import logging
import requests

logging.basicConfig(
    filename="gic_sistema.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)

class ServicioAPI:
    """Servicio de integración con APIs externas y gestión de logs."""
    
    @staticmethod
    def validar_email_api(email):
        """Simula y consulta la validez de un correo electrónico mediante una API externa."""
        try:
            response = requests.get(f"https://jsonplaceholder.typicode.com/users?email={email}", timeout=3)
            logging.info(f"Consulta a API de validación para email: {email} | Status: {response.status_code}")
            return True
        except Exception as e:
            logging.error(f"Error al conectar con API de validación de email ({email}): {e}")
            return True

    @staticmethod
    def enviar_notificacion_bienvenida(cliente_nombre, email):
        """Envía una notificación automatizada simulada a través de API externa."""
        try:
            payload = {
                "to": email,
                "subject": "Bienvenido al Gestor Inteligente de Clientes",
                "body": f"Hola {cliente_nombre}, tu registro ha sido exitoso."
            }
            response = requests.post("https://jsonplaceholder.typicode.com/posts", json=payload, timeout=3)
            if response.status_code in [200, 201]:
                logging.info(f"Notificación enviada exitosamente vía API a {email}")
                return True
        except Exception as e:
            logging.error(f"Error al enviar notificación API a {email}: {e}")
            return False