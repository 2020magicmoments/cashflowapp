[app]
title = Cash Flow Manager
package.name = cashflowmanager
package.domain = org.cfmanager
source.dir = .
source.include_exts = py,png,jpg,kv,atlas

# Fixed version error
version = 1.0

# Fixed requirements
requirements = python3,kivy==2.2.1,kivymd,pillow,sqlite3,fpdf,android

orientation = portrait
fullscreen = 0
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1