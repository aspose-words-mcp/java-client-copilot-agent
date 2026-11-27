"""Offline tests for the LINQ Reporting runtime check (no JDK or Aspose jar needed)."""
import unittest
from check_linq_runtime import ROOT, CASES, check_output, rule_cases, sections


class LinqRuntimeCheckTests(unittest.TestCase):
    def test_rule_examples_found(self):
        text = (ROOT/'examples'/'error-correction.md').read_text(encoding='utf-8')
        cases = {c['id']: c for c in rule_cases(text)}
        self.assertEqual(sorted(cases), ['rule-J1-right', 'rule-J9-right', 'rule-J9-wrong'])
        self.assertTrue(cases['rule-J9-wrong']['expect_failure'])
        self.assertIn('<<end>>', cases['rule-J9-wrong']['template'])
        self.assertIn('where(', cases['rule-J9-right']['template'])
        self.assertIn('public static class Sender', cases['rule-J1-right']['code'])

    def test_every_linq_question_has_a_case(self):
        showcase = ROOT/'showcase'/'runs'/'published-01'/'showcase.md'
        if not showcase.is_file():
            self.skipTest('no published run')
        linq = {k for k in sections(showcase.read_text(encoding='utf-8')) if k.startswith('linq-reporting-')}
        self.assertEqual(linq, {c['id'] for c in CASES})

    def test_output_checks(self):
        self.assertEqual(check_output('Hello, Ann', ['Hello, Ann'], []), [])
        self.assertIn('template tags remain in the output', check_output('<<[x]>>', [], []))
        self.assertEqual(check_output('Pen', [], ['Pen']), ['unexpected "Pen"'])
        self.assertEqual(check_output(None, ['x'], []), ['no output document was produced'])


if __name__ == '__main__':
    unittest.main()
