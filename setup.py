from cx_Freeze import setup, Executable

executables = [Executable('main.py',
                          targetName='Isopoly merger.exe',
                          icon='resources\\Isopoly_merger.ico')]

excludes = ['unittest', 'email', 'html', 'http', 'xml', 'pydoc']
zip_include_packages = ['collections', 'encodings',
                        'importlib', 'isopoly_merger', 'logging']
include_files = [('resources/GOST_Common Italic.ttf', 'resources/GOST_Common Italic.ttf'),
                 ('resources/GOST_Common.ttf', 'resources/GOST_Common.ttf')]

options = {
    'build_exe': {
        'include_msvcr': True,
        'build_exe': 'build_windows',
        'excludes': excludes,
        'zip_include_packages': zip_include_packages,
        'include_files': include_files,
    }
}

setup(
    name="Isopoly merger",
    version="0.9.0",
    description="Слияние результатов расчётов изополей по максимальному значению",
    executables=executables,
    options=options
)
