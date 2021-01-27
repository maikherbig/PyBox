# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['PyBox.py'],
             pathex=['C:\\Users\\s7378965\\anaconda3\\envs\\PyBox_0.1.0'],
             binaries=[],
             datas=[],
             hiddenimports=['pywt','pywt._extensions._cwt','pywrap_tensorflow','_pywrap_tensorflow_internal','aid_imports'],
             hookspath=[],
             runtime_hooks=[],
             excludes=['model_zoo','aid_backbone','aid_bin','aid_start','aid_dl','aid_frontend','aid_img','partial_trainability.py'],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='PyBox_0.1.0',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True , icon='icon_main.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='PyBox_0.1.0')
