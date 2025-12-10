import unittest
import numpy as np
import os
from unittest.mock import patch, MagicMock

# Assuming src is in the Python path
from src.decision_logic import get_speed_limit, get_weather_speed_reduction
from src.llm_integration import get_simulated_aqi, get_llm_speed_reduction_recommendation

class TestLLMIntegration(unittest.TestCase):

    def test_get_simulated_aqi(self):
        # Test that AQI is within expected ranges for different hours
        aqi_morning = get_simulated_aqi(8) # Morning rush hour
        self.assertGreaterEqual(aqi_morning, 70)
        self.assertLessEqual(aqi_morning, 120)

        aqi_evening = get_simulated_aqi(18) # Evening rush hour
        self.assertGreaterEqual(aqi_evening, 80)
        self.assertLessEqual(aqi_evening, 150)

        aqi_off_peak = get_simulated_aqi(2) # Off-peak
        self.assertGreaterEqual(aqi_off_peak, 30)
        self.assertLessEqual(aqi_off_peak, 90)

    @patch('src.llm_integration.genai')
    @patch.dict(os.environ, {"GEMINI_API_KEY": "fake_key"})
    def test_get_llm_speed_reduction_recommendation_api(self, mock_genai):
        # Configure the mock to return a specific reduction
        mock_model = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "20"
        mock_model.generate_content.return_value = mock_response
        mock_genai.GenerativeModel.return_value = mock_model

        # Test with an AQI that would normally trigger fallback logic if API failed
        # But here we force the API to return "20" regardless of input to prove it's using the mock
        reduction = get_llm_speed_reduction_recommendation(120)
        self.assertEqual(reduction, 20)
        mock_model.generate_content.assert_called_once()

    @patch.dict(os.environ, {}, clear=True) # Ensure no API key
    def test_get_llm_speed_reduction_recommendation_fallback(self):
        # Test fallback logic (no API key)
        self.assertEqual(get_llm_speed_reduction_recommendation(30), 0) # Good
        self.assertEqual(get_llm_speed_reduction_recommendation(75), 10) # Moderate
        self.assertEqual(get_llm_speed_reduction_recommendation(120), 20) # Unhealthy for sensitive groups
        self.assertEqual(get_llm_speed_reduction_recommendation(180), 30) # Unhealthy for all


class TestDecisionLogic(unittest.TestCase):

    def setUp(self):
        # Create mocks for NN components
        self.mock_model = MagicMock()
        self.mock_scaler = MagicMock()
        self.mock_mean_values = np.zeros(8) # 8 features
        
        # Configure scaler mock to return input (identity) for simplicity or specific shape
        self.mock_scaler.transform.return_value = np.zeros((1, 8))

    @patch('src.decision_logic.get_simulated_aqi', return_value=40)
    @patch('src.decision_logic.nn_model')
    @patch('src.decision_logic.scaler')
    @patch('src.decision_logic.mean_values', new_callable=lambda: np.zeros(8))
    def test_default_speed_limit(self, mock_means, mock_scaler, mock_model, mock_aqi):
        # Mock API to return NO for routing
        with patch('google.generativeai.GenerativeModel') as MockModel, \
             patch('google.generativeai.configure'):
            
            mock_router_model = MagicMock()
            mock_router_response = MagicMock()
            mock_router_response.text = "NO"
            mock_router_model.generate_content.return_value = mock_router_response
            MockModel.return_value = mock_router_model
            
            # Setup NN mock (should not be called if logic is correct, but safer to have)
            mock_model.predict.return_value = np.array([[0.1]])
            
            # We need to simulate the API key environment variable for the import inside function to try using genai
            with patch.dict(os.environ, {"GEMINI_API_KEY": "fake_key"}):
                speed_limit, reason = get_speed_limit(illuminance=1000, water_level=500, temperature=10, current_hour=12)
            
            self.assertEqual(speed_limit, 80)
            self.assertIn("Default speed limit", reason)

    @patch('src.decision_logic.get_simulated_aqi', return_value=40)
    @patch('src.decision_logic.nn_model')
    @patch('src.decision_logic.scaler')
    @patch('src.decision_logic.mean_values', new_callable=lambda: np.zeros(8))
    def test_darkness_reduction_with_api_router(self, mock_means, mock_scaler, mock_model, mock_aqi):
        # Mock API to return YES for routing
        with patch('google.generativeai.GenerativeModel') as MockModel, \
             patch('google.generativeai.configure'), \
             patch.dict(os.environ, {"GEMINI_API_KEY": "fake_key"}):
            
            mock_router_model = MagicMock()
            mock_router_response = MagicMock()
            mock_router_response.text = "YES"
            mock_router_model.generate_content.return_value = mock_router_response
            MockModel.return_value = mock_router_model

            # Configure NN mock to predict high risk
            mock_model.predict.return_value = np.array([[1.5]])
            
            # REQ1: Darkness
            speed_limit, reason = get_speed_limit(illuminance=100, water_level=500, temperature=10, current_hour=12)
            
            self.assertEqual(speed_limit, 60) # 80 - 20
            self.assertIn("Darkness", reason)
            self.assertIn("NN predicts", reason)
            
            # Verify router was called
            mock_router_model.generate_content.assert_called()
            # Verify NN was called
            mock_model.predict.assert_called_once()
            
    # ... (skipping unchanged tests) ...
    
    @patch('src.decision_logic.get_simulated_aqi', return_value=120)
    @patch('src.decision_logic.nn_model')
    @patch('src.decision_logic.scaler')
    @patch('src.decision_logic.mean_values', new_callable=lambda: np.zeros(8))
    def test_combined_darkness_and_air_quality(self, mock_means, mock_scaler, mock_model, mock_aqi):
        # Darkness (NN High Risk) + AQI High
        with patch('google.generativeai.GenerativeModel') as MockModel, \
             patch('google.generativeai.configure'), \
             patch('src.decision_logic.get_llm_speed_reduction_recommendation', return_value=20), \
             patch.dict(os.environ, {"GEMINI_API_KEY": "fake_key"}):
             
            mock_router_model = MagicMock()
            mock_router_response = MagicMock()
            mock_router_response.text = "YES"
            mock_router_model.generate_content.return_value = mock_router_response
            MockModel.return_value = mock_router_model

            mock_model.predict.return_value = np.array([[1.5]])
            
            speed_limit, reason = get_speed_limit(illuminance=100, water_level=500, temperature=10, current_hour=12)
            # Darkness -> 60. AQI 120 -> 60. Min is 60.
            self.assertEqual(speed_limit, 60)
            self.assertIn("Darkness", reason)
            self.assertIn("Poor air quality", reason)

if __name__ == '__main__':
    unittest.main()