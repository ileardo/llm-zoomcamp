# Vector Search

Vector search goes beyond traditional keyword matching by using numerical embeddings to measure semantic similarity between pieces of data. This allows it to understand context and meaning, enabling accurate retrieval across text, images, audio, and other modalities, even when keywords or exact phrasing are missing.

## Qdrant

[Qdrant](https://qdrant.tech/) is an open-source vector search engine, a dedicated solution built in Rust for scalable vector search.

Run in Docker:

```bash
docker pull qdrant/qdrant

docker run -p 6333:6333 -p 6334:6334 \
   -v "$(pwd)/qdrant_storage:/qdrant/storage:z" \
   qdrant/qdrant
```
