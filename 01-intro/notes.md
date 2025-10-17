# Introduction

## RAG

RAG = Retrieval Augmented Generation

* Retrieval = Search
* Generation = LLM

## ElasticSearch

Persistent search engine.
An index Elastic Search (ES) is like a table in a relational DB.

Run elasticsearch:

* Download container

    ```bash
    docker run -it \
        --rm \
        --name elasticsearch \
        -m 4GB \
        -p 9200:9200 \
        -p 9300:9300 \
        -e "discovery.type=single-node" \
        -e "xpack.security.enabled=false" \
        docker.elastic.co/elasticsearch/elasticsearch:8.4.3
    ```

* Forward ports `9200` and `9300`

* Test with curl:

    ```bash
    curl http://localhost:9200
    ```

### Troubleshooting

If Elasticsearch exits unexpectedly, it's likely due to Java heap memory configuration. Use this command instead:

```bash
docker run -d \
    --name elasticsearch \
    -m 4GB \
    -p 9200:9200 \
    -p 9300:9300 \
    -e "discovery.type=single-node" \
    -e "xpack.security.enabled=false" \
    -e "ES_JAVA_OPTS=-Xms512m -Xmx512m" \
    docker.elastic.co/elasticsearch/elasticsearch:8.4.3
```

The `ES_JAVA_OPTS=-Xms512m -Xmx512m` parameter limits the Java heap size to 512MB, preventing memory allocation issues.

Check cluster health:

```bash
curl http://localhost:9200/_cluster/health?pretty
```
