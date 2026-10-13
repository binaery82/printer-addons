# Printer Add-ons for Home Assistant

A collection of Home Assistant add-ons for printer-related tasks.

[![GitHub Release](https://img.shields.io/github/v/release/binaery82/printer-addons?label=release)](https://github.com/binaery82/printer-addons/releases)
[![License](https://img.shields.io/github/license/binaery82/printer-addons)](LICENSE)

## 🧩 Available Add-ons

### PWG Raster Converter

Converts PDF files to **PWG Raster** (`image/pwg-raster`) on demand. Used by the [IPPx Printer](https://github.com/binaery82/ippx_printer) integration for printing PDFs on printers that do not support PDF natively.

PWG-Raster is the document format required by IPP Everywhere printers. It allows printing multi-page PDFs as a **single job**, which is not possible with other formats like JPEG.

## 🗂️ Installation

1. In Home Assistant: **Settings → Add-ons → Add-on Store**.
2. Top right: **⋮ → Repositories**.
3. Add the URL of this repository:

   ```link
   https://github.com/binaery82/printer-addons
   ```

4. Click **Add**.
5. The add-ons from this repository now appear in the store.

## ⚙️ Configuration

### PWG Raster Converter

| Option | Type | Default | Range | Description |
| - | - | - | - | - |
| `dpi` | integer | `300` | `72`–`4800` | Resolution for the PWG Raster output. Higher values produce sharper prints but larger files. |

**Notes on DPI:**

- `300` is the standard for most printers and produces good quality.
- `600` improves text sharpness for small fonts.
- `1200` or higher is rarely needed and produces very large files.
- The printer scales the raster to its own resolution if it differs.

## 🔗 Companion Integration

The **PWG Raster Converter** is designed to work with the [IPPx Printer](https://github.com/binaery82/ippx_printer) Home Assistant integration. When printing a PDF on a printer that does not support PDF natively, the integration automatically routes the PDF through this add-on.

If the add-on is not installed or not running, the integration returns a clear error message and the PDF is not printed.

## 🛠️ Development

### Repository structure

```none
printer-addons/
├── repository.yaml                # Identifies this repository to Home Assistant
├── README.md
├── LICENSE
└── pwg-converter/                 # The add-on
    ├── config.yaml                # Add-on metadata
    ├── Dockerfile                 # Container definition
    ├── run.sh                     # Start script
    ├── server.py                  # HTTP server + PDF → PWG conversion
    └── translations/
        ├── en.yaml                # English translations
        └── de.yaml                # German translations
```

### Adding a new add-on

1. Create a new folder in the repository root.
2. Add a `config.yaml`, `Dockerfile`, and `run.sh`.
3. Optionally add a `translations/` folder.
4. Restart the add-on store or reload the repository in Home Assistant.

The add-on is then available in the store.

### Testing locally

1. Copy the add-on folder to the `addons` directory of your Home Assistant installation.
2. In Home Assistant: **Settings → Add-ons → Add-on Store**.
3. Top right: **⋮ → Check for updates**.
4. The add-on appears under **Local add-ons**.

### Building for multi-architecture

The `config.yaml` lists supported architectures under `arch`. For distribution via GitHub, use a CI/CD workflow (e.g., GitHub Actions) to build and publish multi-architecture images to a container registry.

## 🐛 Issues and Feature Requests

Please open an issue in the [issue tracker](https://github.com/binaery82/printer-addons/issues) if you find a bug or want to request a feature.

## 📄 License

See [LICENSE](LICENSE).

## 🙏 Acknowledgments

- **[Ghostscript](https://www.ghostscript.com/)** – used by the PWG Raster Converter for PDF rendering.
- **[Home Assistant](https://www.home-assistant.io/)** – for the add-on framework.
- The Home Assistant community – for documentation and examples.
