a = Analysis(['.\\main.py'],
             pathex=['C:\\Users\\User\\Documents\\Workspace\\Python_APP\\FolderReader'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)

def extra_datas(mydir):
    def rec_glob(p, files):
        import os
        import glob
        for d in glob.glob(p):
            if os.path.isfile(d):
                files.append(d)
            rec_glob("%s/*" % d, files)
    files = []
    rec_glob("%s/*" % mydir, files)
    extra_datas = []
    for f in files:
        extra_datas.append((f, f, 'DATA'))

    return extra_datas

a.datas += extra_datas('data')

for d in a.datas:
    if 'pyconfig' in d[0]: 
        a.datas.remove(d)
        break

pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='FolderReader.exe',
          debug=False,
          append_pkg=True,
          strip=None,
          upx=True,
          console=False , icon='data\\img\\icon.ico')
