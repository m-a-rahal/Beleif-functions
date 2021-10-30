from pyds import MassFunction, powerset
import time
DECIMAL_PRECISTION = 5 # round values for before printing them on screen

# IMPLEMENTER LA RECONNAISSANCE DES SPECIFITE DES FCTS DE MASSES !!!!!

# this class is like MassFunction, but it automatically accounts for Ω  (descernment frame — "cadre de descernement" in french)
class Mass(MassFunction):
    IGNORANCE_TOTALE = 0
    PROBA = 1
    POSSIB = 2
    GENERAL = 3
    CATEGORIQUE = 4
    def __init__(self, source, omega = None, normalize = False, index = None):
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

        if normalize:
            source = Mass.normaliser(source, index = index)
        s = 0.0
        for k,v in source.items():
            s += v
        if not source.get(omega, False) :
            source[omega] = 1 - s
        for s in source:
            try:
                self[s] = source[s]
            except Exception as e:
                if abs(source[s]) < 1/10**DECIMAL_PRECISTION:
                    self[s] = 0
                else:
                    raise e # raise hell


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

    def detect_type(self, return_str = True): 
        focals = {} # elements with mass ≠ 0
        for k,v in self.items():
            if round(v, DECIMAL_PRECISTION) > 0: focals[k] = v

        # cas triviale
        if self[self.frame()] == 1: # means m(Ω) = 1 
            return 'ignorance totale (masse du cadre de descernement = 1)' if return_str else IGNORANCE_TOTALE
        elif len(focals) == 1 and len(focals.keys()[0]) > 0: # one focal element (not ∅) must have mass = 1 
            return f"cadre catégorique, m({set_to_str(focals.keys()[0])}) = 1" if return_str else CATEGORIQUE

        # sort focal elements form smallest to biggest (to detect inclusion)
        items = sorted(focals.items(), key= lambda x : len(x[0]))
        probabiliste = True # until proven otherwise
        possibiliste = True # until proven otherwise

        for i,(s,v) in enumerate(items):
            if len(s) != 1:
                probabiliste = False # probabilist means all focal elements are singletons
            if i > 0 and not s.issuperset(items[i-1][0]):
                possibiliste = False # possibilist means elements are one inside the other (so if there are two different size, one must be inside the other)

        if probabiliste :
            return 'cadre probabiliste, toutes les elements focaux sont des singletons' if return_str else PROBA
        if possibiliste :
            return 'cadre possibiliste, les elements focaux sont emboités' if return_str else POSSIB
        # if none of the above is true, it's the general case
        return 'cadre général de la théorie des fonctions de croyance' if return_str else GENERAL

    def doubt(self, hypothesis = None):
        """
        calculates the doubt of a hypothesis, doubt(A) = 1 - bel(A), ∀A ⊂ Ω
        """
        if hypothesis is None:
            return {h:self.doubt(h) for h in powerset(self.core())}
        else:
            return 1 - self.bel(hypothesis)


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

    @staticmethod
    def normaliser(source, sum_of_weights = None, index = None):
        """
        if the sum of weights is greater than 1, the source will be normalized
        """
        if sum_of_weights is None:
            sum_of_weights = sum([v for k,v in source.items()])
        if index is None:
            index = dict(source)
        if sum_of_weights > 1:
            print('*'*100)
            print(f'la source {index}')
            print(f'a une somme de masses = {sum_of_weights}')
            print(f'normalisation de la source en divisant par {sum_of_weights} ...')
            print('*'*100)
            for s in source:
                source[s] /= sum_of_weights
        return source

    def __str__(self):
        text = ''
        for k,v in sorted(self.items(), key = lambda x : len(x[0])):
            if round(v, DECIMAL_PRECISTION) > 0.0:
                text += f'{set_to_str(k)} : {round(v,DECIMAL_PRECISTION)}\n'
        return text

    # def bel(self):
    #     beleifs = {}
    #     for s in self.all():
    #         for sub in self:
    #             if sub.issubset(s):
    #                 beleifs[s] = beleifs.get(s,0) + self[sub]
    #     return beleifs

    # def pl(self):
    #     plausibilities = {}
    #     for s in self.all():
    #         for sub in self:
    #             if s & sub:
    #                 plausibilities[s] = plausibilities.get(s,0) + self[sub]
    #     return plausibilities

class Sources(list):
    def __init__(self, omega):
        """
        use this class to combine multiple sources (having the same 'omega')
        """
        super().__init__()
        self.omega = str_to_set(omega)
        self.sources_affaiblis = set()

    def add(self, source, normalize = False):
        index = len(self) + 1 if normalize else None
        self.append(Mass(source, self.omega, normalize, index = index))

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
            text += str(s)
            text += f'>>> type = {s.detect_type()}\n\n'
        return text

    def show_source(self, source_index):
        print(f'resource {source_index+1} :')
        print(self[source_index])

    def combine(self, show_steps = False, conjonctive_only = True):
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
        result = Mass(s1, self.omega)
        if show_steps:
            m_type = result.detect_type()
            print(f'>>> type = {m_type}\n\n')
            best = sorted(result.items(), key= lambda x : x[1], reverse = True)[0]
            print(f"l'element le plus probable est : {set_to_str(best[0])}, avec masse = {round(best[1], DECIMAL_PRECISTION)}")  
        return result




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

def pritty_print(title):
    print(f"\n--- {title} ---------------------------\n")


def show_dict(dic, skip_null_values = False, show_count = False):
    i = 1
    for ensemble, bel in dic.items():
        if bel > 0.0 :
            count = str(i) if show_count else ''
            print(f'{count}- {set_to_str(ensemble)} : {round(bel,DECIMAL_PRECISTION)}'); i += 1
