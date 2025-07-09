"""
Tests para las utilidades de reintentos
"""
import pytest
import time
from unittest import TestCase
from unittest.mock import Mock, patch
from alerts.utils.retry_utils import retry_with_backoff, retry_requests


class TestRetryUtils(TestCase):
    """Tests para las utilidades de reintentos"""
    
    def test_successful_execution_no_retry(self):
        """Test que una función exitosa no se reintenta"""
        call_count = 0
        
        @retry_with_backoff(max_retries=3)
        def successful_function():
            nonlocal call_count
            call_count += 1
            return "success"
        
        result = successful_function()
        self.assertEqual(result, "success")
        self.assertEqual(call_count, 1)
    
    def test_retry_on_exception(self):
        """Test que se reintenta cuando hay excepción"""
        call_count = 0
        
        @retry_with_backoff(max_retries=3, initial_delay=0.1)
        def failing_function():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise ValueError("Test error")
            return "success"
        
        result = failing_function()
        self.assertEqual(result, "success")
        self.assertEqual(call_count, 3)
    
    def test_max_retries_exceeded(self):
        """Test que se lanza excepción después de max_retries"""
        call_count = 0
        
        @retry_with_backoff(max_retries=2, initial_delay=0.1)
        def always_failing_function():
            nonlocal call_count
            call_count += 1
            raise ValueError("Always fails")
        
        with self.assertRaises(ValueError):
            always_failing_function()
        
        # Se llama 1 vez inicial + 2 reintentos = 3 veces total
        self.assertEqual(call_count, 3)
    
    def test_specific_exception_handling(self):
        """Test que solo se reintentan excepciones específicas"""
        call_count = 0
        
        @retry_with_backoff(exceptions=ValueError, max_retries=3, initial_delay=0.1)
        def specific_exception_function():
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                raise ValueError("Retry this")
            elif call_count == 2:
                raise TypeError("Don't retry this")
            return "should not reach"
        
        with self.assertRaises(TypeError):
            specific_exception_function()
        
        # Solo se reintenta una vez porque TypeError no está en las excepciones
        self.assertEqual(call_count, 2)
    
    def test_backoff_timing(self):
        """Test que el backoff incrementa el delay"""
        delays = []
        
        @retry_with_backoff(
            max_retries=3,
            initial_delay=0.1,
            backoff_factor=2.0,
            jitter=False
        )
        def timing_function():
            start_time = time.time()
            if len(delays) < 3:
                raise ValueError("Measure timing")
            return "success"
        
        start_time = time.time()
        
        try:
            timing_function()
        except ValueError:
            pass
        
        # Verificar que hubo reintentos con delays crecientes
        # Con initial_delay=0.1 y backoff_factor=2.0:
        # Delay 1: 0.1s
        # Delay 2: 0.2s
        # Delay 3: 0.4s
        # Total mínimo esperado: 0.7s
        total_time = time.time() - start_time
        self.assertGreater(total_time, 0.6)  # Dar margen para variaciones
    
    def test_max_delay_limit(self):
        """Test que el delay no excede max_delay"""
        @retry_with_backoff(
            max_retries=5,
            initial_delay=1.0,
            backoff_factor=10.0,
            max_delay=2.0,
            jitter=False
        )
        def delay_limit_function():
            # Esta función siempre falla para probar el límite de delay
            raise ValueError("Test max delay")
        
        start_time = time.time()
        
        try:
            delay_limit_function()
        except ValueError:
            pass
        
        total_time = time.time() - start_time
        
        # Con max_delay=2.0, incluso con backoff alto, no debe exceder
        # 1 + 2 + 2 + 2 + 2 = 9 segundos (5 delays máximos de 2s cada uno)
        # Pero damos margen para la ejecución
        self.assertLess(total_time, 12.0)
    
    @patch('requests.get')
    def test_retry_requests_decorator(self, mock_get):
        """Test del decorador preconfigurado para requests"""
        import requests
        
        # Simular fallo seguido de éxito
        mock_get.side_effect = [
            requests.exceptions.Timeout("Timeout"),
            requests.exceptions.ConnectionError("Connection error"),
            Mock(status_code=200, text="Success")
        ]
        
        @retry_requests()
        def make_request():
            response = requests.get("https://example.com")
            return response.text
        
        result = make_request()
        self.assertEqual(result, "Success")
        self.assertEqual(mock_get.call_count, 3)