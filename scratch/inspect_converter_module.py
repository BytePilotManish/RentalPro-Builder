import kannada_converter
from inspect import getmembers, isfunction, ismodule

print("Module contents:", dir(kannada_converter))
for name, val in getmembers(kannada_converter):
    print(f"{name}: {type(val)}")
