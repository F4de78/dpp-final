# dpp-final
DPP - "Anonymizing Transaction Databases for Publication" - AA 2022/23


## Links
- [Datasets](http://fimi.uantwerpen.be/data/)

## Dizionario
- (k,h,p)-coherence
  - k: praticamente la k di k-anon, numero minimo di ransazioni in ogni beta-cohort
  - h: percentuale di transazioni che condividono elementi privati rispetto a k
  - p: numero di elementi pubblici considerati in ogni sottoinsieme beta, prior attaccante sa alcune tue transazioni
  - l'attaccante puo ricondursi in due modi:
    - 1/k probabilità
    - l'attaccante ha probabilità h a partire da un private item 
- beta-cohort: insieme di transazioni che hanno come attributi tutti gli elementi di p
