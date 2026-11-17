import hashlib
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from src import fetch_sources


class SourceImportTests(unittest.TestCase):
    def test_exact_source_import_is_idempotent_and_rejects_substitutes(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);source=root/'download';source.write_bytes(b'original')
            name='data/raw/source.zip'
            sources={name:('https://example.invalid/source',8,hashlib.sha256(b'original').hexdigest())}
            with patch.object(fetch_sources,'ROOT',root),patch.object(fetch_sources,'SOURCES',sources):
                fetch_sources.import_source(name,source)
                fetch_sources.import_source(name,source)
                self.assertEqual((root/name).read_bytes(),b'original')
                source.write_bytes(b'changed!')
                with self.assertRaisesRegex(ValueError,'not the recorded source'):
                    fetch_sources.import_source(name,source)
                self.assertEqual((root/name).read_bytes(),b'original')

    def test_different_existing_destination_is_preserved(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);source=root/'download';source.write_bytes(b'original')
            name='existing';(root/name).write_bytes(b'keep this')
            with patch.object(fetch_sources,'ROOT',root),patch.object(fetch_sources,'SOURCES',{name:('',8,hashlib.sha256(b'original').hexdigest())}):
                with self.assertRaisesRegex(ValueError,'left untouched'):fetch_sources.import_source(name,source)
                self.assertEqual((root/name).read_bytes(),b'keep this')
