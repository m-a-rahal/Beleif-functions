# Execution Results (exercice4.py)
    ****************************************************************************************************
    la source 3
    a une somme de masses = 1.05
    normalisation de la source en divisant par 1.05 ...
    ****************************************************************************************************
    masses de la source 1 :
    {énergies_fossiles} : 0.4
    {transport} : 0.45
    {centrales_therm} : 0.15
    {chauff_bois, transport, énergies_fossiles, centrales_therm, naturel} : 0.0
    
    masses de la source 2 :
    {transport} : 0.75
    {chauff_bois, transport, énergies_fossiles, centrales_therm, naturel} : 0.25
    
    masses de la source 3 :
    {transport} : 0.33333
    {centrales_therm} : 0.47619
    {chauff_bois} : 0.17143
    {naturel} : 0.01905
    {chauff_bois, transport, énergies_fossiles, centrales_therm, naturel} : 0.0
    
    
    
    --- beleifs (non nuls) du premier expert  ---------------------------
    
    + {centrales_therm} : 0.15
    + {transport} : 0.45
    + {énergies_fossiles} : 0.4
    + {centrales_therm, transport} : 0.6
    + {centrales_therm, énergies_fossiles} : 0.55
    + {transport, énergies_fossiles} : 0.85
    + {centrales_therm, transport, énergies_fossiles} : 1.0
    
    --- plausibilités (non nuls) du premier expert  ---------------------------
    
    + {centrales_therm} : 0.15
    + {transport} : 0.45
    + {énergies_fossiles} : 0.4
    + {centrales_therm, transport} : 0.6
    + {centrales_therm, énergies_fossiles} : 0.55
    + {transport, énergies_fossiles} : 0.85
    + {centrales_therm, transport, énergies_fossiles} : 1.0
    
    --- combinaison des sources (commes rien n'est indiqué, les sources sont considérés fiables, et la combinaison de ces dérnier est faite en conjonction) ---------------------------
    
    combinaison 1 :
    k = 0.4125, 1/(1-k) = 1.70213
    {énergies_fossiles} : 0.17021
    {transport} : 0.76596
    {centrales_therm} : 0.06383
    {chauff_bois, transport, énergies_fossiles, centrales_therm, naturel} : 0
    
    combinaison 2 :
    k = 0.71429, 1/(1-k) = 3.5
    {transport} : 0.89362
    {centrales_therm} : 0.10638
    {chauff_bois, transport, énergies_fossiles, centrales_therm, naturel} : 0
    
    
    --- après combinaison ---------------------------
    
    {transport} : 0.89362
    {centrales_therm} : 0.10638
    {chauff_bois, transport, énergies_fossiles, centrales_therm, naturel} : 0

    [Finished in 1.9s]


'''
# Conclusion
le cause la plus probable de la pollution de l'air est les moyens de transport avec une probabilité de 89.362% (cadre probabiliste, car toutes éléments focaux sont des singletons)