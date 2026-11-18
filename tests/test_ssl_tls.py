"""PRO-59: цепочка доверия TLS (certifi → truststore → SSL_CERT_FILE), понятная ошибка
CERTIFICATE_VERIFY_FAILED с готовой командой исправления и HTTPS-проверка в pfs doctor.
Сеть не трогаем: ssl-контекст и opener подменяются в тестах.

Запуск: python3 -m unittest tests.test_ssl_tls -v
"""
import argparse
import io
import os
import ssl
import sys
import tempfile
import types
import unittest
import urllib.error
import urllib.request
from contextlib import redirect_stdout
from unittest import mock

from tools.pfs import cli, extract  # noqa: E402
from tools.pfs.core import PfsError  # noqa: E402

URL = "https://example.org/pricing"

SSL_ERR = urllib.error.URLError(ssl.SSLCertVerificationError(
    1, "[SSL: CERTIFICATE_VERIFY_FAILED] unable to get local issuer certificate (_ssl.c:1000)"))
NET_ERR = urllib.error.URLError(ConnectionError("connection refused"))


class FakeOpener:
    """Opener, чей open() всегда падает заданной ошибкой (до сети дело не доходит)."""

    def __init__(self, exc):
        self.exc = exc

    def open(self, req, timeout=None):
        raise self.exc


class SSLContextTests(unittest.TestCase):
    def test_fetch_url_passes_substituted_context_to_https_handler(self):
        """Подмена ssl-контекста: fetch_url строит HTTPSHandler с контекстом из build_ssl_context."""
        marker = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        captured = {}
        handler_mock = mock.MagicMock(side_effect=lambda **kw: captured.update(kw) or mock.MagicMock())
        with mock.patch.object(extract, "build_ssl_context", return_value=marker), \
             mock.patch.object(urllib.request, "HTTPSHandler", handler_mock), \
             mock.patch.object(urllib.request, "build_opener", return_value=FakeOpener(NET_ERR)), \
             mock.patch.object(extract.socket, "getaddrinfo", return_value=[("AF_INET", 1, 6, "", ("93.184.216.34", 0))]):
            with self.assertRaises(PfsError):
                extract.fetch_url(URL, attempts=1)
        self.assertIs(captured["context"], marker)

    def test_ssl_failure_message_names_ready_fix_command(self):
        """CERTIFICATE_VERIFY_FAILED: в тексте ошибки — готовая команда исправления, TLS не отключается.

        Ожидания ветвятся по способу установки (PRO-82, QA D3): в uv tool окружении
        pip нет — там совет «uv tool install --with certifi», в venv/system — pip
        (+ mac-подсказка «Install Certificates.command» на macOS).
        """
        with mock.patch.object(urllib.request, "build_opener", return_value=FakeOpener(SSL_ERR)), \
             mock.patch.object(extract.socket, "getaddrinfo", return_value=[("AF_INET", 1, 6, "", ("93.184.216.34", 0))]):
            with self.assertRaises(PfsError) as cm:
                extract.fetch_url(URL, attempts=1)
        msg = str(cm.exception)
        self.assertIn("certifi", msg)
        if "/uv/tools/" in sys.executable:
            self.assertIn("uv tool install --force --with certifi product-factory-strategist", msg)
        else:
            self.assertIn("pip install certifi", msg)
            self.assertIn(sys.executable, msg)
            if sys.platform == "darwin":
                self.assertIn("Install Certificates.command", msg)  # на macOS — готовый путь исправления
        self.assertNotIn("check_hostname = False", msg)  # проверку TLS не отключаем никогда

    def test_non_ssl_failure_keeps_manual_save_hint(self):
        """Обычная сетевая ошибка: прежняя подсказка «сохраните вручную», без совета про сертификаты."""
        with mock.patch.object(urllib.request, "build_opener", return_value=FakeOpener(NET_ERR)), \
             mock.patch.object(extract.socket, "getaddrinfo", return_value=[("AF_INET", 1, 6, "", ("93.184.216.34", 0))]):
            with self.assertRaises(PfsError) as cm:
                extract.fetch_url(URL, attempts=1)
        msg = str(cm.exception)
        self.assertIn("Сохраните страницу вручную", msg)
        self.assertNotIn("Install Certificates.command", msg)


class CertHintTests(unittest.TestCase):
    def test_hint_names_pip_certifi_and_macos_command(self):
        """Подсказка соответствует способу установки (QA C-02): uv tool → uv-команда,
        venv/system → pip (+ mac-подсказка «Install Certificates.command» на macOS)."""
        hint = extract.cert_fix_hint()
        if "/uv/tools/" in sys.executable:
            self.assertIn("uv tool install --force --with certifi product-factory-strategist", hint)
            self.assertNotIn("pip install", hint)
        else:
            self.assertIn("pip install certifi", hint)
            self.assertIn(sys.executable, hint)
            if sys.platform == "darwin":
                self.assertIn("Install Certificates.command", hint)

    def test_hint_uv_tool_branch_names_uv_command(self):
        """uv tool-ветка (QA D3/PRO-82): в окружении без pip — команда uv tool install."""
        uv_python = "/home/z/.local/share/uv/tools/product-factory-strategist/bin/python3"
        with mock.patch.object(extract.sys, "executable", uv_python):
            hint = extract.cert_fix_hint()
        self.assertIn("uv tool install --force --with certifi product-factory-strategist", hint)
        self.assertNotIn("pip install", hint)  # pip в uv tool окружении отсутствует
        self.assertNotIn("Install Certificates.command", hint)

    def test_is_cert_error_detects_wrapped_and_plain_ssl(self):
        self.assertTrue(extract.is_cert_error(SSL_ERR))
        self.assertTrue(extract.is_cert_error(
            ssl.SSLCertVerificationError(1, "[SSL: CERTIFICATE_VERIFY_FAILED] boom")))
        self.assertFalse(extract.is_cert_error(NET_ERR))
        self.assertFalse(extract.is_cert_error(
            urllib.error.HTTPError(URL, 403, "Forbidden", None, None)))


