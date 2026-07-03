[app]
title = محفظة التمويل والتحصيل
package.name = financemobile
package.domain = org.mokhtargerges

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,db,ttf

version = 1.0

requirements = python3==3.11,kivy==2.3.0,kivymd==1.2.0,pillow,sqlite3

orientation = portrait
fullscreen = 0

android.permissions = \
    INTERNET,\
    READ_EXTERNAL_STORAGE,\
    WRITE_EXTERNAL_STORAGE,\
    READ_CONTACTS,\
    WRITE_CONTACTS,\
    CAMERA,\
    ACCESS_NETWORK_STATE,\
    RECEIVE_BOOT_COMPLETED,\
    VIBRATE,\
    WAKE_LOCK,\
    FOREGROUND_SERVICE

android.api = 33
android.minapi = 21
android.ndk = 25b
android.sdk = 33
android.accept_sdk_license = True
android.arch = arm64-v8a

android.enable_androidx = True
android.add_compile_options = "sourceCompatibility = JavaVersion.VERSION_11" "targetCompatibility = JavaVersion.VERSION_11"

android.wakelock = True
android.allow_backup = True

icon.filename = %(source.dir)s/icon.png
presplash.filename = %(source.dir)s/presplash.png

[buildozer]
log_level = 2
warn_on_root = 1
