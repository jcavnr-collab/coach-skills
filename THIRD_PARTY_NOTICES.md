# Fonts, artwork, and runtime dependencies

The package's original instructions, renderers, and fictional examples are distributed under the root MIT license. The exceptions and runtime dependencies below retain their own licenses.

| Dependency | Use | Upstream license |
|---|---|---|
| Excalidraw 0.18.0 | Native SVG export and optional geometry restoration | [MIT, copyright 2020 Excalidraw](https://github.com/excalidraw/excalidraw/blob/v0.18.0/LICENSE) |
| Playwright for Python 1.60.0 | Local browser rendering and PNG capture | [Apache-2.0](https://github.com/microsoft/playwright-python/blob/v1.60.0/LICENSE) |
| markdown-it-py 4.2.0 | Whitepaper Markdown parsing | [MIT](https://github.com/executablebooks/markdown-it-py/blob/master/LICENSE) |
| pypdfium2 5.14.0 | Rasterize the actual PDF pages | [Apache-2.0 or BSD-3-Clause; PDFium and dependencies retain their notices](https://github.com/pypdfium2-team/pypdfium2/blob/main/LICENSE) |
| Pillow 13.0.0 | Image validation and PNG output | [MIT-CMU](https://github.com/python-pillow/Pillow/blob/main/LICENSE) |

Browser and font distributions retain their own notices. The renderer loads the Excalidraw module through esm.sh and resolves its font resources. No third-party project grants access to CinchOS or the coach's connected services.

The Cinch whitepaper skill bundles unmodified Epilogue and Open Sans variable fonts under SIL Open Font License 1.1. Copyright and license text are in [its fonts folder](plugins/cinch-coach/skills/cinch-whitepaper/assets/fonts/); `sources.json` records exact upstream URLs and SHA-256 hashes. Its HTML exports embed the corresponding license notices. The illustrated Rincon guide embeds Outfit, also under [SIL OFL 1.1](docs/assets/licenses/Outfit-OFL.txt). The guide's editable Excalidraw/SVG diagram carries the same Outfit notice alongside it.

Rincon AI's guide artwork and brand mark are supplied for this guide and remain Rincon AI brand assets, outside the code's MIT grant. Cinch Cycling and other service names and identities remain the property of their respective owners. This package grants no trademark rights or endorsement by a service provider.

The public renderer and diagram guidance were authored for this distribution against Excalidraw's documented export and restore APIs. The package does not include the earlier third-party diagram skill or its helper files.
