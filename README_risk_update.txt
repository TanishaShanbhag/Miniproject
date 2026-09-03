Risk output update summary:
- Backend now returns prediction, risk_type, risk_percent.
- Risk percent uses model.predict_proba if available; else falls back to 75%/25%.
- Check: Could not load model: No module named 'numpy._core'
