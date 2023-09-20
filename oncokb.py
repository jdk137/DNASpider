
#https://www.oncokb.org/api/private/search/variants/clinical?hugoSymbol=TP53

#drugs



#https://www.oncokb.org/api/private/utils/variantAnnotation?hugoSymbol=TP53&referenceGenome=GRCh37&alteration=S121F


import requests
import json
import re

gene = "TP53"
variant = 'R175H' # match.group(3) # "" # "p.R175H"
referenceGenome = 'GRCh37'


  # get gene
headers = {
  'content-type': 'application/json',
  'authorization': '' #authorization: Bearer ad64ec18-aaa1-418d-9ca5-ab5857c12ab2
}

# 获取token令牌
def getToken ():

  # get token
  tokenUrl = 'https://www.oncokb.org/gene/TP53'
  response = requests.request("GET", tokenUrl)
  # print(response.text)

  lines = response.text.split('\n')
  # Online Python - IDE, Editor, Compiler, Interpreter
  for l in lines: 
    match = re.match(r'.*window\.serverConfig\.token\ \=\ \"(.*?)\"', l)
    #print(match) 
    if match:
      token = match.group(1)
      # print(token) 
  # print(match)
  return token



# getGene
def getGene (gene):
  #https://www.oncokb.org/api/v1/genes/lookup?query=TP63
  #oncogene, tsg
  #Oncogene, Tumor Suppressor

  url = "https://www.oncokb.org/api/v1/genes/lookup?query=" + gene;

  response = requests.request("GET", url, headers=headers)
  # print(response.content.decode())

  # print(response.json())

  genes = response.json()

  r = None

  for g in genes:
    if g["hugoSymbol"] == gene:
      r = g

  return r


# getTheraps
def getTheraps (gene):

  url = "https://www.oncokb.org/api/private/search/variants/clinical?hugoSymbol=" + gene;

  response = requests.request("GET", url, headers=headers)
  # print(response.content.decode())

  # print(response.json())

  theraps = response.json()

  r = []

  for t in theraps:
    if len(t["drug"]) > 0:
      r.append(t)

  return r

# getVariant
def getVariant (gene, variant):

  url = "https://www.oncokb.org/api/private/utils/variantAnnotation?hugoSymbol=" + gene + "&referenceGenome=" + referenceGenome + "&alteration=" + variant;

  response = requests.request("GET", url, headers=headers)
  # print(response.content.decode())

  # print(response.json())

  vInfo = response.json()

  return vInfo


def getOncokb (gene, variant):

  token = getToken()
  if not token:
    out = 'get token fail'
    return out

  if token :
    headers["authorization"] = 'Bearer ' + token


  g = getGene(gene)
  if not g:
    out = 'no gene'
    return out
  else:
    out = gene
    if g["oncogene"] or g["tsg"]:
      out += "\n"
      out += 'Oncogene; ' if g["oncogene"] else ''
      out += 'Tumor Suppressor' if g["tsg"] else ''


  theraps = getTheraps(gene)
  if len(theraps) == 0:
    out += '\n no therap'
  else :
    out += '\nLevel\tAlterations\tLevel-associated cancer types\tDrugs\tCitations'
    for t in theraps:
      out += '\n' + '\t'.join([t['level'], t['variant']['alteration'], t['cancerTypes'][0]['mainType'], ' '.join(t['drug']), str(len(t['drugAbstracts'])) ])


  if variant == '':
    return out
  v = getVariant(gene, variant)
  out += '\n' + gene + ' ' + variant
  out += '\noncogenic\tknownEffect\tPrognostic_Level\tDiagnostic_Level'
  out += '\n' + '\t'.join([
      v["oncogenic"],
      v["mutationEffect"]["knownEffect"],
      v["highestPrognosticImplicationLevel"] or '',
      v["highestDiagnosticImplicationLevel"] or ''
    ])
  out += '\n' + v["mutationEffect"]["description"]

  return out

#print(getOncokb('TP53', 'R249W'))






