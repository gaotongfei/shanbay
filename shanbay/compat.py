import sys

py_version = sys.version_info.major

is_py2 = (py_version == 2)
is_py3 = (py_version == 3)

if is_py2:
    bytes = str
elif is_py3:
    bytes = bytes