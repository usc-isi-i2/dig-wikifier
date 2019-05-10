# Redis Scripts

One of the key scripts used to load the data structures into redis is the populate_redis.py
It takes a dictionary structure and loads it into Redis into the appropriate type
Supports 4 operations
1. Store a json against a key
2. Store a  number(count) against a key
3. Store a Set against a key
4. delete a key

The above script can be used to load/unload a dictionary of numbers, lists, jsons etc

Sample usage -
## Load a dictionary of counts
```
python populate_redis.py -x localhost -p 6379 -d data.json -t NUMBER -v counts:
```
The above will store each key as
counts:key  and store the count as the value

## Load a dicitionary of lists as set
```
python populate_redis.py -x localhost -p 6379 -d data.json -t SET -v properties:
```

The above will store each key as
properties:key and store the list as a set in redis

## To Delete
let's say we want to delete the first counts dictionary we stored, we shall use the script the following way--
```
python populate_redis.py -x localhost -p 6379 -d data.json -t DEL -v counts:

This will delete all the keys in the dictionary that were stored as `counts:key` from Redis
```

## Wikifier baseline

This script uses the annotations.json file, to call the Wikifier service that we have in this repository to generate a baseline for the performance
These queries were manually annotated to the correct wikidata entities, the results of precision recall and F-1 scores are stored in the json and stored
in a new file

```
python wikifier_baseline.py
```

Must contain the annotations.json in the same directory
Set the host and port for redis in the script as well

