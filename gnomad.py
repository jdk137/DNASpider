import requests
import json
import re

# c.*30G>T multiresult

# qStr = "NM_000546.5(TP53):c.*30G>T,"  # 2 af

qStr = "NM_000546.5(TP53):c.1135C>T,p.Arg379Cys"


match = re.match( r'.*\((.*)\)\:(.*)\,(.*)', qStr);

gene = match.group(1) # "TP53"
variant = match.group(2) # "c.*30G>T" # "c.524G>A"
protein = match.group(3) # "" # "p.R175H"

#print(gene, variant, protein)


referenceGenome = "GRCh37"

datasetId = "gnomad_r2_1" #"gnomad_r3" # 


ensemblId = "ENSG00000141510" # ENSG00000141510


#variantId = "17-7579801-G-C" #"17-7578115-T-C"

# 获取ensemble ID
def getEn ():
  global gene

  en = "";

  url = "http://gnomad-sg.org/api/"

  query = """
          query GeneSearch($query: String!, $referenceGenome: ReferenceGenomeId!) {
            gene_search(query: $query, reference_genome: $referenceGenome) {
              ensembl_id
              symbol
            }
          }
  """

  variables = {
    "query": gene,
    "referenceGenome": referenceGenome # "GRCh37"
  }

  payload = json.dumps({
    "query": query,
    "variables": variables
  })

  headers = {
    'content-type': 'application/json',
    'Accept-Encoding': 'gzip, deflate, br',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'accept': '*/*',
  }

  response = requests.request("POST", url, headers=headers, data = payload)

  # print(response.content.decode())

  # print(response.json())

  # print(type(response.json()))
  # print(type(response.content))

  for g in response.json()["data"]["gene_search"]:
      # print(g)
      if g["symbol"] == gene:
          en = g["ensembl_id"]



  # print(en)

  return en


# ensemblId = getEn()

# print(ensemblId)

# 获取variant_id
def getV ():
  global ensemblId
  url = "http://gnomad-sg.org/api/"

  query = """

    query VariantsInGene($geneId: String!, $datasetId: DatasetId!, $referenceGenome: ReferenceGenomeId!) {
      meta {
        clinvar_release_date
      }
      gene(gene_id: $geneId, reference_genome: $referenceGenome) {
        clinvar_variants {
          clinical_significance
          clinvar_variation_id
          gnomad {
            exome {
              ac
              an
              filters
            }
            genome {
              ac
              an
              filters
            }
          }
          gold_stars
          hgvsc
          hgvsp
          in_gnomad
          major_consequence
          pos
          review_status
          transcript_id
          variant_id
        }
        variants(dataset: $datasetId) {
          consequence
          flags
          hgvs
          hgvsc
          hgvsp
          lof
          lof_filter
          lof_flags
          pos
          rsids
          transcript_id
          variant_id
          exome {
            ac
            ac_hemi
            ac_hom
            an
            af
            filters
            populations {
              id
              ac
              an
              ac_hemi
              ac_hom
            }
          }
          genome {
            ac
            ac_hemi
            ac_hom
            an
            af
            filters
            populations {
              id
              ac
              an
              ac_hemi
              ac_hom
            }
          }
          lof_curation {
            verdict
            flags
          }
        }
      }
    }
  """

  variables = {
    "datasetId": datasetId, # "gnomad_r2_1",
    "geneId": ensemblId, # ENSG00000141510
    "referenceGenome": referenceGenome # "GRCh37";
  }

  payload = json.dumps({
    "query": query,
    "variables": variables
  })

  headers = {
    'content-type': 'application/json',
    'Accept-Encoding': 'gzip, deflate, br',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'accept': '*/*',
  }

  response = requests.request("POST", url, headers=headers, data = payload)

  # print(response.content.decode())

  #print(response.json())

  # return

  # print(type(response.json()))
  # print(type(response.content))

  vs = response.json()["data"]["gene"]["variants"];
  fvs = [];
  v_id = [];

  # 照搬了网页中代码逻辑
  for v in vs:
      # print(g)
      if v["exome"] and len(v["exome"]["filters"]) != 0 :
        v["exome"] = ''
        #print(v)
      if v["genome"] and len(v["genome"]["filters"]) != 0 :
        v["genome"] = ''
        #print(v)
      if v["exome"] or v["genome"]:
        fvs.append(v)

  # print(len(vs))
  # print(len(fvs))

  for fv in fvs:
    if (fv["hgvs"] == (protein or variant)) and fv["hgvsc"] == variant:
      #print(protein, variant, fv["hgvs"], fv["hgvsc"])
      #print(fv)
      v_id.append(fv["variant_id"])

  return v_id

  #return 0 #v_id[0]


