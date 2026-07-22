#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import re
import os
import sys

sys.path.insert(0, os.getcwd())
from source.Controller.restService import analysis


class TestSemanticAnalysis(unittest.TestCase):
    """
    Abstract, regex-based unit tests for Sanskrit sentence semantic analysis.
    Tests core sentences like 'रामः गच्छति', 'कमले नृत्यत', and 'कमले नृत्यतः'.
    """

    # Abstract regex patterns for semantic report validation
    COMPATIBLE_PATTERN = re.compile(
        r"The (Sentence|Verb|Krdanta) is Semantically Compatible", re.IGNORECASE
    )
    INCOMPATIBLE_OR_VOCATIVE_PATTERN = re.compile(
        r"Vocative|Incompatible|Not handled|not compatible", re.IGNORECASE
    )
    ERROR_PATTERN = re.compile(
        r"NoneType|AttributeError|TypeError|Failed:", re.IGNORECASE
    )

    def test_semantic_analysis_core_sentences(self):
        test_sentences = [
            "रामः गच्छति",
            "रामः गच्छति । ",
            "कमले नृत्यत",
            "कमले नृत्यतः । ",
            "कमलानि पश्यति",
            "जनाः वदन्ति"
        ]

        for sentence in test_sentences:
            with self.subTest(sentence=sentence):
                res = analysis(sentence, "devanagari")
                self.assertIn("syntactic", res)
                self.assertIn("interpretations", res["syntactic"])

                interpretations = res["syntactic"]["interpretations"]
                self.assertGreater(
                    len(interpretations),
                    0,
                    f"Sentence '{sentence}' should yield at least 1 interpretation",
                )

                has_at_least_one_evaluated = False
                has_at_least_one_compatible = False

                for idx, interp in enumerate(interpretations):
                    self.assertIn("semantic", interp)
                    sem = interp["semantic"]

                    self.assertIn("evaluated", sem)
                    self.assertIn("compatible", sem)
                    self.assertIn("report", sem)

                    report_text = " ".join(sem["report"])

                    # Ensure no exception leak in report strings
                    self.assertFalse(
                        self.ERROR_PATTERN.search(report_text),
                        f"Exception trace found in report for '{sentence}' (Page {idx+1}): {report_text}",
                    )

                    if sem["evaluated"]:
                        has_at_least_one_evaluated = True

                    if sem["compatible"]:
                        has_at_least_one_compatible = True
                        self.assertTrue(
                            self.COMPATIBLE_PATTERN.search(report_text),
                            f"Compatible interpretation missing matching pattern for '{sentence}' (Page {idx+1}): {report_text}",
                        )
                    elif sem["evaluated"]:
                        self.assertTrue(
                            self.INCOMPATIBLE_OR_VOCATIVE_PATTERN.search(report_text),
                            f"Evaluated incompatible interpretation missing pattern for '{sentence}' (Page {idx+1}): {report_text}",
                        )

                self.assertTrue(
                    has_at_least_one_evaluated,
                    f"Sentence '{sentence}' should have at least 1 semantically evaluated page",
                )
                self.assertTrue(
                    has_at_least_one_compatible,
                    f"Valid sentence '{sentence}' should have at least 1 semantically compatible interpretation",
                )


if __name__ == "__main__":
    unittest.main()
