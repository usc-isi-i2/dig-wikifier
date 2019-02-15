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

