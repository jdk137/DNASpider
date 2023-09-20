import requests
import json
import re

from gnomad import queryGnomad
from tp53 import getTAFunc
from hotspot import getSpot
from oncokb import getOncokb

# c.*30G>T multiresult

# qStr = "NM_000546.5(TP53):c.*30G>T,"  # 2 af

#qStr = "NM_000546.5(TP53):c.1135C>T,p.Arg379Cys"
qStr = [
  "NM_000546.5(TP53):c.524G>A,p.R175H",
  "NM_000546.5(TP53):c.844C>T,p.R282W",
  "NM_001098210.2(CTNNB1):c.1004A>T,p.K335I",
  "NM_001982.3(ERBB3):c.850G>A,p.G284R",
  "NM_000546.5(TP53):c.1135C>T,p.Arg379Cys",
  "NM_000546.5(TP53):c.*30G>T,"][5]

def querySingle (qStr):

  match = re.match( r'.*\((.*)\)\:(.*)\,(.*)', qStr);

  gene = match.group(1) # "TP53"
  variant = match.group(2) # "c.*30G>T" # "c.524G>A"
  protein = match.group(3) # "" # "p.R175H"
  residue = re.match(r'[A-Z]*[0-9]*', protein.split('.')[1]).group() if protein else ''
  oncokbP = protein.split('.')[1] if protein else ''

  #print(gene, variant, protein, residue, oncokbP)

  referenceGenome = "GRCh37"
  datasetId = "gnomad_r2_1" # "gnomad_r3" # 


  out = '========= ' + qStr + ' ==========='
  gnomadResult = queryGnomad(qStr, referenceGenome, datasetId)
  out += '\n' + gnomadResult
  print(out)

  if gene == 'TP53':
    variantResult = getTAFunc(variant)
    print('\n' + variantResult)
    out += '\n\n' + variantResult

  spotResult = getSpot(gene, residue)
  print('\n' + spotResult)
  out += '\n\n' + spotResult


  oncokbResult = getOncokb(gene, oncokbP)
  print('\n' + oncokbResult)
  out += '\n\n' + oncokbResult

  return out

#querySingle(qStr)
