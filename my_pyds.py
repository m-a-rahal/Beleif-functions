from pyds import MassFunction
DECIMAL_PRECISTION = 5 # round values for before printing them on screen

# this class is like MassFunction, but it automatically accounts for Ω  (descernment frame — "cadre de descernement" in french)
class Mass(MassFunction):
    def __init__(self, source, omega = None):
        """
        Constructs a mass function. must receive:
        - omega : string with comma seperated names, e.g : "A1, A2, A3", or "car emissions, central heating"
        - source : a set containing all the sets and their massses e.g : {'a' : 0.1, 'b, c' : '0.2'}, or {'industrial cause, natural cause' : 0.5}
        """
        super().__init__()
        if omega is None:
            raise Exception('must specify omega in mass definition')
        # transform text input into sets
        source = Mass.transform_source(source)
        omega = str_to_set(omega)

        s = 0.0
        for k,v in source.items():
            s += v
        if not source.get(omega, False) :
            source[omega] = 1 - s

        for s in source:
            self[s] = source[s]


    def conflict(self, other):
        """
        calculated the conflict :
        K = ∑ m1(B) * m2(C) : B ∩ C = ∅,  ∀B,C ⊂ Ω
        """
        k = 0
        for b in self.all():
            for c in other.all():
                if len(b & c) == 0:
                    k += self[b] * other[c]
        return k

    def my_combine_conjunctive(self, other, normalization = True):
        res = Mass(self.combine_conjunctive(other, normalization = False), self.frame())
        return res.normalize_with_K(self.conflict(other))

    def normalize_with_K(self, K):
        """
        Sets the mass of ∅ to 0, and divides all others by 1 - K
        """
        # set mass(∅) = 0
        if frozenset() in self:
            del self[frozenset()]

        # for all others, divide by 1 - K where K = conflict constant
        factor = 1 / (1 - K)
        for k, v in self.items():
            self[k] = v * factor
        return self

    @staticmethod
    def transform_source(source):
        """
        transforms source from comma separeted strings into sets
        """
        new_source = {}
        for k,v in source.items():
            new_source[str_to_set(k)] = v
        return new_source

    def bel_str(self, source):
        """
        just like bel() but you pass a string (space separeted names)
        """
        return self.bel(str_to_set(source))


    def pl_str(self, source):
        """
        just like pl() but you pass a string (space separeted names)
        """
        return self.pl(str_to_set(source))


    def q_str(self, source):
        """
        just like q() but you pass a string (space separeted names)
        """
        return self.q(str_to_set(source))

    def show_beleif(self):
        i = 1
        for ensemble, bel in self.bel().items():
            print(f'{i}- {set_to_str(ensemble)} : {round(bel,DECIMAL_PRECISTION)}'); i += 1

    def __str__(self):
        text = ''
        for k,v in sorted(self.items(), key = lambda x : len(x[0])):
            if v > 0.0 or k == self.frame():
                text += f'{set_to_str(k)} : {round(v,DECIMAL_PRECISTION)}\n'
        return text


class Sources(list):
    def __init__(self, omega):
        """
        use this class to combine multiple sources (having the same 'omega')
        """
        super().__init__()
        self.omega = str_to_set(omega)
        self.sources_affaiblis = set()

    def add(self, source):
        self.append(Mass(source, self.omega))

    def affaiblir(self, source_index, alpha):
        """
        affaiblir une source avec un taux alpha d'affaiblissement
        """
        assert 0 <= alpha <= 1, 'alpha must be in range [0,1]'
        source = self[source_index]
        for s in source.keys():
            if s != self.omega: # affaiblire la masse des elements autre que omega
                source[s] = (1 - alpha)*source[s]
            else: # augmenter la masse de omega
                source[s] = (1 - alpha)*(source[s]) + alpha
            source[s] = source[s]
        
        # ajouter la source au sources affaiblis (affin de bien combiner par la suite)
        self.sources_affaiblis.add(source_index)

    def __str__(self):
        text = ''
        for i, s in enumerate(self):
            text += f'masses de la source {i+1} :\n'
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
            res = s1.my_combine_conjunctive(s2, normalization=True)
            if show_steps:
                print(f'combinaison {count} :'); count += 1
                k = s1.conflict(s2)
                print('k =', round(k, DECIMAL_PRECISTION), end = ', ')
                print('1/(1-k) =', round(1/(1-k), DECIMAL_PRECISTION))
                print(Mass(res, self.omega))

            s1 = res
        return Mass(s1, self.omega)



def str_to_set(text):
    """
    transforms comma separated string into a set
    'name1, name2, name3' -> {'name1', 'name2', 'name3'}
    """
    if isinstance(text, str):
        return frozenset([name.strip() for name in text.split(',')])
    elif isinstance(text, set) or isinstance(text, frozenset): # if its already a set, return it (might happen!)
        return text
    else:
        raise Exception(f'the input "{text}" was supposed to be a string (or maybe a set), introduced to function set_to_str')

def set_to_str(s):
    return "{" + ', '.join([str(x) for x in s]) + "}"

