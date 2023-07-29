# -*- SPEC FILE FOR WINDOWS PAKAGE BUILD WITH PYINSTALLER -*-
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# -*- INSTALL YOUR CODE AND ALL DEPENDENCIES ON A VENV ENVIRONMENT -*-
# -*- EDIT THE FILE PATHS FOR YOUR INSTALLED FILE PATHS CHECK EACH CAREFULLY TO ENSURE EXISTS AND HAS SAME NAME-*-
# -*- IF THERE ARE ANY TORCH .dll FILES IN YOUR DIRECTORY NOT LISTED BELOW, ADD THEM USING THE SAME METHOD -*-
# -*- INSTALL PYINSTALLER TO YOUR VIRTUAL ENVIRONMENT -*-
# -*- RUN THIS FILE IN THE CODE FILE CONTAINING MAIN.PY -*-
# -*- RUN THIS FILE WITH COMMAND 'pyinstall main.spec -*-

# -*- NOTE - IT IS EASIER TO INSTALL "AUTO-PY-TO-EXE" AND ADD THE DEPENDENCIES IN THE GUI -*-
# -*- SEE AUTO_PY_TO_EXE.PDF -*-
# -*- AUTO-PY-TO-EXE PROVIDES A USER INTERFACE TO ADD THESE DEPENDENCIES -*-
# -*- OPEN THE OPEN AUTO-PY-TO-EXE TYPE COMMAND auto-to-py-exe IN THE COMMAND LIND
# -*- IN "SCRIPT LOCATION' CLICK BROWSE, NAVIGATE TO MAIN.PY AND ADD -*-
# -*- IN ONEFILE LEAVE AS "one Directory" -*-
# -*- IN CONSOLE WINDOW SELECT "Window based hide the console" -*-
# -*- IN ADDITIONAL FILES USE BROWSE TO ADD ALL THE DEPENDENCIES LISTED BELOW IN "datas" THE WILL BE IN YOUR VENV ENVIRONEMNT IN 'SITE PACKAGES' -*-
# -*- SELECTING ADD FILE FOR WAVIO AND SOUNDDEVICE .PY FILES -*-
# -*- FOR THE REMAINDER USE THE ADD FOLDER OPTION TO ADD E.G. NAVIGATE TO THE CUSTOMTKINTER FOLDER AND CLICK SELECT FOLDER -*-
# -*- EXPAND ADVANCED, UNDER "--add-binary" BROWSE TO ADD ALL TORCH .dll FILES AS BELOW USING THE ADD FOLDER OPTION -*-
# -*- MOVE TO BOTTOM OF THE FORM AND PRESS "CONVERT .PY TO .EXE" THIS SHOULD CREATE A FOLDER CALLED MAIN CONTAINING THE FILES AND THE MAIN.EXE -*-



a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[
        ('C:\\Users\\samhi\\documents\\myenv\\lib\\site-packages\\torch\\lib\\asmjit.dll', 'torch\\lib'),
        ('C:\\Users\\samhi\\documents\\myenv\\lib\\site-packages\\torch\\lib\\c10.dll', 'torch\\lib'),
        ('C:\\Users\\samhi\\documents\\myenv\\lib\\site-packages\\torch\\lib\\fbgemm.dll', 'torch\\lib'),
        ('C:\\Users\\samhi\\documents\\myenv\\lib\\site-packages\\torch\\lib\\libiomp5md.dll', 'torch\\lib'),
        ('C:\\Users\\samhi\\documents\\myenv\\lib\\site-packages\\torch\\lib\\libiompstubs5md.dll', 'torch\\lib'),
        ('C:\\Users\\samhi\\documents\\myenv\\lib\\site-packages\\torch\\lib\\shm.dll', 'torch\\lib'),
        ('C:\\Users\\samhi\\documents\\myenv\\lib\\site-packages\\torch\\lib\\torch.dll', 'torch\\lib'),
        ('C:\\Users\\samhi\\documents\\myenv\\lib\\site-packages\\torch\\lib\\torch_cpu.dll', 'torch\\lib'),
        ('C:\\Users\\samhi\\documents\\myenv\\lib\\site-packages\\torch\\lib\\torch_global_deps.dll', 'torch\\lib'),
        ('C:\\Users\\samhi\\documents\\myenv\\lib\\site-packages\\torch\\lib\\torch_python.dll', 'torch\\lib'),
        ('C:\\Users\\samhi\\documents\\myenv\\lib\\site-packages\\torch\\lib\\uv.dll', 'torch\\lib')
    ],
    datas=[
        ('C:\\Users\\samhi\\documents\\myenv\\lib\\site-packages\\customtkinter', 'customtkinter'),
        ('modules\\*.py', 'modules'),
        ('data\\*', 'data'),
        ('settings\\*', 'settings'),
        ('images\\*', 'images'),
        ('C:\\Users\\samhi\\documents\\myenv\\lib\\site-packages\\sounddevice.py', 'sounddevice'),
        ('C:\\Users\\samhi\\documents\\myenv\\lib\\site-packages\\wavio.py', 'wavio'),
        ('C:\\Users\\samhi\\documents\\myenv\\lib\\site-packages\\tkmacosx', 'tkmacosx'),
        ('C:\\Users\\samhi\\documents\\myenv\\lib\\site-packages\\yaml', 'yaml'),
        ('C:\\Users\\samhi\\documents\\myenv\\lib\\site-packages\\tk', 'tk'),
        ('C:\\Users\\samhi\\documents\\myenv\\lib\\site-packages\\whisper', 'whisper'),
        ('C:\\Users\\samhi\\documents\\myenv\\lib\\site-packages\\torch', 'torch'),
        ('C:\\Users\\samhi\\documents\\myenv\\lib\\site-packages\\ffmpeg', 'ffmpeg')
    ],
    hiddenimports=['certifi'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    exclude_binaries=False,
    name='dividu.exe',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None
)

