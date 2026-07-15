import time
import pytest
from playwright.sync_api import sync_playwright

def test_subanta_page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        # Open Subanta generator page
        page.goto("http://127.0.0.1:8000/webclient_Subanta_Generate.html")

        # Select first option in the listbox
        page.select_option("#Dhatus", index=0)

        # Click the generate button
        page.click("#DhatusButton")

        # Wait for the table to contain elements
        page.wait_for_selector("#tbl tr td")

        # Verify declension table populated
        rows = page.query_selector_all("#tbl tr")
        assert len(rows) > 1, "Declension table should contain generated forms"

        browser.close()

def test_sentence_analysis_page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        # Open analysis page
        page.goto("http://127.0.0.1:8000/webclient_sentence_analyser.html")
        
        # Select the first sentence option
        page.select_option("#Dhatus", index=0)
        
        # Click Morphological Analysis button
        page.click("#btnMorphologicalAnalysis")
        
        # Wait for morphological analysis table to populate
        page.wait_for_selector("#sentenceAnalysis tr td")
        
        # Click Syntax Analysis button
        page.click("#btnSyntacticAnalysis")
        
        # Wait for syntactic interpretation/table to render
        page.wait_for_selector("#sentenceAnalysis tr td", timeout=5000)
        
        # Verify that Graphs button is enabled
        assert not page.is_disabled("#btnGraph"), "Graphs button should be enabled"
        
        browser.close()
