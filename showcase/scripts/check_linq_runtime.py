#!/usr/bin/env python3
"""Run the LINQ Reporting examples against the real Aspose.Words for Java jar.

Compilation does not check LINQ Reporting templates: ReportingEngine parses the <<...>> tags
when the program runs. This script runs every linq-reporting answer of a showcase run and the
J1/J9 examples of examples/error-correction.md:

- it builds the template the answer describes (from its text block or the inline template it names);
- it compiles the answer's Java code verbatim with the showcase compiler settings and runs it,
  or, for a template given only in prose, runs it with a JsonDataSource holding matching data;
- it reads the produced document and checks that no tags remain and the expected values appear.
The J9 WRONG example must fail at run time and the RIGHT one must pass.

  python showcase/scripts/check_linq_runtime.py [--showcase <showcase.md>] [--jar <jar>]

Writes the report next to the showcase (linq-runtime-check.md) and keeps every case's files
under showcase/runs/linq-check/ (ignored by Git).
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
FENCE = re.compile(r'^```(\w*)[ \t]*\n(.*?)^```[ \t]*$', re.M | re.S)
PUBLIC_CLASS = re.compile(r'^public\s+(?:final\s+)?class\s+(\w+)', re.M)
LINT = ['--release', '17', '-Xlint:deprecation,removal,unchecked,rawtypes', '-Werror', '-encoding', 'UTF-8']

# Templates are taken from the answer's text block or copied verbatim from the inline template it names.
CASES = [
    {'id': 'linq-reporting-01', 'mode': 'json', 'template': 'text-block',
     'data': {'Customer': {'IsActive': True, 'Name': 'Ann'},
              'Orders': [{'Name': 'Pen', 'Price': 5}, {'Name': 'Book', 'Price': 12}]},
     'expect': ['Hello, Ann', 'Pen', 'Book'], 'absent': ['inactive']},
    {'id': 'linq-reporting-02', 'mode': 'code', 'expect': ['Hello Avery!']},
    {'id': 'linq-reporting-03', 'mode': 'code',
     'template': '<<[sender.getName()]>> says: “<<[sender.getMessage()]>>”',
     'expect': ['Aspose says: “Hello World”']},
    {'id': 'linq-reporting-04', 'mode': 'code', 'template': 'Hello, <<[sender.getName()]>>!',
     'expect': ['Hello, Avery!']},
    {'id': 'linq-reporting-05', 'mode': 'code', 'template': 'text-block',
     'expect': ['Notebook', '150'], 'absent': ['Pen']},
    {'id': 'linq-reporting-06', 'mode': 'json', 'template': 'text-block', 'name': 'orders',
     'data': [{'Id': 1, 'Total': 150, 'Items': [{'Name': 'Laptop'}]},
              {'Id': 2, 'Total': 40, 'Items': [{'Name': 'Mouse'}, {'Name': 'Cable'}]}],
     'expect': ['Order: 1', 'Order: 2', 'Eligible for a discount.', 'Standard pricing.', 'Laptop', 'Cable']},
    {'id': 'linq-reporting-07', 'mode': 'code', 'template': '<<[Name]>>',
     'runs': [{'data_file': 'data.json', 'data': '{"Name": "Aspose JSON"}', 'expect': ['Aspose JSON']},
              {'data_file': 'data.xml', 'data': '<root><Name>Aspose XML</Name></root>', 'expect': ['Aspose XML']}]},
    {'id': 'linq-reporting-08', 'mode': 'none'},
]


def run(command, cwd, timeout=180):
    try:
        done = subprocess.run(command, cwd=cwd, capture_output=True, text=True,
                              encoding='utf-8', errors='replace', timeout=timeout)
        output = '\n'.join(l for l in (done.stdout + '\n' + done.stderr).splitlines()
                           if not l.startswith('Picked up '))
        return done.returncode, output.strip()
    except subprocess.TimeoutExpired:
        return None, f'timed out after {timeout} s'


def default_jar():
    override = os.environ.get('ASPOSE_WORDS_JAR')
    if override:
        return Path(override)
    return (Path.home()/'.m2'/'repository'/'com'/'aspose'/'aspose-words'/'26.10'/
            'aspose-words-26.10-jdk17.jar')


def sections(text):
    found = {}
    for part in re.split(r'(?=<a id="[^"]+"></a>)', text):
        m = re.match(r'<a id="([^"]+)"></a>', part)
        if m:
            found[m.group(1)] = part
    return found


def rule_cases(rules_text):
    """J1 and J9 examples from error-correction.md, with the template each one needs."""
    cases = []
    j1 = rules_text.split('### J1', 1)[1].split('### J2', 1)[0]
    right = [b for lang, b in FENCE.findall(j1) if lang == 'java' and b.lstrip().startswith('// RIGHT')]
    if right:
        cases.append({'id': 'rule-J1-right', 'question': 'error-correction.md J1 RIGHT example', 'mode': 'code',
                      'code': right[0], 'template': '<<[sender.getName()]>>: <<[sender.getMessage()]>>',
                      'expect': ['Aspose: Hello']})
    j9 = rules_text.split('### J9', 1)[1].split('## Before you answer', 1)[0]
    blocks = FENCE.findall(j9)
    texts = [b.rstrip('\n') for lang, b in blocks if lang == 'text']
    javas = [b for lang, b in blocks if lang == 'java']
    if len(texts) == 2 and len(javas) == 2:
        cases.append({'id': 'rule-J9-wrong', 'question': 'error-correction.md J9 WRONG example (must fail at run time)',
                      'mode': 'code', 'code': javas[0], 'template': texts[0], 'expect': ['Notebook'],
                      'expect_failure': True})
        cases.append({'id': 'rule-J9-right', 'question': 'error-correction.md J9 RIGHT example',
                      'mode': 'code', 'code': javas[1], 'template': texts[1], 'expect': ['Notebook', '150']})
    return cases


class Runner:
    def __init__(self, jar, work):
        self.jar, self.work = jar, work
        self.tools = work/'_harness'
        self.tools.mkdir(parents=True, exist_ok=True)
        code, text = run(['javac', '--release', '17', '-encoding', 'UTF-8', '-cp', str(jar), '-d', str(self.tools),
                          str(HERE/'LinqHarness.java')], self.tools)
        if code != 0:
            sys.exit('Cannot compile LinqHarness.java:\n' + text)

    def cp(self, *extra):
        return os.pathsep.join([str(self.jar), *map(str, extra)])

    def harness(self, cwd, *args):
        return run(['java', '-cp', self.cp(self.tools), 'LinqHarness', *map(str, args)], cwd)

    def make_template(self, folder, text):
        (folder/'template.txt').write_text(text, encoding='utf-8')
        return self.harness(folder, 'template', folder/'template.docx', folder/'template.txt')

    def doc_text(self, folder, name):
        if not (folder/name).is_file():
            return None
        code, text = self.harness(folder, 'text', folder/name)
        return text if code == 0 else None


def check_output(text, expect, absent):
    if text is None:
        return ['no output document was produced']
    problems = ['template tags remain in the output'] if '<<' in text else []
    problems += [f'missing "{e}"' for e in expect if e not in text]
    problems += [f'unexpected "{a}"' for a in absent if a in text]
    return problems


def first_error(text):
    return next((l.strip() for l in text.splitlines() if 'Exception' in l or 'error' in l.lower()), '')[:200]


def run_case(runner, case, body, folder):
    """Return (status, note, log lines)."""
    log = []
    java = [b for lang, b in FENCE.findall(body) if lang == 'java']
    blocks = [b for lang, b in FENCE.findall(body) if lang == 'text']
    template = case.get('template')
    if template == 'text-block':
        template = blocks[0].rstrip('\n') if blocks else None
    if template:
        code, text = runner.make_template(folder, template)
        log += ['Template:', '', '```text', template, '```', '']
        if code != 0:
            return 'error', 'could not create the template', log + ['```text', text, '```', '']
    outcomes = []
    if case['mode'] == 'json':
        (folder/'data.json').write_text(json.dumps(case['data'], indent=2), encoding='utf-8')
        args = ['json', folder/'template.docx', folder/'data.json', folder/'report.docx']
        args += [case['name']] if case.get('name') else []
        code, text = runner.harness(folder, *args)
        name = f'"{case["name"]}"' if case.get('name') else 'no name'
        log += [f'Run: `ReportingEngine.buildReport` with a `JsonDataSource` ({name}):', '',
                '```json', json.dumps(case['data'], indent=2), '```', '']
        outcomes.append((code, text, 'report.docx', case.get('expect', []), case.get('absent', [])))
    else:
        source = case.get('code') or (java[0] if java else None)
        if not source:
            return 'error', 'no java block', log
        cls = (PUBLIC_CLASS.search(source) or [None, 'Example'])[1]
        (folder/f'{cls}.java').write_text(source, encoding='utf-8')
        code, text = run(['javac', *LINT, '-cp', runner.cp(), '-d', str(folder/'classes'), str(folder/f'{cls}.java')], folder)
        if code != 0:
            return 'fail', 'does not compile', log + ['Compilation failed:', '', '```text', text, '```', '']
        for spec in case.get('runs') or [{}]:
            argv, output = [], 'report.docx'
            if spec.get('data_file'):
                (folder/spec['data_file']).write_text(spec['data'], encoding='utf-8')
                output = 'report-' + spec['data_file'].split('.')[1] + '.docx'
                argv = ['template.docx', spec['data_file'], output]
                log += [f'Data `{spec["data_file"]}`: `{spec["data"]}`', '']
            code, text = run(['java', '-cp', runner.cp(folder/'classes'), cls, *argv], folder)
            log += [f'Run: `java {cls} {" ".join(argv)}`'.rstrip(), '']
            outcomes.append((code, text, output, spec.get('expect', case.get('expect', [])),
                             spec.get('absent', case.get('absent', []))))
    problems, errors = [], []
    for code, text, output, expect, absent in outcomes:
        produced = runner.doc_text(folder, output) if code == 0 else None
        found = [f'exited with code {code}'] if code != 0 else check_output(produced, expect, absent)
        problems += found
        if code != 0:
            errors.append(first_error(text))
        if text:
            log += ['Console output:', '', '```text', text[-2500:], '```', '']
        if produced is not None:
            shown = '\n'.join(l for l in produced.replace('\r', '\n').splitlines()
                              if l.strip() and 'valuation' not in l)
            log += [f'Text of `{output}` (evaluation notices removed):', '', '```text', shown[-1500:], '```', '']
    if case.get('expect_failure'):
        if problems:
            return 'passed', 'fails at run time as the rule says: ' + '; '.join(e for e in errors if e), log
        return 'fail', 'expected a run-time failure, but it ran', log
    if problems:
        return 'fail', '; '.join(problems) + (f' ({errors[0]})' if errors and errors[0] else ''), log
    return 'passed', 'output contains the expected values', log


def main():
    p = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    p.add_argument('--showcase', type=Path, default=ROOT/'showcase'/'runs'/'published-01'/'showcase.md')
    p.add_argument('--rules', type=Path, default=ROOT/'examples'/'error-correction.md')
    p.add_argument('--jar', type=Path, default=default_jar())
    p.add_argument('--work', type=Path, default=ROOT/'showcase'/'runs'/'linq-check')
    p.add_argument('--report', type=Path, help='default: linq-runtime-check.md next to the showcase')
    a = p.parse_args()
    if not a.jar.is_file():
        sys.exit(f'Jar not found: {a.jar} (run `mvn -B -q compile` in examples/ or set ASPOSE_WORDS_JAR)')
    for tool in ('javac', 'java'):
        if not shutil.which(tool):
            sys.exit(f'{tool} is not on PATH')
    report_path = a.report or a.showcase.with_name('linq-runtime-check.md')
    answers = sections(a.showcase.read_text(encoding='utf-8'))
    work = a.work.resolve()
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)
    runner = Runner(a.jar.resolve(), work)
    cases = [dict(c, question=(re.search(r'^### (.+)$', answers.get(c['id'], ''), re.M) or [None, '?'])[1])
             for c in CASES] + rule_cases(a.rules.read_text(encoding='utf-8'))
    rows, details = [], []
    for case in cases:
        folder = work/case['id']
        folder.mkdir()
        if case['mode'] == 'none':
            status, note, log = 'not applicable', 'comparison only; no template or code to run', []
        else:
            status, note, log = run_case(runner, case, answers.get(case['id'], ''), folder)
        rows.append((case['id'], status, note))
        details += [f'## {case["id"]}: {case["question"]}', '', *log, f'Result: **{status}**: {note}', '']
        print(case['id'], status, '' if status == 'passed' else note, flush=True)

    java_version = run(['java', '-version'], work)[1].splitlines()[0]
    try:
        shown = a.showcase.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        shown = a.showcase.name
    report = ['# LINQ Reporting runtime check', '',
              f'Showcase: `{shown}` · rules: `examples/error-correction.md` (J1, J9) · '
              f'jar: `{a.jar.name}` · Java: `{java_version}`', '',
              'Compilation does not check LINQ Reporting templates; `ReportingEngine` parses them at run time. '
              'Each case below builds the template the answer describes, runs the answer\'s Java code (or, for a '
              'template given only in prose, a `JsonDataSource` with matching data) and checks the generated '
              'document: no tags left and the expected values present. Without a license, Aspose.Words adds '
              'evaluation notices to the output; they are ignored. Generated with '
              '`python showcase/scripts/check_linq_runtime.py`.', '',
              '| Case | Result | Notes |', '| --- | --- | --- |']
    report += [f'| {c} | {s} | {n.replace("|", "/")} |' for c, s, n in rows]
    report += ['', *details]
    report_path.write_text('\n'.join(report).rstrip() + '\n', encoding='utf-8')
    print(f'\nReport: {report_path.resolve()}')
    if any(s in ('fail', 'error') for _, s, _ in rows):
        sys.exit(1)


if __name__ == '__main__':
    main()
