"""
test_pii.py  –  Unit tests for the Presidio PII module.

Run with:
    python -m pytest tests/ -v
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.pii.presidio_custom import analyze_pii


def test_email_detected():
    result = analyze_pii("My email is ali.khan@example.com please contact me.")
    types = [e["type"] for e in result["entities"]]
    assert "EMAIL_ADDRESS" in types
    assert result["has_pii"] is True
    assert "<EMAIL>" in result["masked_text"]

def test_cnic_detected():
    result = analyze_pii("My CNIC is 35202-1234567-1 for verification.")
    types = [e["type"] for e in result["entities"]]
    assert "CNIC" in types
    assert "<CNIC>" in result["masked_text"]

def test_student_id_detected():
    result = analyze_pii("My student ID is FA21-BCS-123 from COMSATS.")
    types = [e["type"] for e in result["entities"]]
    assert "STUDENT_ID" in types
    assert "<STUDENT_ID>" in result["masked_text"]

def test_phone_detected():
    result = analyze_pii("Call me at 03001234567 anytime.")
    assert result["has_pii"] is True

def test_api_key_detected():
    result = analyze_pii("My API key is sk-proj-xKzD1qW2mNp8vLr3hJyU5oAeB7cFtG9 keep it safe.")
    types = [e["type"] for e in result["entities"]]
    assert "API_KEY" in types
    assert result["has_secret"] is True

def test_benign_no_pii():
    result = analyze_pii("Explain supervised learning with one example.")
    assert result["has_pii"] is False
    assert result["entities"] == []
    assert result["pii_risk"] == 0.0

def test_composite_pii():
    result = analyze_pii("Student FA21-BCS-123 email is student@example.com.")
    types = [e["type"] for e in result["entities"]]
    assert "STUDENT_ID" in types
    assert "EMAIL_ADDRESS" in types

def test_masked_text_original_unchanged():
    original = "My CNIC is 35202-1234567-1."
    result = analyze_pii(original)
    # Original text must not be modified
    assert original == "My CNIC is 35202-1234567-1."
    # Masked text must differ
    assert result["masked_text"] != original
