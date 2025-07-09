"""
Tests para el servicio de extracción de PDFs
"""
import pytest
from unittest import TestCase
from unittest.mock import Mock, patch, MagicMock
from alerts.services.pdf_extractor import PDFExtractor


class TestPDFExtractor(TestCase):
    """Tests para el servicio de extracción de PDFs"""
    
    def setUp(self):
        self.extractor = PDFExtractor()
    
    def test_is_valid_text(self):
        """Test de validación de texto extraído"""
        # Texto válido
        valid_text = "Este es un texto válido con suficientes palabras para ser considerado útil en el contexto de extracción."
        self.assertTrue(self.extractor._is_valid_text(valid_text))
        
        # Texto muy corto
        short_text = "Muy corto"
        self.assertFalse(self.extractor._is_valid_text(short_text))
        
        # Texto con pocas palabras
        few_words_text = "a b c d e"
        self.assertFalse(self.extractor._is_valid_text(few_words_text))
        
        # Texto con muchos caracteres especiales
        special_chars_text = "!@#$%^&*()_+{}[]|\\:;<>?,./~`" * 10
        self.assertFalse(self.extractor._is_valid_text(special_chars_text))
        
        # Texto vacío
        self.assertFalse(self.extractor._is_valid_text(""))
        self.assertFalse(self.extractor._is_valid_text(None))
    
    @patch('PyPDF2.PdfReader')
    def test_extract_with_pypdf2_success(self, mock_pdf_reader):
        """Test de extracción exitosa con PyPDF2"""
        # Configurar mock
        mock_page = Mock()
        mock_page.extract_text.return_value = "Este es el contenido extraído del PDF con PyPDF2. Contiene suficiente texto para ser válido."
        
        mock_reader_instance = Mock()
        mock_reader_instance.pages = [mock_page, mock_page]
        mock_pdf_reader.return_value = mock_reader_instance
        
        # Ejecutar extracción
        pdf_content = b"fake pdf content"
        text = self.extractor._extract_with_pypdf2(pdf_content, max_pages=2)
        
        # Verificar
        self.assertIn("Este es el contenido extraído", text)
        self.assertEqual(mock_page.extract_text.call_count, 2)
    
    @patch('pdfminer.high_level.extract_text')
    def test_extract_with_pdfminer_success(self, mock_extract_text):
        """Test de extracción exitosa con PDFMiner"""
        expected_text = "Contenido extraído con PDFMiner. Este método es más robusto para PDFs complejos."
        mock_extract_text.return_value = expected_text
        
        pdf_content = b"fake pdf content"
        text = self.extractor._extract_with_pdfminer(pdf_content, max_pages=2)
        
        self.assertEqual(text, expected_text.strip())
        mock_extract_text.assert_called_once()
    
    @patch('pytesseract.image_to_string')
    @patch('pdf2image.convert_from_bytes')
    def test_extract_with_ocr_success(self, mock_convert, mock_ocr):
        """Test de extracción exitosa con OCR"""
        # Configurar mocks
        mock_image = Mock()
        mock_convert.return_value = [mock_image, mock_image]
        mock_ocr.return_value = "Texto extraído mediante OCR desde imagen escaneada del documento."
        
        pdf_content = b"fake pdf content"
        text = self.extractor._extract_with_ocr(pdf_content, max_pages=2)
        
        # Verificar
        self.assertIn("OCR", text)
        self.assertEqual(mock_ocr.call_count, 2)
        mock_convert.assert_called_once_with(pdf_content, first_page=1, last_page=2, dpi=200)
    
    @patch('alerts.services.pdf_extractor.PDFExtractor._extract_with_pypdf2')
    @patch('alerts.services.pdf_extractor.PDFExtractor._extract_with_pdfminer')
    @patch('alerts.services.pdf_extractor.PDFExtractor._extract_with_ocr')
    def test_fallback_mechanism(self, mock_ocr, mock_pdfminer, mock_pypdf2):
        """Test del mecanismo de fallback entre métodos"""
        # PyPDF2 falla
        mock_pypdf2.side_effect = Exception("PyPDF2 failed")
        
        # PDFMiner retorna texto inválido
        mock_pdfminer.return_value = "abc"  # Muy corto
        
        # OCR funciona
        mock_ocr.return_value = "Este es un texto válido extraído por OCR con suficientes palabras para pasar la validación."
        
        pdf_content = b"fake pdf content"
        text, method = self.extractor.extract_text(pdf_content)
        
        # Verificar que se intentaron los métodos en orden
        mock_pypdf2.assert_called_once()
        mock_pdfminer.assert_called_once()
        mock_ocr.assert_called_once()
        
        # Verificar resultado
        self.assertEqual(method, "ocr")
        self.assertIn("texto válido extraído por OCR", text)
    
    @patch('alerts.services.pdf_extractor.PDFExtractor._extract_with_pypdf2')
    @patch('alerts.services.pdf_extractor.PDFExtractor._extract_with_pdfminer')
    @patch('alerts.services.pdf_extractor.PDFExtractor._extract_with_ocr')
    @patch('alerts.services.pdf_extractor.PDFExtractor._extract_with_enhanced_ocr')
    def test_all_methods_fail(self, mock_enhanced_ocr, mock_ocr, mock_pdfminer, mock_pypdf2):
        """Test cuando todos los métodos fallan"""
        # Todos los métodos fallan
        mock_pypdf2.side_effect = Exception("Failed")
        mock_pdfminer.side_effect = Exception("Failed")
        mock_ocr.side_effect = Exception("Failed")
        mock_enhanced_ocr.side_effect = Exception("Failed")
        
        pdf_content = b"fake pdf content"
        text, method = self.extractor.extract_text(pdf_content)
        
        # Verificar resultado
        self.assertEqual(text, "")
        self.assertEqual(method, "failed")
    
    @patch('PyPDF2.PdfReader')
    def test_get_pdf_info(self, mock_pdf_reader):
        """Test de obtención de información del PDF"""
        # Configurar mock
        mock_page = Mock()
        mock_page.extract_text.return_value = "Contenido de la página"
        
        mock_reader_instance = Mock()
        mock_reader_instance.pages = [mock_page, mock_page, mock_page]
        mock_reader_instance.is_encrypted = False
        mock_pdf_reader.return_value = mock_reader_instance
        
        pdf_content = b"fake pdf content of some length"
        info = self.extractor.get_pdf_info(pdf_content)
        
        # Verificar información
        self.assertEqual(info['num_pages'], 3)
        self.assertEqual(info['size_bytes'], len(pdf_content))
        self.assertFalse(info['encrypted'])
        self.assertTrue(info['has_text'])
    
    @patch('requests.get')
    def test_extract_text_from_url_success(self, mock_get):
        """Test de extracción desde URL"""
        # Configurar mock de requests
        mock_response = Mock()
        mock_response.content = b"fake pdf content"
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        # Mock del método extract_text
        with patch.object(self.extractor, 'extract_text') as mock_extract:
            mock_extract.return_value = ("Texto extraído", "pypdf2")
            
            text, method = self.extractor.extract_text_from_url("https://example.com/test.pdf")
            
            # Verificar
            mock_get.assert_called_once_with("https://example.com/test.pdf", timeout=30)
            mock_extract.assert_called_once_with(b"fake pdf content", 2)
            self.assertEqual(text, "Texto extraído")
            self.assertEqual(method, "pypdf2")