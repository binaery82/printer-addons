"""HTTP server that converts PDF to PWG Raster using Ghostscript."""

import http.server
import subprocess
import tempfile
import os
import json
import logging

logging.basicConfig(level=logging.INFO)
_LOGGER = logging.getLogger(__name__)

LISTEN_PORT = 8099
OPTIONS_FILE = "/data/options.json"
DEFAULT_DPI = 300


def _load_dpi() -> int:
    """Load the configured DPI from the add-on options."""
    try:
        with open(OPTIONS_FILE) as f:
            options = json.load(f)
        return int(options.get("dpi", DEFAULT_DPI))
    except Exception as err:
        _LOGGER.warning(
            "Could not read options from %s: %s. Using default DPI %d.",
            OPTIONS_FILE, err, DEFAULT_DPI,
        )
        return DEFAULT_DPI


class PdfToPwgHandler(http.server.BaseHTTPRequestHandler):
    """Handles POST requests with PDF data."""

    def do_POST(self):
        try:
            length = int(self.headers.get("Content-Length", 0))
            if length == 0:
                self.send_error(400, "Empty request body")
                return

            pdf_bytes = self.rfile.read(length)
            _LOGGER.info("Received PDF: %d bytes", len(pdf_bytes))

            dpi = _load_dpi()
            pwg_bytes = self._convert_pdf_to_pwg(pdf_bytes, dpi)

            self.send_response(200)
            self.send_header("Content-Type", "application/vnd.pwg-raster")
            self.send_header("Content-Length", str(len(pwg_bytes)))
            self.end_headers()
            self.wfile.write(pwg_bytes)
            _LOGGER.info("Sent PWG Raster: %d bytes (DPI=%d)", len(pwg_bytes), dpi)

        except Exception as err:
            _LOGGER.exception("Conversion failed: %s", err)
            self.send_error(500, f"Conversion failed: {err}")

    def _convert_pdf_to_pwg(self, pdf_bytes: bytes, dpi: int) -> bytes:
        """Convert PDF bytes to PWG Raster bytes using Ghostscript.

        No -sPAPERSIZE is passed, so Ghostscript uses the page size
        from the PDF and writes it into the PWG Raster metadata.
        """
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f_in:
            f_in.write(pdf_bytes)
            pdf_path = f_in.name

        pwg_path = pdf_path + ".pwg"

        try:
            result = subprocess.run(
                [
                    "gs",
                    "-dSAFER",
                    "-dBATCH",
                    "-dNOPAUSE",
                    "-sDEVICE=pwgraster",
                    f"-r{dpi}x{dpi}",
                    f"-sOutputFile={pwg_path}",
                    pdf_path,
                ],
                capture_output=True,
                timeout=120,
            )

            if result.returncode != 0:
                stderr = result.stderr.decode(errors="replace")
                raise RuntimeError(f"Ghostscript error: {stderr}")

            with open(pwg_path, "rb") as f:
                return f.read()

        finally:
            os.unlink(pdf_path)
            if os.path.exists(pwg_path):
                os.unlink(pwg_path)

    def log_message(self, format, *args):
        """Suppress default HTTP logging noise."""
        pass


if __name__ == "__main__":
    dpi = _load_dpi()
    server = http.server.HTTPServer(("0.0.0.0", LISTEN_PORT), PdfToPwgHandler)
    _LOGGER.info("PWG Converter listening on port %d (DPI=%d)", LISTEN_PORT, dpi)
    server.serve_forever()