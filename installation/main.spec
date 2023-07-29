# -*- MacOS SPEC file for DiViDu-next -*-

# -*- mode: python ; coding: utf-8 -*-


block_cipher = None

# -*- INSTALL YOUR CODE AND ALL DEPENDENCIES ON A VENV ENVIRONMENT -*-
# -*- EDIT THE FILE PATHS FOR YOUR INSTALLED FILE PATHS CHECK EACH CAREFULLY TO ENSURE EXISTS AND HAS SAME NAME-*-
# -*- IF THERE ARE ANY TORCH .dll FILES IN YOUR DIRECTORY NOT LISTED BELOW, ADD THEM USING THE SAME METHOD -*-
# -*- INSTALL PYINSTALLER TO YOUR VIRTUAL ENVIRONMENT -*-
# -*- RUN THIS FILE IN THE CODE FILE CONTAINING MAIN.PY -*-
# -*- RUN THIS FILE WITH COMMAND 'pyinstall main.spec' -*-

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[('/Users/richardhill/Documents/Uni/Project/Code/version260323/Team11/DividuCode/env/lib/python3.10/site-packages/torch/lib/libc10.dylib','torch/lib'), 
              ('/Users/richardhill/Documents/Uni/Project/Code/version260323/Team11/DividuCode/env/lib/python3.10/site-packages/torch/lib/libiomp5.dylib', 'torch/lib'), 
              ('/Users/richardhill/Documents/Uni/Project/Code/version260323/Team11/DividuCode/env/lib/python3.10/site-packages/torch/lib/libshm.dylib', 'torch/lib'), 
              ('/Users/richardhill/Documents/Uni/Project/Code/version260323/Team11/DividuCode/env/lib/python3.10/site-packages/torch/lib/libtorch_cpu.dylib', 'torch/lib'), 
              ('/Users/richardhill/Documents/Uni/Project/Code/version260323/Team11/DividuCode/env/lib/python3.10/site-packages/torch/lib/libtorch_global_deps.dylib', 'torch/lib'), 
              ('/Users/richardhill/Documents/Uni/Project/Code/version260323/Team11/DividuCode/env/lib/python3.10/site-packages/torch/lib/libtorch_python.dylib', 'torch/lib'), 
              ('/Users/richardhill/Documents/Uni/Project/Code/version260323/Team11/DividuCode/env/lib/python3.10/site-packages/torch/lib/libtorch.dylib', 'torch/lib')],
    datas=[('/Users/richardhill/Documents/Uni/Project/Code/version260323/Team11/DividuCode/env/lib/python3.10/site-packages/customtkinter', 'customtkinter'), 
           ('modules/*.py', 'modules'), 
           ('data/*', 'data'), 
           ('settings/*', 'settings'), 
           ('images/*', 'images'), 
           ('/Users/richardhill/Documents/Uni/Project/Code/version260323/Team11/DividuCode/env/lib/python3.10/site-packages/sounddevice.py', 'sounddevice'), 
           ('/Users/richardhill/Documents/Uni/Project/Code/version260323/Team11/DividuCode/env/lib/python3.10/site-packages/wavio.py', 'wavio'), 
           ('/Users/richardhill/Documents/Uni/Project/Code/version260323/Team11/DividuCode/env/lib/python3.10/site-packages/tkmacosx', 'tkmacosx'), 
           ('/Users/richardhill/Documents/Uni/Project/Code/version260323/Team11/DividuCode/env/lib/python3.10/site-packages/yaml', 'yaml'), 
           ('/Users/richardhill/Documents/Uni/Project/Code/version260323/Team11/DividuCode/env/lib/python3.10/site-packages/tk', 'tk'), 
           ('/Users/richardhill/Documents/Uni/Project/Code/version260323/Team11/DividuCode/env/lib/python3.10/site-packages/whisper', 'whisper'), 
           ('/Users/richardhill/Documents/Uni/Project/Code/version260323/Team11/DividuCode/env/lib/python3.10/site-packages/torch', 'torch'),
           ('/Users/richardhill/Documents/Uni/Project/Code/version260323/Team11/DividuCode/env/lib/python3.10/site-packages/ffmpeg','ffmpeg')],
    hiddenimports=['/Users/richardhill/Documents/Uni/Project/Code/version260323/Team11/DividuCode/env/lib/python3.10/site-packages/certifi','certifi'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='main',
)
app = BUNDLE(
    coll,
    name='dividunext.app',
    icon=None,
    bundle_identifier=None,
)