# print(getV())
# 获取东亚变异频率
def getAf (variantId):
  url = "http://gnomad-sg.org/api/"

  query = """
    query GnomadVariant($variantId: String!, $datasetId: DatasetId!, $referenceGenome: ReferenceGenomeId!, $includeLiftoverAsSource: Boolean!, $includeLiftoverAsTarget: Boolean!) {
      variant(variantId: $variantId, dataset: $datasetId) {
        variant_id
        reference_genome
        chrom
        pos
        ref
        alt
        colocated_variants
        multi_nucleotide_variants {
          combined_variant_id
          changes_amino_acids
          n_individuals
          other_constituent_snvs
        }
        exome {
          ac
          an
          ac_hemi
          ac_hom
          faf95 {
            popmax
            popmax_population
          }
          filters
          populations {
            id
            ac
            an
            ac_hemi
            ac_hom
          }
          age_distribution {
            het {
              bin_edges
              bin_freq
              n_smaller
              n_larger
            }
            hom {
              bin_edges
              bin_freq
              n_smaller
              n_larger
            }
          }
          quality_metrics {
            allele_balance {
              alt {
                bin_edges
                bin_freq
                n_smaller
                n_larger
              }
            }
            genotype_depth {
              all {
                bin_edges
                bin_freq
                n_smaller
                n_larger
              }
              alt {
                bin_edges
                bin_freq
                n_smaller
                n_larger
              }
            }
            genotype_quality {
              all {
                bin_edges
                bin_freq
                n_smaller
                n_larger
              }
              alt {
                bin_edges
                bin_freq
                n_smaller
                n_larger
              }
            }
            site_quality_metrics {
              metric
              value
            }
          }
        }
        genome {
          ac
          an
          ac_hemi
          ac_hom
          faf95 {
            popmax
            popmax_population
          }
          filters
          populations {
            id
            ac
            an
            ac_hemi
            ac_hom
          }
          age_distribution {
            het {
              bin_edges
              bin_freq
              n_smaller
              n_larger
            }
            hom {
              bin_edges
              bin_freq
              n_smaller
              n_larger
            }
          }
          quality_metrics {
            allele_balance {
              alt {
                bin_edges
                bin_freq
                n_smaller
                n_larger
              }
            }
            genotype_depth {
              all {
                bin_edges
                bin_freq
                n_smaller
                n_larger
              }
              alt {
                bin_edges
                bin_freq
                n_smaller
                n_larger
              }
            }
            genotype_quality {
              all {
                bin_edges
                bin_freq
                n_smaller
                n_larger
              }
              alt {
                bin_edges
                bin_freq
                n_smaller
                n_larger
              }
            }
            site_quality_metrics {
              metric
              value
            }
          }
        }
        flags
        lof_curations {
          gene_id
          gene_symbol
          verdict
          flags
          project
        }
        rsids
        transcript_consequences {
          gene_id
          gene_version
          gene_symbol
          hgvs
          hgvsc
          hgvsp
          is_canonical
          is_mane_select
          is_mane_select_version
          lof
          lof_flags
          lof_filter
          major_consequence
          polyphen_prediction
          sift_prediction
          transcript_id
          transcript_version
        }
        in_silico_predictors {
          id
          value
          flags
        }
      }

      clinvar_variant(variant_id: $variantId, reference_genome: $referenceGenome) {
        clinical_significance
        clinvar_variation_id
        gold_stars
        last_evaluated
        review_status
        submissions {
          clinical_significance
          conditions {
            name
            medgen_id
          }
          last_evaluated
          review_status
          submitter_name
        }
      }

      liftover(source_variant_id: $variantId, reference_genome: $referenceGenome) @include(if: $includeLiftoverAsSource) {
        liftover {
          variant_id
          reference_genome
        }
        datasets
      }

      liftover_sources: liftover(liftover_variant_id: $variantId, reference_genome: $referenceGenome) @include(if: $includeLiftoverAsTarget) {
        source {
          variant_id
          reference_genome
        }
        datasets
      }

      meta {
        clinvar_release_date
      }
    }

  """

  variables = {
    "datasetId": datasetId, # "gnomad_r2_1",
    "includeLiftoverAsSource": bool(1),
    "includeLiftoverAsTarget": bool(0),
    "referenceGenome": referenceGenome, # "GRCh37",
    "variantId": variantId # "17-7578115-T-C"
  }

  # print(json.dumps(variables));

  payload = json.dumps({
    "query": query,
    "variables": variables
  })

  headers = {
    'content-type': 'application/json',
    'Accept-Encoding': 'gzip, deflate, br',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'accept': '*/*',
  }

  response = requests.request("POST", url, headers=headers, data = payload)

  # print(response.content.decode())

  # print(response.json())

  # return

  #print(type(response.json()))

  # print(type(response.content))

  vs = response.json()["data"]["variant"];

  ac = 0;
  an = 0;
  af = 0;

  # print(vs["exome"]);
  # print(vs["genome"]);

  # 照搬了网页中代码里的逻辑
  if vs["exome"] and vs["exome"]["populations"] and (len(vs["exome"]["populations"]) > 0) :
    for r in vs["exome"]["populations"]:
      if r["id"] == 'eas' :
        ac += r["ac"]
        an += r["an"]

  if vs["genome"] and vs["genome"]["populations"] and (len(vs["genome"]["populations"]) > 0) :
    for r in vs["genome"]["populations"]:
      if r["id"] == 'eas' :
        ac += r["ac"]
        an += r["an"]

  if an == 0:
    af = 0
  else :
    af = '%.4f' % (ac / an);

  return af;

# print(getAf(variantId))

def queryGnomad (qStr, refeGenome, dataset) :
  global gene, variant, protein, referenceGenome, datasetId

  if qStr :
    match = re.match( r'.*\((.*)\)\:(.*)\,(.*)', qStr);

    gene = match.group(1) # "TP53"
    variant = match.group(2) # "c.*30G>T" # "c.524G>A"
    protein = match.group(3) # "" # "p.R175H"

  if refeGenome :
    referenceGenome = refeGenome

  if dataset :
    datasetId = dataset

  # print(gene, variant, protein)

  out = '';
  if not gene :
    out = 'no gene'
    return out

  ensemblId = getEn()
  if not ensemblId :
    out = 'no gene'
    return out

  out = '\nensemblId: ' + ensemblId;

  v_ids = getV()

  if len(v_ids) == 0 :
    out += '\nno variant'
    return out

  for vId in v_ids:
    out += '\n' + vId + '\neast asion frequency: ' + getAf(vId)

  return out

#print(queryGnomad())




