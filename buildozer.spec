[app]
# (required) Title of your application
title = Elektrotechnický pomocník

# (required) Package name
package.name = elektrotechnicky-pomocnik

# (required) Package domain
package.domain = com.markusaureus

# (required) Source code where the main.py lives
source.dir = .

# (required) Source filename to your main file
# <--- DÔLEŽITÉ: Uistite sa, že toto je správny názov vášho súboru!
source.main_py = main.py

# (optional) Icon of the application
# <--- ZMENA: Cesta opravená podľa vašej štruktúry
icon.filename = %(source.dir)s/icon.png

# (optional) Presplash of the application
# <--- ZMENA: Cesta opravená podľa vašej štruktúry
presplash.filename = %(source.dir)s/presplash_screen.png

# (required) Application version
version = 1.0

# (required) Application requirements
requirements = python3,kivy,pyjnius,kivymd,android

# (optional) Application orientation
orientation = portrait

# (optional) Make the application fullscreen
fullscreen = 0

# (optional) List of Android permissions
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, FOREGROUND_SERVICE


[buildozer]
# (int) Log level (0 = error, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1

# (str) The directory in which python-for-android will be cloned
p4a.branch = master



[android]
# (str) The Android archs to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.archs = arm64-v8a

# (int) Target Android API, should be the highest one available.
android.api = 34

# (int) Minimum API your APK / AAB will support.
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (bool) If True, then automatically accept SDK license
android.accept_sdk_license = True

# (list) Permissions - pre túto aplikáciu nie sú potrebné žiadne
# android.permissions =

# (str) The Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
# android.archs = arm64-v8a, armeabi-v7a

# (bool) enables Android auto backup feature (Android API >= 23)
android.allow_backup = True

# (str) The format used to package the app for release mode (aab or apk)
android.release_artifact = apk

# Požiadavky pre AndroidX
android.enable_androidx = True
android.gradle_dependencies = 'androidx.appcompat:appcompat:1.2.0'
