# Runtime dependencies

The package instructions, public renderer and fictional example are distributed under the root MIT license. Dependency source, browser binaries and fonts are downloaded at runtime, not vendored here.

| Dependency | Use | Upstream license |
|---|---|---|
| Excalidraw 0.18.0 | Native SVG export and optional geometry restoration | [MIT, copyright 2020 Excalidraw](https://github.com/excalidraw/excalidraw/blob/v0.18.0/LICENSE) |
| Playwright for Python 1.60.0 | Local browser rendering and PNG capture | [Apache-2.0](https://github.com/microsoft/playwright-python/blob/v1.60.0/LICENSE) |

Browser and font distributions retain their own notices. The renderer loads the Excalidraw module through esm.sh and resolves its font resources. No third-party project grants access to CinchOS or the coach's connected services.

The public renderer and diagram guidance were authored for this distribution against Excalidraw's documented export and restore APIs. The package does not include the earlier third-party diagram skill or its helper files.
