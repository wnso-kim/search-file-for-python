# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=['/Users/argo/workspace/SEARCH_FILE_PROJECT/src/search_src'],  # 스크립트 파일이 있는 디렉토리
    binaries=[],
    datas=[('/Users/argo/workspace/SEARCH_FILE_PROJECT/src/search_src', 'search_src'),  # 스크립트 파일과 함께 포함될 디렉토리 및 별칭
        ('/Users/argo/workspace/SEARCH_FILE_PROJECT/src/pyqt_widget_src/searchFileMainUi.ui', '.'),  # UI 파일 및 별칭
        ('/Users/argo/workspace/SEARCH_FILE_PROJECT/src/pyqt_widget_src/searchFileTagUi.ui', '.'),
        ('/Users/argo/workspace/SEARCH_FILE_PROJECT/src/search_src/fileFolder.py', 'search_src'),  # 다른 Python 스크립트 파일 및 별칭
        ('/Users/argo/workspace/SEARCH_FILE_PROJECT/src/search_src/tag.py', 'search_src'),
        ('/Users/argo/workspace/SEARCH_FILE_PROJECT/src/pyqt_widget_src/widget.py', 'pyqt_widget_src')],
    hiddenimports=['watchdog.observers', 'watchdog.events', 'PyQt6.uic', 'PyQt6.QtCore', 'PyQt6.QtGui', 'PyQt6.QtWidgets', 'json'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
app = BUNDLE(
    exe,
    name='main.app',
    icon=None,
    bundle_identifier=None,
)
