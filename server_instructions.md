# Server instructions


## Server instructions for running DBpedia-spotlight docker
1. Clone DBPedia splotight docker to a location
``` git clone https://github.com/dbpedia-spotlight/spotlight-docker.git ```
2. Replace the paths to the release server(the env vars mentioned below) in the docker file for the version you want to run -

For example, I changed the variables in spotlight-docker/v1.0/english/Dockerfile

```

ENV RELEASE_SERVER    cfhcable.dl.sourceforge.net/project/dbpedia-spotlight
ENV RELEASE_FILENAME  dbpedia-spotlight-1.0.0.jar
ENV LANGUAGE_MODEL    en_2+2.tar.gz

```

3. To run do the following :
```
Assume your docker host is localhost and HTTP public port is 2222 (change these values if you need).

Run

    docker build -f Dockerfile  -t english_spotlight .

and finally

    docker run -i -p 2222:80 english_spotlight spotlight.sh
```

The current deployment of DBPedia is located at `/lfs1/DBpedia/spotlight-docker/` on minds server

To clear the logs, use the following command  as root user -

```
echo "" > $(docker inspect --format='{{.LogPath}}' docker_container_id)
```

## Server instructions for Wikidata/ Wikifier service -

The current wikidata is located at `/lfs1/wikidata`

The backups folder has a copy of all the data files, especially the file dump in case we need it.
The main wikidata json dump file is wikidata.gz. All pre-processing scripts read this wikidata.gz file to compute the information
needed.

The redis server is located in the `/lfs1/wikidata/redis` folder. There is a script to start the redis server. This redis server has BGSAVE
so its data will be persisted in disk in case of unexpected shutdowns.
Redis config file - redis/redis-5.0.0/config/6379.conf

## To run wikifier
1. Activate the virtual env - wikifier
2. Go to `/lfs1/wikidata/wikifier/` and execute `run_wikifier.sh`

the log for the service is written to `wiki.log`

# To setup wikifier (From scratch)
We require 3 key data structures to get the wikifier up and running.
First setup the env as mentioned in the [README](https://github.com/usc-isi-i2/dig-wikifier/tree/master)
**Note: If some dependencies were missed, install them as the errors pop-up**

Data structures that will be required in redis -
1. Candidates map
2. Labels for each qnode
3. Label-count map

Embeddings that will be required - One of **VERSE/TransX Embeddings**

## What is candidate map and how to generate Candidates map?
It is a dictionary structure used in the wikifier. The keys are labels and the values are a list of Qnodes that possess that exact label
We use this as a secondary trie, by loading it to redis and pointing a modified version of etk extractor to this redis.
Compute the data using script mentioned [here](https://github.com/usc-isi-i2/dig-wikifier/tree/master/scripts/wikidata_processing)

Also the script to directly generate it can be run as follows -

```
python glossary_label_map_gen.py -w wikidatapth.gz -l candidatemap.json -g glossaryout.txt
```


Once the labels are extracted, generate a reverse mapping of label-to-Qnodes using that dictionary and load that into redis as -
```
python populate_redis.py -x localhost -p 6379 -d candidatemap.json -t SET -v ""

Note: Do not enter any prefix here
```
This should load the label map gen into redis


## Labels for each node
The labels for each qnode can be constructed using the following script -
```
python label_map_gen.py -w path_to_wikidata.gz -l label_map.json
```

Load the label map into redis as follows -
```
python populate_redis.py -x localhost -p 6379 -d label_map.json -t SET -v "lbl:"

Note: Prefix is - "lbl:"
```

## Label count map
Now We can again use the script mentioned [here](https://github.com/usc-isi-i2/dig-wikifier/tree/master/scripts/wikidata_processing) to
compute label-to-Qnode count dictionary
We can then load that dictionary to redis as -
```
python populate_redis.py -x localhost -p 6379 -d label_count.json -t SET -v ""
```

Again no prefix here, the keys will be of the form `Donald Trump:Q22686` and value as `56` and so on

Once we load these three data structures into redis into the right keyspaces we are good to proceed to the last step of the setup

## Loading the embedding.
Store the embeddings in one of the locations and pass the location in the `wikifier.cfg` file. Ensure to set the properties correctly
before trying to start the service using `run_wikifier.sh`

Current properties can be found [here](https://github.com/usc-isi-i2/dig-wikifier/blob/master/wikifier/wikifier.cfg)
The config file is `wikifier/wikifier.cfg`

Once all the above steps have been completed, we can proceed to run the starter script `run_wikifier.sh` which should start the service on the
specified port in the config


Currently the files are stored in the following locations -
## Embeddings
Embeddings are located on minds03 server at `/lfs1/wikidata/wikifier/embeddings` folder. The are other embeddings that have been generated
and are located at `/lfs1/embeddings` folder

## The service
The service that has the code synced with this repository is located at `/lfs1/wikidata` folder

## Redis setup
If you have queries regarding redis server setup, refer [this](https://github.com/usc-isi-i2/dig-wikifier/blob/master/scripts/REDIS.md)