# How-To: Search Documents

`ragbits-document-search` package comes with all functionalities required to perform document search. The whole process can be divided into 3 steps:
1. Load documents
2. Process documents, embedd them and store into the vector database
3. Do the search

This guide will walk you through all those steps and explain the details. Let's start with a minimalistic example to get the main idea:

```python
import asyncio
from pathlib import Path

from ragbits.core.embeddings.litellm import LiteLLMEmbedder
from ragbits.core.vector_stores.in_memory import InMemoryVectorStore
from ragbits.document_search import DocumentSearch
from ragbits.document_search.documents.document import DocumentMeta
from ragbits.document_search.documents.sources import GCSSource


async def main() -> None:
    # Load documents (there are multiple possible sources)
    documents = [
        DocumentMeta.from_local_path(Path("<path_to_your_document>")),
        DocumentMeta.create_text_document_from_literal("Test document"),
        DocumentMeta.from_source(GCSSource(bucket="<your_bucket>", object_name="<your_object_name>"))
    ]

    embedder = LiteLLMEmbedder()
    vector_store = InMemoryVectorStore(embedder=embedder)
    document_search = DocumentSearch(
        vector_store=vector_store,
    )

    # Ingest documents - here they are processed, embed and stored
    await document_search.ingest(documents)

    # Actual search
    results = await document_search.search("I'm boiling my water and I need a joke")
    print(results)


if __name__ == "__main__":
    asyncio.run(main())
```

## Documents loading
Before doing any search we need to have some documents that will build our knowledge base. Ragbits offers a handy class [`Document`][ragbits.document_search.documents.document.Document] that stores all the information needed for document loading.
Objects of this class are usually instantiated using [`DocumentMeta`][ragbits.document_search.documents.document.DocumentMeta] helper class that supports loading files from your local storage, GCS or HuggingFace.
You can easily add support for your custom sources by extending the [`Source`][ragbits.document_search.documents.sources.Source] class and implementing the abstract methods:

```python
from pathlib import Path

from ragbits.document_search.documents.sources import Source


class CustomSource(Source):
    @property
    def id(self) -> str:
        pass

    async def fetch(self) -> Path:
        pass
```

## Processing, embedding and storing
Having the documents loaded we can proceed with the pipeline. The next step covers the processing, embedding and storing. Embedders and Vector Stores have their own sections in the documentation, here we will focus on the processing.

Before a document can be ingested into the system it needs to be processed into a collection of elements that the system supports. Right now there are two supported elements:
`TextElement` and `ImageElement`. You can introduce your own elements by simply extending the [`Element`][ragbits.document_search.documents.element.Element] class.

Depending on a type of the document there are different `providers` that work under the hood to return a list of supported elements. Ragbits rely mainly on [Unstructured](https://unstructured.io/)
library that supports parsing and chunking of most common document types (i.e. pdf, md, doc, jpg). You can specify a mapping of file type to provider when creating document search instance:
```python
from ragbits.core.embeddings.litellm import LiteLLMEmbedder
from ragbits.core.vector_stores.in_memory import InMemoryVectorStore
from ragbits.document_search import DocumentSearch
from ragbits.document_search.ingestion.parsers.router import DocumentParserRouter
from ragbits.document_search.documents.document import DocumentType
from ragbits.document_search.ingestion.parsers.unstructured.default import UnstructuredDocumentParser

embedder = LiteLLMEmbedder()
vector_store = InMemoryVectorStore(embedder=embedder)
document_search = DocumentSearch(
    vector_store=vector_store,
    parser_router=DocumentParserRouter({DocumentType.TXT: UnstructuredDocumentParser()})
)
```

If you want to implement a new provider you should extend the [`DocumentParser`][ragbits.document_search.ingestion.parsers.base.DocumentParser] class:
```python
from ragbits.document_search.documents.document import DocumentMeta, DocumentType
from ragbits.document_search.documents.element import Element
from ragbits.document_search.ingestion.parsers.base import DocumentParser


class CustomProvider(DocumentParser):
    SUPPORTED_DOCUMENT_TYPES = { DocumentType.TXT }  # provide supported document types

    async def process(self, document_meta: DocumentMeta) -> list[Element]:
        pass
```

## Search
After storing indexed documents in the system we can move to the search part. It is very simple and straightforward, you simply need to call [`search()`][ragbits.document_search.DocumentSearch.search] function.
The response will be a sequence of elements that are the most similar to provided query.

## Advanced configuration
There is an additional functionality of [`DocumentSearch`][ragbits.document_search.DocumentSearch] class that allows to provide a config with complete setup.
```python
config = {
    "vector_store": {...},
    "reranker": {...},
    "parser_router": {...},
    "rephraser": {...},
}

document_search = DocumentSearch.from_config(config)
```
For a complete example please refer to `examples/document-search/from_config.py`

If you want to improve your search results you could read more on how to adjust [QueryRephraser](use_rephraser.md) or [Reranker](use_reranker.md).