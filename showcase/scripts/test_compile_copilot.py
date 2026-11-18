"""Tests for bounded repair, preservation of failed answers, and javac classification."""
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch
from compile_copilot import verify_and_repair, compile_answer, tool_urls, class_name

ORIGINAL = 'Example [docs](https://example.com/api)\n```java\nbroken\n```'
FIXED = ORIGINAL.replace('broken', 'fixed')


class RepairTests(unittest.TestCase):
    def check_flow(self, states, candidates, budget=2):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        calls = []
        def repair(prompt, folder):
            calls.append(prompt)
            return {'execution_status': 'completed', 'recorded_answer_markdown': candidates[len(calls)-1]}
        with patch('compile_copilot.compile_answer', side_effect=[{'status': s} for s in states]):
            answer, record = verify_and_repair('question', ORIGINAL, root, '26.10', '17', 120, budget, repair)
        return answer, record, calls

    def test_repair_passes(self):
        answer, record, calls = self.check_flow(['failed', 'passed'], [FIXED])
        self.assertEqual(answer, FIXED)
        self.assertTrue(record['accepted'])
        self.assertEqual(len(calls), 1)
        self.assertIn('Java release 17', calls[0])

    def test_exhausted_retains_original(self):
        answer, record, calls = self.check_flow(['failed', 'failed', 'failed'], [FIXED, FIXED+'\nChanged'])
        self.assertEqual(answer, ORIGINAL)
        self.assertFalse(record['accepted'])
        self.assertEqual(len(calls), 2)

    def test_unchanged_stops(self):
        _, record, calls = self.check_flow(['failed'], [ORIGINAL])
        self.assertEqual(record['attempts'][-1]['disposition'], 'unchanged_answer')
        self.assertEqual(len(calls), 1)

    def test_citations_and_removed_code_rejected(self):
        _, record, calls = self.check_flow(['failed'], [FIXED+' https://invented.example/api', 'https://example.com/api'])
        self.assertEqual([a['disposition'] for a in record['attempts']], ['initial', 'citation_rejected', 'code_removed'])
        self.assertEqual(len(calls), 2)

    def test_infrastructure_and_no_code_do_not_repair(self):
        for state in ['unavailable', 'timeout', 'no_code', 'passed']:
            _, record, calls = self.check_flow([state], [])
            self.assertEqual(calls, [])
            self.assertEqual(record['status'], state)

    def test_zero_budget(self):
        _, record, calls = self.check_flow(['failed'], [], budget=0)
        self.assertEqual(calls, [])
        self.assertEqual(record['status'], 'failed')

    def test_no_code(self):
        with tempfile.TemporaryDirectory() as folder:
            self.assertEqual(compile_answer('Explanation only', Path(folder))['status'], 'no_code')

    def test_csharp_block_is_not_java(self):
        with tempfile.TemporaryDirectory() as folder:
            answer = '```csharp\nvar doc = new Document("a.docx");\n```'
            self.assertEqual(compile_answer(answer, Path(folder))['status'], 'no_code')

    def test_only_words_java_urls(self):
        events = []
        for server in ['words-java', 'shell']:
            events += [{'type': 'tool.execution_start', 'data': {'toolCallId': server, 'mcpServerName': server}},
                       {'type': 'tool.execution_complete', 'data': {'toolCallId': server, 'success': True, 'result': 'https://example.com/'+server}}]
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)/'events.jsonl'
            path.write_text('\n'.join(json.dumps(e) for e in events), encoding='utf-8')
            self.assertEqual(tool_urls(path), {'https://example.com/words-java'})


class ClassNameTests(unittest.TestCase):
    def test_public_class_names_file(self):
        self.assertEqual(class_name('import x.Y;\n\npublic class ConvertToPdf {\n}\nclass Helper {}'), 'ConvertToPdf')
        self.assertEqual(class_name('public final class Report {}'), 'Report')
        self.assertEqual(class_name('// public class Comment {}\nclass Plain {}'), 'Plain')
        self.assertEqual(class_name('Document doc = null;'), 'Example')


