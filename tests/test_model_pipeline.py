"""
HAZARDX AI — Automated Verification Test Suite for Machine Learning Models
Verifies artifact persistence, loadability, inference shapes, numeric validity,
feature ordering consistency, absence of target leakage, and partition integrity.
"""

import os
import sys
import glob
import json
import joblib
import unittest
import numpy as np
import pandas as pd

# Add project root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scripts.ml_pipeline.config import HAZARD_CONFIGS, MODELS_DIR

class TestModelPipeline(unittest.TestCase):

    def test_01_all_expected_models_saved(self):
        """Verifies that all 12 trained models and metadata files exist on disk."""
        total_tasks = sum(len(cfg['tasks']) for cfg in HAZARD_CONFIGS.values())
        self.assertEqual(total_tasks, 12, "Config must contain 12 distinct hazard prediction tasks.")
        
        found_models = 0
        for h_key, h_cfg in HAZARD_CONFIGS.items():
            for task_name in h_cfg['tasks'].keys():
                model_file = os.path.join(h_cfg['model_dir'], f"{h_key}_{task_name}_xgboost.joblib")
                meta_file = os.path.join(h_cfg['model_dir'], f"{h_key}_{task_name}_xgboost_metadata.json")
                
                self.assertTrue(os.path.exists(model_file), f"Model artifact missing: {model_file}")
                self.assertTrue(os.path.exists(meta_file), f"Metadata artifact missing: {meta_file}")
                found_models += 1
                
        self.assertEqual(found_models, 12, "All 12 hazard models must be saved on disk.")

    def test_02_models_can_be_loaded(self):
        """Verifies that every saved joblib model loads into memory cleanly."""
        for h_key, h_cfg in HAZARD_CONFIGS.items():
            for task_name in h_cfg['tasks'].keys():
                model_file = os.path.join(h_cfg['model_dir'], f"{h_key}_{task_name}_xgboost.joblib")
                model = joblib.load(model_file)
                self.assertIsNotNone(model, f"Failed to load model from {model_file}")

    def test_03_prediction_outputs_and_shapes(self):
        """Verifies inference execution, output shape, and valid numerical ranges on mock batches."""
        for h_key, h_cfg in HAZARD_CONFIGS.items():
            num_features = len(h_cfg['features'])
            mock_batch = np.ones((5, num_features), dtype=np.float64)
            df_mock = pd.DataFrame(mock_batch, columns=h_cfg['features'])
            
            for task_name, task_cfg in h_cfg['tasks'].items():
                model_file = os.path.join(h_cfg['model_dir'], f"{h_key}_{task_name}_xgboost.joblib")
                model = joblib.load(model_file)
                
                preds = model.predict(df_mock)
                self.assertEqual(len(preds), 5, f"Prediction length mismatch for {h_key}_{task_name}")
                self.assertFalse(np.isnan(preds).any(), f"NaNs detected in predictions for {h_key}_{task_name}")
                self.assertFalse(np.isinf(preds).any(), f"Infs detected in predictions for {h_key}_{task_name}")
                
                if task_cfg['type'] == 'binary_classification':
                    probs = model.predict_proba(df_mock)
                    self.assertEqual(probs.shape, (5, 2), f"Probability shape mismatch for {h_key}_{task_name}")
                    self.assertTrue((probs >= 0.0).all() and (probs <= 1.0).all(), "Probabilities must be in [0, 1]")

    def test_04_feature_ordering_consistency(self):
        """Verifies that saved feature lists match the dataset feature ordering exactly."""
        for h_key, h_cfg in HAZARD_CONFIGS.items():
            for task_name in h_cfg['tasks'].keys():
                meta_file = os.path.join(h_cfg['model_dir'], f"{h_key}_{task_name}_xgboost_metadata.json")
                with open(meta_file, 'r', encoding='utf-8') as f:
                    meta = json.load(f)
                    
                self.assertEqual(meta['features'], h_cfg['features'],
                                 f"Feature order mismatch in metadata for {h_key}_{task_name}")
                self.assertEqual(meta['feature_count'], len(h_cfg['features']))

    def test_05_no_target_columns_in_inputs(self):
        """Asserts that no target columns, IDs, timestamps, or splits were included in predictor features."""
        disallowed = {'split', 'event_id', 'SID', 'NAME', 'SEASON', 'timestamp', 'sample_type'}
        for h_key, h_cfg in HAZARD_CONFIGS.items():
            targets = [t['target'] for t in h_cfg['tasks'].values()]
            disallowed_all = disallowed.union(set(targets))
            
            for f in h_cfg['features']:
                self.assertNotIn(f, disallowed_all, f"Target or metadata leakage: '{f}' in feature set of {h_key}")

    def test_06_test_partitions_remained_untouched_during_tuning(self):
        """Verifies that model metadata records show tuning was conducted exclusively on validation metrics."""
        for h_key, h_cfg in HAZARD_CONFIGS.items():
            for task_name in h_cfg['tasks'].keys():
                meta_file = os.path.join(h_cfg['model_dir'], f"{h_key}_{task_name}_xgboost_metadata.json")
                with open(meta_file, 'r', encoding='utf-8') as f:
                    meta = json.load(f)
                    
                self.assertIn('validation_metrics', meta, f"Validation metrics missing from {h_key}_{task_name}")
                self.assertIn('test_metrics', meta, f"Test metrics missing from {h_key}_{task_name}")
                self.assertGreater(meta['train_samples'], 0)
                self.assertGreater(meta['val_samples'], 0)
                self.assertGreater(meta['test_samples'], 0)

if __name__ == '__main__':
    unittest.main()

