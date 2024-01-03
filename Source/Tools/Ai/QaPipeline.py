# https://haystack.deepset.ai/tutorials/01_basic_qa_pipeline
# https://github.com/deepset-ai/haystack-tutorials/blob/main/tutorials/01_Basic_QA_Pipeline.ipynb
# https://huggingface.co/deepset/roberta-base-squad2
# https://docs.haystack.deepset.ai/docs/ready_made_pipelines#extractiveqapipeline

import os
import ssl
import logging
from haystack.telemetry import tutorial_running
from haystack.document_stores import InMemoryDocumentStore
from haystack.pipelines.standard_pipelines import TextIndexingPipeline

def questionDocuments(documentDirectory, question):
    tutorial_running(1)
    logging.basicConfig(format="%(levelname)s - %(name)s -  %(message)s", level=logging.WARNING)
    logging.getLogger("haystack").setLevel(logging.INFO)

    document_store = InMemoryDocumentStore(use_bm25=True)

    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context

    files_to_index = [documentDirectory + "/" + f for f in os.listdir(documentDirectory)]
    indexing_pipeline = TextIndexingPipeline(document_store)
    indexing_pipeline.run_batch(file_paths=files_to_index)

    from haystack.nodes import BM25Retriever
    retriever = BM25Retriever(document_store=document_store)

    from haystack.nodes import FARMReader
    reader = FARMReader(model_name_or_path="deepset/roberta-base-squad2", use_gpu=True)

    from haystack.pipelines import ExtractiveQAPipeline
    pipe = ExtractiveQAPipeline(reader, retriever)

    prediction = pipe.run(
        query=question,
        params={
            "Retriever": {"top_k": 10},
            "Reader": {"top_k": 5}
        }
    )

    from pprint import pprint
    pprint(prediction)

    from haystack.utils import print_answers
    print_answers(
        prediction,
        details="medium" ## Choose from `minimum`, `medium`, and `all`
    )

    print(prediction["query"])
    print(prediction["answers"][0])

    p0 = prediction["answers"][0].to_dict()
    print(p0)
    print(p0["answer"])
    print(p0["score"])
    print(p0["context"])
    documentId = p0["document_ids"][0]
    print(documentId)

    document = document_store.get_document_by_id(documentId)
    print(document.to_dict())