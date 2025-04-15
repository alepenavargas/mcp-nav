"""Pruebas para el módulo WebsiteNavigator."""

import unittest
from unittest.mock import MagicMock, patch

from app import WebsiteNavigator


class TestWebsiteNavigator(unittest.TestCase):
    """Pruebas para la clase WebsiteNavigator."""

    def setUp(self):
        """Configurar el entorno de prueba."""
        self.navigator = WebsiteNavigator()
    
    def test_init(self):
        """Probar la inicialización correcta."""
        self.assertEqual(self.navigator.current_url, "https://modelcontextprotocol.io")
        self.assertEqual(self.navigator.history, ["https://modelcontextprotocol.io"])
    
    @patch('requests.Session.get')
    def test_get_page_content(self, mock_get):
        """Probar la obtención de contenido de página."""
        # Configurar el mock
        mock_response = MagicMock()
        mock_response.text = """
        <html>
            <head><title>Test Page</title></head>
            <body>
                <main>
                    <p>Main content</p>
                    <a href="/test">Test link</a>
                    <a href="https://example.com">External link</a>
                </main>
            </body>
        </html>
        """
        mock_get.return_value = mock_response
        
        # Llamar a la función a probar
        result = self.navigator.get_page_content("/test-page")
        
        # Verificar resultados
        self.assertEqual(result["title"], "Test Page")
        self.assertIn("Main content", result["content"])
        self.assertEqual(len(result["links"]), 1)  # Solo debería incluir enlaces internos
        self.assertEqual(result["links"][0]["url"], "/test")
        self.assertEqual(self.navigator.current_url, "https://modelcontextprotocol.io/test-page")
        self.assertEqual(len(self.navigator.history), 2)


if __name__ == "__main__":
    unittest.main() 