[app]
title = Cash Flow Manager
package.name = cashflowmanager
package.domain = org.cfmanager
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0

requirements = python3,kivy==2.2.1,kivymd==1.1.1,pillow,fpdf,sqlite3

orientation = portrait
fullscreen = 0

android.permissions = INTERNET,READ_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a

android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
