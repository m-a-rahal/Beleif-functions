import exo1, exo4, exo5
from my_pyds import pritty_print, show_dict
from time import sleep

sources = exo5.init(False)
for s in sources:
    pritty_print('beleifs (non nuls) du premier expert ')
    show_dict(s.bel(), skip_null_values = True)
    sleep(2)

    pritty_print('plausibilités (non nuls) du premier expert ')
    show_dict(s.pl(), skip_null_values = True)
    sleep(5)