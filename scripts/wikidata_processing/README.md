# Wikidata Pre-Processing
This folder contains several scripts, each aimed at computing a specific data structure from the json dumps of Wikidata. Shall describe briefly what each script
does and how to use those scripts

## Compute the labels of each Qnode
To extract all labels of each qnode, we shall use the script label_map_gen.py

```
python label_map_gen.py -w path_to_wikidata.gz -l output.json
```
This file will output a dictionary who's key is the Qnode ID and the values are the labels for that Qnode. currently extracts all languages that are specified
inside the script. Check comments in script for more info on languages to extract

## Compute neighbors map
To extract all the edge information with properties, we have a script that does exactly that from Wikidata

```
python compute_neighbors.py -w wikidata_dump.gz -o outfile.json
```

The outfile.json will look like the following -
```
{
    "Q123" : {
            "P12" : ["Q124", "Q125", "Q126"] ,
            "P25" : ["Q100", "Q10201"]
            .
            .
            .
            .
    }
    .
    .
    .
    .

}
```

And also it will contain the entire 56+ million entities in Wikidata along with their edges.
**Note: This script only extracts properties that connect two Qnodes in Wikidata. There are several other properties in Wikidata that point to constants, but for the purpose of our analysis and experiments, we limited ourselves to edges between two Qnodes**

## Compute occurance of label-to-Qnode counts
This script is used to compute number of times a specific label and qnode are being referenced within the wikidata ontology. This is used as a reference for transition
probability within the Wikifier service.

```
python compute_label_node_count.py -l label_map.json -o outfile.json -w wikidatapath.gz
```

**Note that this file requires the label_map generated as input to extract the counts**


## Compute properties of Qnodes
This script is used to compute all properties of Wikidata or only a specific whitelist if present for each Qnode

Usage -
```
python compute_properties_wikidata.py -o outputfile.json -w wikidatapath.gz -a allowed_file
```

The allowed file must look like -

```
http://wikidata.org/wiki/P31
.
.
```

It will extract the properties and create a whitelist.
If the file is empty it will generate a property map that lists all properties for each Qnode in Wikidata.

The generated output should look like

```
{
    "Q123" : ["P31", "P252", . . . . . ],
    .
    .
    .

}
```

## Edge pruning
This script has been used to take the neighbor map produced by compute_neighbors.py and reduce it to a subgraph. It takes a list of nodes
as whitelist, and retains only edges that connect any two nodes that are present in the whitelist. This way we get a neat subgraph of just
the nodes and edges we want to inspect.

```
python edge_prune.py -d neighbor_map.json -w whitelistfile -o output.json
```

Whitelist file must look like the following (Each line representing one qnode) -
```
http://wikidata.org/wiki/Q123
.
.
```

**Note : All these files are extremely large and will take a lot of memory to process. If you're trying this on your local machine with entire wikidata, that would be extremely bad idea. Please use a machine with large enough ram or work with smaller subsets of the ontology. If not, load the wikdata into a secondary structure like MySQL or MongoDB and then repurpose the scripts to work using these secondary structures.**

