# https://haystack.deepset.ai/tutorials/01_basic_qa_pipeline
# https://github.com/deepset-ai/haystack-tutorials/blob/main/tutorials/01_Basic_QA_Pipeline.ipynb
# https://huggingface.co/deepset/roberta-base-squad2
# https://docs.haystack.deepset.ai/docs/ready_made_pipelines#extractiveqapipeline

import os
import ssl
import logging
from haystack.document_stores import InMemoryDocumentStore
from haystack.pipelines.standard_pipelines import TextIndexingPipeline
from haystack.nodes import BM25Retriever
from haystack.nodes import FARMReader
from haystack.pipelines import ExtractiveQAPipeline

def questionDocuments(documentDirectory, question):
    logging.basicConfig(format="%(levelname)s - %(name)s -  %(message)s", level=logging.WARNING)
    logging.getLogger("haystack").setLevel(logging.WARN)

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
    retriever = BM25Retriever(document_store=document_store)
    reader = FARMReader(model_name_or_path = "deepset/roberta-base-squad2", use_gpu = True)
    pipe = ExtractiveQAPipeline(reader, retriever)
    params = { "Retriever": {"top_k": 10}, "Reader": {"top_k": 5} }
    prediction = pipe.run(query = question, params = params)
    return mapAnswers(document_store, prediction)

def mapAnswers(document_store, prediction):
    answers = []
    for answer in prediction["answers"]:
        answerDict = answer.to_dict()
        docIds = answerDict["document_ids"]
        backgroundContent = []
        for docId in docIds:
            content = document_store.get_document_by_id(docId)
            backgroundContent.append(content.to_dict()["content"])
        answers.append({
            "answer": answerDict["answer"],
            "score": answerDict["score"],
            "context": answerDict["context"],
            "backgroundContent": backgroundContent
        });
    return answers