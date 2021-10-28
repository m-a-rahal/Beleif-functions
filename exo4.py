from my_pyds import Sources, pritty_print, show_dict

def init(show = True):
    global sources # making sources public will help us in the presentation so we can import sources and simply print out the different stuff (interactive mode)
    # exercice 4
    # on écrit Ω comme étant des mots séparés par des virgules
    omega = 'énergies_fossiles, transport, centrales_therm, chauff_bois, naturel'

    # on stockes nos sources d'information dans une classe appelée 'Sources'
    sources = Sources(omega)
    sources.add({'énergies_fossiles' : 0.40, 'transport' : 0.45, 'centrales_therm' : 0.15})
    sources.add({'transport' : 0.75})
    # ajout et normalisation de la 3ème source (somme des masses = 1.05 > 1)
    sources.add({'transport' : 0.35, 'centrales_therm' : 0.5, 'chauff_bois' : 0.18, 'naturel' : 0.02}
    , normalize = True)

    # afficher les masses des sources
    if show: print(sources)
    return sources


def main():
    # afficher les beleifs et plaisibilités pour la première source (premier expert)
    pritty_print('beleifs (non nuls) du premier expert ')
    show_dict(sources[0].bel(), skip_null_values = True)

    pritty_print('plausibilités (non nuls) du premier expert ')
    show_dict(sources[0].pl(), skip_null_values = True)

    # combiner les sources (en ignorant celles avec m(Ω) = 1)
    pritty_print("combinaison des sources (commes rien n'est indiqué, les sources sont considérés fiables, et la combinaison de ces dérnier est faite en conjonction)")
    m = sources.combine(show_steps = True)
    pritty_print('après combinaison')
    print(m)

if __name__ == '__main__':
    init()
    main()