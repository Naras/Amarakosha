import os
import pytest
from playwright.sync_api import sync_playwright

def get_file_url(rel_path):
    abs_path = os.path.abspath(rel_path)
    return f"file://{abs_path}"

def test_subanta_page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Open Subanta generator page using local file URL
        page.goto(get_file_url("source/View/Webclient/webclient_Subanta_Generate.html"))

        # Wait for options and select first option in the listbox
        page.wait_for_selector("#Dhatus option", timeout=10000)
        page.select_option("#Dhatus", index=0)

        # Click the generate button
        page.click("#DhatusButton")

        # Wait for the table to contain elements
        page.wait_for_selector("#tbl tr td", timeout=10000)

        # Verify declension table populated
        rows = page.query_selector_all("#tbl tr")
        assert len(rows) > 1, "Declension table should contain generated forms"

        browser.close()

def test_sentence_analysis_page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Open analysis page using local file URL
        page.goto(get_file_url("source/View/Webclient/webclient_sentence_analyser.html"))
        
        # Wait for dropdown options to load from REST API
        page.wait_for_selector("#Dhatus option", timeout=10000)
        page.select_option("#Dhatus", index=0)
        
        # Click Morphological Analysis button
        page.click("#btnMorphologicalAnalysis")
        
        # Wait for morphological analysis table to populate
        page.wait_for_selector("#sentenceAnalysis tr td", timeout=10000)
        
        # Click Syntax Analysis button
        page.click("#btnSyntacticAnalysis")
        
        # Wait for syntactic interpretation/table to render
        page.wait_for_selector("#sentenceAnalysis tr td", timeout=10000)
        
        # Verify that Graphs button is enabled
        assert not page.is_disabled("#btnGraph"), "Graphs button should be enabled"
        
        # Select Page 6 interpretation button and verify semantic analysis card & report
        page.click('#pageButtons button:has-text("Page 6")')
        page.wait_for_selector("#semanticCard", state="visible", timeout=10000)
        
        badge = page.inner_text("#semanticStatusBadge")
        report = page.inner_text("#semanticReport")
        
        assert "COMPATIBLE" in badge.upper(), f"Unexpected status badge: {badge}"
        assert "Semantically Compatible" in report, f"Unexpected report content: {report}"
        
        browser.close()
