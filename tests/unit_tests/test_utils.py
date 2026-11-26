"""Behavioural tests for pycmdtools' pure helpers."""

import hashlib
import json
import os
import tempfile
import unittest
from typing import TYPE_CHECKING
from unittest import mock

import pytest

from pycmdtools import schema_cache, utils

if TYPE_CHECKING:
    from pathlib import Path


class ChecksumTests(unittest.TestCase):
    def test_checksum_matches_hashlib(self):
        data = b"pycmdtools checksum payload\n" * 500
        with tempfile.NamedTemporaryFile(delete=False) as fh:
            fh.write(data)
            name = fh.name
        try:
            got = utils.checksum(name, "sha256")
            want = hashlib.sha256(data).hexdigest()
            assert got == want
        finally:
            os.unlink(name)

    def test_checksum_empty_file(self):
        with tempfile.NamedTemporaryFile(delete=False) as fh:
            name = fh.name
        try:
            got = utils.checksum(name, "md5")
            want = hashlib.new("md5", b"").hexdigest()
            assert got == want
        finally:
            os.unlink(name)


class DiamondLinesTests(unittest.TestCase):
    def test_reads_lines_from_files(self):
        names = []
        try:
            for chunk in ("a\nb\n", "c\n"):
                with tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8") as fh:
                    fh.write(chunk)
                    names.append(fh.name)
            lines = list(utils.diamond_lines(names))
            assert lines == ["a\n", "b\n", "c\n"]
        finally:
            for n in names:
                os.unlink(n)


class BadSymlinkTests(unittest.TestCase):
    @staticmethod
    def _touch(path: str) -> None:
        with open(path, "w", encoding="utf-8"):
            pass

    def test_finds_dangling_symlink(self):
        with tempfile.TemporaryDirectory() as d:
            target = os.path.join(d, "target")
            self._touch(target)
            good = os.path.join(d, "good")
            bad = os.path.join(d, "bad")
            os.symlink(target, good)
            os.symlink(os.path.join(d, "does-not-exist"), bad)
            found = list(utils.yield_bad_symlinks(folder=d))
            assert found == [bad]

    def test_standard_exceptions_are_skipped(self):
        with tempfile.TemporaryDirectory() as d:
            lock = os.path.join(d, "lock")
            os.symlink(os.path.join(d, "missing"), lock)
            skipped = list(utils.yield_bad_symlinks(folder=d, use_standard_exceptions=True))
            assert skipped == []
            included = list(utils.yield_bad_symlinks(folder=d, use_standard_exceptions=False))
            assert included == [lock]


class ErrorTests(unittest.TestCase):
    def test_error_reraises(self):
        exc = OSError("boom")
        with pytest.raises(OSError, match="boom"):
            utils.error(exc)


def _cache_file(url: str) -> Path:
    """Where schema_cache stores `url`: CACHE_DIR/<sha256 of the url>.json."""
    return schema_cache.CACHE_DIR / (hashlib.sha256(url.encode()).hexdigest() + ".json")


class SchemaCacheTests(unittest.TestCase):
    def test_fetch_schema_stores_under_sha256_json_name(self):
        url = "https://example.com/schema.json"
        with tempfile.TemporaryDirectory() as d:
            orig = schema_cache.CACHE_DIR
            schema_cache.CACHE_DIR = schema_cache.Path(d)
            try:
                response = mock.Mock()
                response.json.return_value = {"type": "object"}
                with mock.patch.object(schema_cache.requests, "get", return_value=response):
                    schema_cache.fetch_schema(url, use_cache=True, memory_cache={})
                assert [p.name for p in schema_cache.Path(d).iterdir()] == [
                    hashlib.sha256(url.encode()).hexdigest() + ".json"
                ]
            finally:
                schema_cache.CACHE_DIR = orig

    def test_fetch_schema_uses_memory_cache(self):
        cached = {"type": "object"}
        memory_cache = {"https://example.com/s.json": cached}
        # a memory-cache hit must not touch disk or network
        got = schema_cache.fetch_schema(
            "https://example.com/s.json",
            use_cache=False,
            memory_cache=memory_cache,
        )
        assert got is cached

    def test_fetch_schema_reads_disk_cache(self):
        with tempfile.TemporaryDirectory() as d:
            orig = schema_cache.CACHE_DIR
            schema_cache.CACHE_DIR = schema_cache.Path(d)
            try:
                url = "https://example.com/disk.json"
                schema = {"title": "on disk"}
                path = _cache_file(url)
                with open(path, "w", encoding="utf-8") as fh:
                    json.dump({"url": url, "schema": schema}, fh)
                memory_cache: dict = {}
                got = schema_cache.fetch_schema(url, use_cache=True, memory_cache=memory_cache)
                # a disk-cache hit returns the bare schema (the same shape the
                # memory-cache and fetch paths return) and memoises it
                assert got == schema
                assert memory_cache[url] is got
            finally:
                schema_cache.CACHE_DIR = orig

    def test_list_and_remove_and_clear_entries(self):
        with tempfile.TemporaryDirectory() as d:
            orig = schema_cache.CACHE_DIR
            schema_cache.CACHE_DIR = schema_cache.Path(d)
            try:
                url = "https://example.com/one.json"
                path = _cache_file(url)
                with open(path, "w", encoding="utf-8") as fh:
                    json.dump({"url": url, "schema": {}}, fh)
                assert schema_cache.list_entries() == [(url, str(path))]
                assert schema_cache.remove_entry(url)
                assert not schema_cache.remove_entry(url)
                assert schema_cache.list_entries() == []
                # clear_all counts what it deletes
                with open(_cache_file("https://example.com/two.json"),
                          "w", encoding="utf-8") as fh:
                    json.dump({"url": "https://example.com/two.json", "schema": {}}, fh)
                assert schema_cache.clear_all() == 1
            finally:
                schema_cache.CACHE_DIR = orig


if __name__ == "__main__":
    unittest.main()
