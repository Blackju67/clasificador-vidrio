[app]
title = ClasificadorVidrio
package.name = clasificadorvidrio
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy

orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 1

[android]
android.archs = arm64-v8a
android.allow_backup = True