class BuildSSLContextTests(unittest.TestCase):
    def _ctx(self, **modules):
        """build_ssl_context с подменой ssl.create_default_context и модулей certifi/truststore."""
        fake_ctx = mock.MagicMock()
        fake_ctx.get_ca_certs.return_value = modules.pop("ca_certs", [{"x": 1}])
        with mock.patch.dict(sys.modules, modules), \
             mock.patch.object(ssl, "create_default_context", return_value=fake_ctx):
            return fake_ctx, extract.build_ssl_context()

    def test_certifi_loaded_into_default_context(self):
        fake_certifi = types.SimpleNamespace(where=lambda: "/fake/certifi.pem")
        fake_ctx, ctx = self._ctx(certifi=fake_certifi, truststore=None)
        self.assertIs(ctx, fake_ctx)
        fake_ctx.load_verify_locations.assert_called_once_with("/fake/certifi.pem")

    def test_truststore_used_when_store_empty_and_certifi_missing(self):
        ts_ctx = mock.MagicMock()
        fake_ts = types.SimpleNamespace(SSLContext=lambda proto: ts_ctx)
        fake_ctx, ctx = self._ctx(ca_certs=[], certifi=None, truststore=fake_ts)
        self.assertIs(ctx, ts_ctx)  # пустое хранилище → системное через truststore

    def test_default_context_kept_when_it_has_cas(self):
        fake_ctx, ctx = self._ctx(certifi=None, truststore=None)
        self.assertIs(ctx, fake_ctx)  # хранилище с CA (учитывает SSL_CERT_FILE) — оставляем
        fake_ctx.load_verify_locations.assert_not_called()


class HttpsProbeTests(unittest.TestCase):
    def test_probe_reports_three_domains(self):
        """HTTPS-проверка doctor: 2–3 домена, статус каждого."""
        statuses = extract.https_probe(get=lambda url, timeout: "ok")
        self.assertEqual(len(statuses), 3)
        self.assertEqual([st for _, st in statuses], ["ok", "ok", "ok"])
        self.assertEqual([h for h, _ in statuses][0], "pypi.org")

    def test_https_get_classifies_ssl_http_and_network(self):
        captured = {}

        def fake_urlopen(req, timeout=None, context=None):
            captured["context"] = context
            raise SSL_ERR

        with mock.patch.object(extract, "build_ssl_context", return_value=ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)), \
             mock.patch.object(urllib.request, "urlopen", fake_urlopen):
            self.assertEqual(extract.https_get("https://pypi.org/", timeout=2), "ssl")
            self.assertIsNotNone(captured["context"])  # зонды идут с тем же TLS-контекстом
        with mock.patch.object(urllib.request, "urlopen",
                               side_effect=urllib.error.HTTPError(URL, 403, "Forbidden", None, None)):
            self.assertEqual(extract.https_get("https://pypi.org/", timeout=2), "http 403")
        with mock.patch.object(urllib.request, "urlopen", side_effect=NET_ERR):
            self.assertEqual(extract.https_get("https://pypi.org/", timeout=2), "net")


class DoctorHTTPSTests(unittest.TestCase):
    def setUp(self):
        # изолированный каталог проектов: doctor сканирует реестры активного projects dir,
        # а в общем каталоге других тестов бывает project.json без slug (независимо от PRO-59)
        tmp = tempfile.mkdtemp(prefix="pfs-test-doctor-")
        patcher = mock.patch.dict(os.environ, {"PFS_PROJECTS_DIR": tmp})
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_doctor_prints_https_ok_line(self):
        with mock.patch.object(extract, "https_probe",
                               return_value=[("pypi.org", "ok"), ("www.python.org", "ok"), ("example.com", "ok")]):
            buf = io.StringIO()
            with redirect_stdout(buf):
                cli.cmd_doctor(argparse.Namespace())
        self.assertIn("HTTPS", buf.getvalue())
        self.assertIn("pypi.org: ok", buf.getvalue())

    def test_doctor_prints_certificates_hint_on_ssl_failure(self):
        with mock.patch.object(extract, "https_probe",
                               return_value=[("pypi.org", "ssl"), ("www.python.org", "ssl"), ("example.com", "net")]):
            buf = io.StringIO()
            with redirect_stdout(buf):
                cli.cmd_doctor(argparse.Namespace())
        out = buf.getvalue()
        self.assertIn("pypi.org: ssl", out)
        self.assertIn("certifi", out)
        if "/uv/tools/" in sys.executable:  # ветка ремедиации по способу установки (PRO-82)
            self.assertIn("uv tool install --force --with certifi", out)
        else:
            self.assertIn("pip install certifi", out)
            if sys.platform == "darwin":
                self.assertIn("Install Certificates.command", out)


if __name__ == "__main__":
    unittest.main()
