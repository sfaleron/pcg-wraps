try:
    import subprocess32 as subprocess

except ImportError:
    import subprocess

if hasattr(subprocess, 'run'):
    exthdlr = subprocess.run
else:
    exthdlr = subprocess.call
