"""Approval freshness and self-contained submission tables; compile when TeX exists."""
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import common
from table_export import table_document


class ApprovalTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.paper = self.root / 'papers/example'
        self.paper.mkdir(parents=True)
        (self.paper / 'main.tex').write_text('Reviewed manuscript')
        self.meta = {'papers': [{'authors': [{'name': 'Author', 'manuscript_approval': {
            'status': 'pending', 'approved_source_commit': None}}]}]}
        self.save()
        self.git('init', '-q')
        self.git('config', 'user.name', 'Test')
        self.git('config', 'user.email', 'test@example.invalid')
        self.git('add', '.')
        self.git('commit', '-qm', 'Reviewed sources')
        self.revision = self.git('rev-parse', 'HEAD').strip()
        root_patch = patch.object(common, 'ROOT', self.root)
        root_patch.start()
        self.addCleanup(root_patch.stop)

    def git(self, *args):
        return subprocess.check_output(['git', *args], cwd=self.root, text=True)

    def save(self):
        (self.root / 'papers.json').write_text(json.dumps(self.meta))

    def approve(self):
        self.meta['papers'][0]['authors'][0]['manuscript_approval'] = {
            'status': 'approved', 'approved_source_commit': self.revision}
        self.save()

    def errors(self):
        return common.approval_errors(self.meta['papers'][0], self.paper)

    def test_pending_and_missing_commit_rejected(self):
        self.assertIn('approval pending', self.errors()[0])
        self.approve()
        self.meta['papers'][0]['authors'][0]['manuscript_approval']['approved_source_commit'] = None
        self.assertIn('full source commit SHA', self.errors()[0])

    def test_recording_approval_does_not_invalidate_it(self):
        self.approve()
        self.assertEqual(self.errors(), [])
        self.git('add', 'papers.json')
        self.git('commit', '-qm', 'Record approval')
        self.assertEqual(self.errors(), [])

    def test_changed_or_deleted_source_invalidates_approval(self):
        self.approve()
        (self.paper / 'main.tex').write_text('Changed manuscript')
        self.assertIn('sources changed', self.errors()[0])
        (self.paper / 'main.tex').unlink()
        self.assertIn('sources changed', self.errors()[0])

    def test_metadata_changes_invalidate_approval(self):
        self.approve()
        self.meta['papers'][0]['title'] = 'New title'
        self.save()
        self.assertIn('sources changed', self.errors()[0])

    def test_untracked_source_invalidates_approval(self):
        self.approve()
        (self.paper / 'new.tex').write_text('New source')
        self.assertIn('sources changed', self.errors()[0])

    def test_unknown_commit_rejected(self):
        self.approve()
        self.meta['papers'][0]['authors'][0]['manuscript_approval']['approved_source_commit'] = 'f' * 40
        self.assertIn('not in current history', self.errors()[0])


class TableTests(unittest.TestCase):
    def test_citations_keep_manuscript_numbers(self):
        manuscript = (r'\begin{thebibliography}{99}\bibitem{first}First.'
            r'\bibitem{second}Second.\bibitem{third}Third.\end{thebibliography}')
        document = table_document(r'\begin{table}[ht]\caption{Example}\cite{third,first}\end{table}',
                                  3, 'PREAMBLE', 'METADATA', manuscript)
        self.assertLess(document.index('METADATA'), document.index(r'\begin{document}'))
        self.assertIn(r'\setcounter{table}{2}', document)
        self.assertIn(r'\bibitem[1]{first}', document)
        self.assertIn(r'\bibitem[3]{third}', document)
        self.assertNotIn('Second.', document)
        self.assertNotIn(r'\begin{table}', document)

    def test_actual_tables_are_self_contained(self):
        count = 0
        for item in common.metadata()['papers']:
            paper = common.ROOT / 'papers' / item['directory']
            common.generate(item)
            manuscript = common.expand(paper / 'main.tex')
            labels = re.findall(r'\\label\{(tab:[^}]+)\}', manuscript)
            for source in (paper / 'tables').glob('*.tex'):
                table = common.expand(source, paper)
                label = re.search(r'\\label\{([^}]+)\}', table)[1]
                if label not in labels:
                    continue
                document = table_document(table, labels.index(label) + 1,
                    (common.ROOT / 'shared/preamble.tex').read_text(),
                    (paper / 'build/metadata.tex').read_text(), manuscript)
                self.assertNotIn(r'\input{', document)
                self.assertIn(r'\newcommand{\papershorttitle}', document)
                count += 1
                if shutil.which('latexmk'):
                    with tempfile.TemporaryDirectory() as directory:
                        target = Path(directory) / 'table.tex'
                        target.write_text(document)
                        result = subprocess.run(['latexmk', '-xelatex', '-interaction=nonstopmode',
                            '-halt-on-error', target.name], cwd=directory, text=True,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                        self.assertEqual(result.returncode, 0, result.stdout[-6000:])
                        log = target.with_suffix('.log').read_text()
                        self.assertNotIn('There were undefined references', log)
                        self.assertNotIn('Citation `', log)
        self.assertEqual(count, 6)


if __name__ == '__main__':
    unittest.main()
