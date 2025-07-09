"""
Tests para el servicio de caché
"""
import pytest
from django.test import TestCase
from django.core.cache import cache
from datetime import datetime
from alerts.services.cache_service import CacheService


class TestCacheService(TestCase):
    """Tests para el servicio de caché"""
    
    def setUp(self):
        self.cache_service = CacheService()
        cache.clear()
    
    def tearDown(self):
        cache.clear()
    
    def test_pdf_cache_operations(self):
        """Test de operaciones básicas de caché para PDFs"""
        url = "https://example.com/test.pdf"
        content = b"Test PDF content"
        
        # Verificar que no existe en caché
        self.assertIsNone(self.cache_service.get_pdf_content(url))
        
        # Guardar en caché
        self.cache_service.set_pdf_content(url, content)
        
        # Verificar que se puede recuperar
        cached_content = self.cache_service.get_pdf_content(url)
        self.assertEqual(cached_content, content)
    
    def test_scraping_result_cache(self):
        """Test de caché para resultados de scraping"""
        date = datetime(2024, 1, 1)
        results = {
            'publicaciones': [
                {'titulo': 'Test 1', 'url': 'url1'},
                {'titulo': 'Test 2', 'url': 'url2'}
            ],
            'valores_monedas': {'dolar': '850.50', 'euro': '920.30'}
        }
        
        # Verificar que no existe
        self.assertIsNone(self.cache_service.get_scraping_result(date))
        
        # Guardar resultados
        self.cache_service.set_scraping_result(date, results)
        
        # Recuperar y verificar
        cached_results = self.cache_service.get_scraping_result(date)
        self.assertEqual(cached_results, results)
    
    def test_api_response_cache(self):
        """Test de caché para respuestas de API"""
        endpoint = "https://api.example.com/analyze"
        params = {'text': 'Test text', 'lang': 'es'}
        response = {'summary': 'Test summary', 'confidence': 0.95}
        
        # Verificar que no existe
        self.assertIsNone(self.cache_service.get_api_response(endpoint, params))
        
        # Guardar respuesta
        self.cache_service.set_api_response(endpoint, params, response)
        
        # Recuperar y verificar
        cached_response = self.cache_service.get_api_response(endpoint, params)
        self.assertEqual(cached_response, response)
    
    def test_cache_invalidation(self):
        """Test de invalidación de caché"""
        date = datetime(2024, 1, 1)
        results = {'test': 'data'}
        
        # Guardar y verificar que existe
        self.cache_service.set_scraping_result(date, results)
        self.assertIsNotNone(self.cache_service.get_scraping_result(date))
        
        # Invalidar caché
        self.cache_service.invalidate_scraping_cache(date)
        
        # Verificar que ya no existe
        self.assertIsNone(self.cache_service.get_scraping_result(date))
    
    def test_get_or_set(self):
        """Test de get_or_set con función callable"""
        key = "test_key"
        value = "test_value"
        call_count = 0
        
        def generate_value():
            nonlocal call_count
            call_count += 1
            return value
        
        # Primera llamada debe ejecutar la función
        result1 = self.cache_service.get_or_set(key, generate_value)
        self.assertEqual(result1, value)
        self.assertEqual(call_count, 1)
        
        # Segunda llamada debe obtener del caché sin ejecutar la función
        result2 = self.cache_service.get_or_set(key, generate_value)
        self.assertEqual(result2, value)
        self.assertEqual(call_count, 1)  # No debe incrementar
    
    def test_cache_key_generation(self):
        """Test de generación de claves de caché"""
        # Test de generación básica
        key = self.cache_service._generate_key("prefix", "identifier")
        self.assertEqual(key, "prefix:identifier")
        
        # Test de hash de URL
        url = "https://example.com/very/long/url/with/parameters?param1=value1&param2=value2"
        hash1 = self.cache_service._hash_url(url)
        hash2 = self.cache_service._hash_url(url)
        
        # El hash debe ser consistente
        self.assertEqual(hash1, hash2)
        
        # El hash debe ser de longitud fija (MD5)
        self.assertEqual(len(hash1), 32)