class ToolchainTests(unittest.TestCase):
    def test_missing_javac_is_unavailable(self):
        with tempfile.TemporaryDirectory() as folder, patch('compile_copilot.shutil.which', return_value=None), \
             patch('compile_copilot.run_logged') as build:
            result = compile_answer(FIXED, Path(folder))
            self.assertEqual(result['status'], 'unavailable')
            self.assertIn('javac', result['reason'])
            build.assert_not_called()

    def test_missing_jar_is_unavailable(self):
        with tempfile.TemporaryDirectory() as folder, \
             patch('compile_copilot.shutil.which', return_value='/fake/javac'), \
             patch('compile_copilot.run_logged') as build:
            result = compile_answer(FIXED, Path(folder), jar=Path(folder)/'missing.jar')
            self.assertEqual(result['status'], 'unavailable')
            self.assertIn('mvn', result['reason'])
            build.assert_not_called()

    def test_unsupported_release_does_not_trigger_repair(self):
        def build(command, cwd, stdout, stderr, timeout):
            stdout.write_text('', encoding='utf-8')
            stderr.write_text('error: release version 25 not supported\nUsage: javac <options> <source files>', encoding='utf-8')
            return {'status': 'failed', 'exit_code': 2}
        with tempfile.TemporaryDirectory() as folder:
            jar = Path(folder)/'aspose-words.jar'
            jar.write_bytes(b'')
            with patch('compile_copilot.shutil.which', return_value='/fake/javac'), \
                 patch('compile_copilot.run_logged', side_effect=build):
                def repair(*args):
                    self.fail('A toolchain failure must not request model repair')
                _, result = verify_and_repair('Question', FIXED, Path(folder)/'out', '26.10', '25', 120, 2, repair, jar)
                self.assertEqual(result['status'], 'unavailable')


@unittest.skipUnless(shutil.which('javac'), 'javac is not installed')
class JavacIntegrationTests(unittest.TestCase):
    """Compile real blocks against a two-class stub of com.aspose.words (no network, no Aspose jar)."""

    @classmethod
    def setUpClass(cls):
        cls.temporary = tempfile.TemporaryDirectory()
        root = Path(cls.temporary.name)
        package = root/'stub'/'com'/'aspose'/'words'
        package.mkdir(parents=True)
        (package/'Document.java').write_text(
            'package com.aspose.words;\npublic class Document {\n'
            '  public Document(String path) throws Exception {}\n'
            '  public void save(String path) throws Exception {}\n}\n', encoding='utf-8')
        (package/'List.java').write_text('package com.aspose.words;\npublic class List {}\n', encoding='utf-8')
        classes = root/'classes'
        subprocess.run(['javac', '-d', str(classes), str(package/'Document.java'), str(package/'List.java')],
                       check=True, capture_output=True)
        cls.jar = root/'aspose-words-stub.jar'
        subprocess.run(['jar', 'cf', str(cls.jar), '-C', str(classes), '.'], check=True, capture_output=True)

    @classmethod
    def tearDownClass(cls):
        cls.temporary.cleanup()

    def compile(self, code):
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        return compile_answer(f'Answer\n```java\n{code}```\n', Path(folder.name), jar=self.jar)

    def test_program_passes(self):
        result = self.compile('import com.aspose.words.Document;\n\npublic class ConvertToPdf {\n'
                              '    public static void main(String[] args) throws Exception {\n'
                              '        new Document("in.docx").save("out.pdf");\n    }\n}\n')
        self.assertEqual(result['status'], 'passed', result)
        self.assertEqual(result['results'][0]['source_file'], 'ConvertToPdf.java')

    def test_compiler_error_is_failed_with_key(self):
        result = self.compile('import com.aspose.words.*;\nimport java.util.*;\n\npublic class Names {\n'
                              '    public static void main(String[] args) throws Exception {\n'
                              '        List<String> names = new ArrayList<>();\n    }\n}\n')
        self.assertEqual(result['status'], 'failed')
        self.assertIn('compiler.err.ref.ambiguous', result['results'][0]['diagnostic_codes'])

    def test_warning_fails_build(self):
        result = self.compile('import java.util.ArrayList;\nimport java.util.List;\n\npublic class Raw {\n'
                              '    public static void main(String[] args) throws Exception {\n'
                              '        List values = new ArrayList();\n        System.out.println(values);\n    }\n}\n')
        self.assertEqual(result['status'], 'failed')
        self.assertIn('compiler.warn.raw.class.use', result['results'][0]['diagnostic_codes'])

    def test_library_block_without_main_fails(self):
        result = self.compile('public class Helper {\n    public static void run() {}\n}\n')
        self.assertEqual(result['status'], 'failed')
        self.assertEqual(result['results'][0]['diagnostic_codes'], ['missing-main'])

    def test_each_block_independent(self):
        first = ('import com.aspose.words.Document;\n\npublic class First {\n'
                 '    public static void main(String[] args) throws Exception {\n'
                 '        Document doc = new Document("in.docx");\n        doc.save("a.pdf");\n    }\n}\n')
        second = ('public class Second {\n    public static void main(String[] args) throws Exception {\n'
                  '        doc.save("b.pdf");\n    }\n}\n')
        with tempfile.TemporaryDirectory() as folder:
            result = compile_answer(f'```java\n{first}```\n\n```java\n{second}```\n', Path(folder), jar=self.jar)
        self.assertEqual([r['status'] for r in result['results']], ['passed', 'failed'])
        self.assertEqual(result['status'], 'failed')


if __name__ == '__main__':
    unittest.main()
