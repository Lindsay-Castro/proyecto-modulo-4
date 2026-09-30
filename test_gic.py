import unittest
from main import ClienteRegular, ClientePremium, ClienteCorporativo, ValidacionError

class TestSistemaGIC(unittest.TestCase):

    def test_creacion_cliente_regular_exito(self):
        """Verifica la creación e inicialización correcta de un Cliente Regular."""
        cliente = ClienteRegular("101", "Carlos Mendoza", "carlos@mail.com", "987654321")
        self.assertEqual(cliente.id_cliente, "101")
        self.assertEqual(cliente.nombre, "Carlos Mendoza")
        self.assertEqual(cliente.obtener_descuento(), 5.0)

    def test_creacion_cliente_premium_exito(self):
        """Verifica el cálculo de descuento y atributos en Cliente Premium."""
        cliente = ClientePremium("102", "Ana Lopez", "ana@mail.com", "912345678", "VIP")
        self.assertEqual(cliente.nivel_membresia, "VIP")
        self.assertEqual(cliente.obtener_descuento(), 15.0)

    def test_validacion_email_invalido(self):
        """Verifica que se lance una excepción ValidacionError si el email es incorrecto."""
        with self.assertRaises(ValidacionError):
            ClienteRegular("103", "Pedro Soto", "email_invalido.com", "987654321")

    def test_validacion_telefono_invalido(self):
        """Verifica que falle si el teléfono tiene letras o menos de 7 dígitos."""
        with self.assertRaises(ValidacionError):
            ClienteRegular("104", "Maria Paz", "maria@mail.com", "123abc")

    def test_metodo_especial_igualdad_eq(self):
        """Verifica que el método __eq__ reconozca dos objetos como iguales si comparten ID."""
        cliente1 = ClienteRegular("200", "Juan Perez", "juan@mail.com", "987654321")
        cliente2 = ClientePremium("200", "Juan P. Perez", "juan.perez@mail.com", "911111111", "Gold")
        self.assertEqual(cliente1, cliente2)

if __name__ == "__main__":
    unittest.main()