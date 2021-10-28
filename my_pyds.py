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
            if v > 0.0 or k == self.frame():
                text += f'{set_to_str(k)} : {v}\n'
        return text


# use this class to combine multiple sources (having the same 'omega')
class Sources(list):
    def __init__(self, omega):
        super().__init__()
        self.omega = omega
        self.sources_affaiblis = set()

    def add(self, source):
        self.append(Masse(source, self.omega))

    # affaiblir une source avec un taux alpha d'affaiblissement
    def affaiblir(self, source_index, alpha):
        assert 0 <= alpha <= 1, 'alpha must be in range [0,1]'
        source = self[source_index]
        for s in source.keys():
            if s != self.omega: # affaiblire la masse des elements autre que omega
                source[s] = Decimal(1 - alpha)*Decimal(source[s])
            else: # augmenter la masse de omega
                source[s] = Decimal(1 - alpha)*Decimal(source[s]) + Decimal(alpha)
            source[s] = float(source[s])
        
        # ajouter la source au sources affaiblis (affin de bien combiner par la suite)
        self.sources_affaiblis.add(source_index)

    def __str__(self):
        text = ''
        for i, s in enumerate(self):
            text += f'resource {i+1} :\n'
            text += str(s) + '\n'
        return text

    def show_source(self, source_index):
        print(f'resource {source_index+1} :')
        print(self[source_index])

    def combine(self, conjonctive_only = True, show_steps = False):
        if not conjonctive_only:
            raise Exception('feature undevelopped yet')
        
        # ignore useless sources, where there's total ignorance
        sources = [s for s in self if s[self.omega] < 1]

        # nothing to do if there isn't two sources to combine at least, return one of the sources 
        if len(sources) == 0:
            return self[0]
        elif len(sources) == 1:
            return sources[0]

        # combine sources two by two
        i = 0
        s1 = sources[i]; i += 1
        count = 1
        while i < len(sources):
            s2 = sources[i]; i += 1
            res = s1.combine_conjunctive(s2, normalization=True)
            if show_steps:
                print(f'combinaison {count} :'); count += 1
                print('k =', s1.conflict(s2))
                print(Masse(res, self.omega))

            s1 = res
        return Masse(s1, self.omega)


def set_to_str(s):
    return "{" + ', '.join([str(x) for x in s]) + "}"

def str_to_set(text):
    return frozenset(text.split())
