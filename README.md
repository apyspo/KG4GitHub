# KG4GitHub

KG4GCR is a knowledge graph of github repositories and linked contributors, using libraries and similar topics of repositories used for recommending new team contributors which has similar skills and interests

For source data "statements.tsv" ~400MB file you can download from below link and add into your google drive so that you can mount to KG4GCR.ipynb

https://drive.google.com/file/d/1zCUwXQjl4u4DtPAgi1MRqQU7SCXgL9-I/view?usp=sharing

getdatafromgithub.py                : Python script file which is used to access GitHub API and extract data for requested repositories.
dict_rep_libs.json                  : Python script stores repository related extracted data in append mode in this json file for all requested repositories.
dict_repositories.json              : List of repositories in json format for getdatafromgithub.py to start processsing one by one.
dict_repositories_notprocessed.json : If python script fails due to API limits and halts, stores remaining list of repositories not processed in this file.
dict_repositories.json.bak          : Initial full list of repositories backup to reuse and copy to dict_repositories whenever needed.
github_json_mapping_contributor.ttl : RML mapping file to be used with rmlmapper.jar to convert json to contout.nt (n-triples of contributors) both using same source dict_rep_libs.json 
github_json_mapping_repository.ttl  : RML mapping file to be used with rmlmapper.jar to convert json to repout.nt (n-triples of repositories) both using same source dict_rep_libs.json
contout.nt                          : N-triples file contains contributor data
repout.nt                           : N-triples file contains repository data
kg4gcr.nt                           : Union of contout.nt and repout.nt for knowledge graph 
SPARQLQueryForTeamMate(P1327).sparql: SPARQL query for consturcting and inserting wdp:P1327 (team member) predicates if both contributor working on the same repository they considered as team-mate. 
KG4GCR.ipynb                        : Google colab python notebook file which includes all functions to process statements.tsv file on google drive https://drive.google.com/file/d/1zCUwXQjl4u4DtPAgi1MRqQU7SCXgL9-I/view?usp=sharing
meta.jsonld                         : Metadata description in schema.org context
