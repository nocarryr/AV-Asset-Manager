def test():
    import os
    import subprocess
    import shlex
    cwd = os.path.dirname(os.path.abspath(__file__))
    os.chdir(os.path.join(cwd, 'avam'))
    cmd = 'python manage.py test'
    print(subprocess.check_output(shlex.split(cmd)))
