from my_pyds import Sources, pritty_print, show_dict

def init(show = True):
    global sources # making sources public will help us in the presentation so we can import sources and simply print out the different stuff (interactive mode)
    # exercice 5
    # on écrit Ω comme étant des mots séparés par des virgules
    omega = 'processus_acc, transmission, stockage'

    # on stockes nos sources d'information dans une classe appelée 'Sources'
    sources = Sources(omega)
    sources.add({'processus_acc' : 0.38, 'transmission' : 0.55})
    sources.add({'stockage' : 0.88})
    sources.add({'processus_acc' : 1/3.0, 'transmission' : 1/3.0, 'stockage' : 1/3.0})

    # afficher les masses des sources
    if show: print(sources)
    return sources


def main():
    # afficher les beleifs et plaisibilités pour les trois experts
    for i,s in enumerate(sources):
        pritty_print(f'beleifs (non nuls) de l\'expert {i+1}')
        show_dict(s.bel(), skip_null_values = True)

        pritty_print(f'plausibilités (non nuls) du premier l\'expert {i+1}')
        show_dict(s.pl(), skip_null_values = True)

    # afficher les degres de doutes pour les trois experts
    for i,s in enumerate(sources):
        pritty_print(f'doutes (non nuls) de l\'expert {i+1}')
        show_dict(s.doubt(), skip_null_values = True)

    # combiner les sources (en ignorant celles avec m(Ω) = 1)
    pritty_print("combinaison des sources (commes rien n'est indiqué, les sources sont considérés fiables, et la combinaison de ces dérnier est faite en conjonction)")
    m = sources.combine(show_steps = True)


if __name__ == '__main__':
    init()
    main()