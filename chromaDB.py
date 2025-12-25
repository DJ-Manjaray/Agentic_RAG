from pathlib import Path
import shutil

import chromadb
from chromadb.errors import InvalidArgumentError

from datasets import df_qa, df_medical_device


DB_PATH = Path(__file__).parent / "chroma_db"
QA_DOCS = df_qa["combined_text"].astype(str).tolist()
QA_METAS = df_qa.to_dict(orient="records")
QA_IDS = df_qa.index.astype(str).tolist()

DEVICE_DOCS = df_medical_device["combined_text"].astype(str).tolist()
DEVICE_METAS = df_medical_device.to_dict(orient="records")
DEVICE_IDS = df_medical_device.index.astype(str).tolist()


def _reset_chroma_path() -> None:
    """Remove the on-disk store so Chroma can start fresh."""
    shutil.rmtree(DB_PATH, ignore_errors=True)


def _init_client() -> chromadb.PersistentClient:
    return chromadb.PersistentClient(path=str(DB_PATH))


def _populate_collection(collection, *, documents, metadatas, ids):
    try:
        current_size = collection.count()
    except InvalidArgumentError:
        raise

    if current_size >= len(ids):
        return collection

    if current_size > 0:
        collection.delete(where={})

    collection.add(documents=documents, metadatas=metadatas, ids=ids)
    return collection


def _build_collections():
    client = _init_client()
    try:
        medical_qna = _populate_collection(
            client.get_or_create_collection(name="medical_q_n_a"),
            documents=QA_DOCS,
            metadatas=QA_METAS,
            ids=QA_IDS,
        )

        medical_devices = _populate_collection(
            client.get_or_create_collection(name="medical_device_manual"),
            documents=DEVICE_DOCS,
            metadatas=DEVICE_METAS,
            ids=DEVICE_IDS,
        )
        return medical_qna, medical_devices
    except InvalidArgumentError as exc:
        # Any compaction/log-store error means the DB files are corrupt – rebuild once.
        if "Failed to pull logs" not in str(exc):
            raise
        _reset_chroma_path()
        client = _init_client()
        medical_qna = _populate_collection(
            client.get_or_create_collection(name="medical_q_n_a"),
            documents=QA_DOCS,
            metadatas=QA_METAS,
            ids=QA_IDS,
        )
        medical_devices = _populate_collection(
            client.get_or_create_collection(name="medical_device_manual"),
            documents=DEVICE_DOCS,
            metadatas=DEVICE_METAS,
            ids=DEVICE_IDS,
        )
        return medical_qna, medical_devices


collection1, collection2 = _build_collections()


if __name__ == "__main__":
    sample_q = "What are the treatments for Kawasaki disease ?"
    print(collection1.query(query_texts=[sample_q], n_results=3))

    sample_device_query = "Which devices are suitable for neonatal patients?"
    print(collection2.query(query_texts=[sample_device_query], n_results=5))
