from pyds import MassFunction

# --- Decimal library is used to make calculations exact, see https://docs.python.org/3/library/decimal.html from more details ------
from decimal import *
getcontext().prec=10
# -----------------------------------------------------------------------------------------------------------------------------------

# this class is like MassFunction, but it automatically accounts for Ω  (descernment frame — "cadre de descernement" in french)
class Masse(MassFunction):
    def __init__(self, source, omega):
        if isinstance(source, dict):
            s = 0.0
            for k,v in source.items():
                s += v
            if not source.get(omega, False) :
                source[omega] = float(1 - Decimal(s))
        super().__init__(source)

    # just like bel() but you pass a string (space separeted names)
    def bel_str(self, source):
        return self.bel(str_to_set(source))

    # just like pl() but you pass a string (space separeted names)
    def pl_str(self, source):
        return self.pl(str_to_set(source))

    # just like q() but you pass a string (space separeted names)
    def q_str(self, source):
        return self.q(str_to_set(source))

    def show_beleif(self):
        i = 1
        for ensemble, bel in self.bel().items():
            print(f'{i}- {set_to_str(ensemble)} : {bel}'); i += 1

    def __str__(self):
        text = ''
        for k,v in sorted(self.items(), key = lambda x : len(x[0])):
            text += f'{set_to_str(k)} : {v}\n'
        return text

def set_to_str(set_):
    return "{" + ', '.join([str(x) for x in set_]) + "}"

def str_to_set(text):
    return frozenset(text.split())
