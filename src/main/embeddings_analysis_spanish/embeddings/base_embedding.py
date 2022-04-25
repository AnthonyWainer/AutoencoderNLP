import os
from typing import List

import numpy as np

from embeddings_analysis_spanish.embeddings.bert_embedding import BertEmbedding
from embeddings_analysis_spanish.embeddings.gensim_embedding import GensimEmbedding
from embeddings_analysis_spanish.embeddings.gpt_embedding import GPTEmbedding
from embeddings_analysis_spanish.utils.logger import Logger
from embeddings_analysis_spanish.utils.mapping import LazyDict


class BaseEmbedding(Logger, BertEmbedding, GPTEmbedding, GensimEmbedding):
    """
    Base Embedding
    """

    def __init__(self, gensim_path: str = "data/gensim", numpy_path: str = "data/numpy") -> None:
        """
        Init embeddings extraction
        :param gensim_path: Path where is vectors Gensim
        :param numpy_path: Path to save or load vector numpy
        """

        super().__init__()
        self.gensim_path = gensim_path
        self.numpy_path = numpy_path

    @property
    def embeddings(self) -> List:
        return ["gpt2", "bert", "w2v", "fast_text", "glove"]

    def extract(self, embedding_name: str, values: np.array, max_len: int) -> np.ndarray:
        """
        Method to extract embeddings from dict
        :param embedding_name: Name to extract
        :param values: Words to process
        :param max_len: Max length to create dimension
        :return: dimensional array with embeddings
        """
        return LazyDict({
            "gpt2": (self.extract_gpt_embedding, (values,)),
            "bert": (self.extract_bert_embedding, (values,)),
            "w2v": (self.extract_gensim_embedding, (embedding_name, values, max_len)),
            "fast_text": (self.extract_gensim_embedding, (embedding_name, values, max_len)),
            "glove": (self.extract_gensim_embedding, (embedding_name, values, max_len))
        }).get(embedding_name)

    def extract_embedding(self, embedding_name: str, dataset_name: str, x_: np.array, max_len: int = 300) -> np.ndarray:
        """
        Method to load or save array with embeddings
        :param embedding_name: Name to extract
        :param dataset_name: Dataset name to process
        :param x_: Words to process
        :param max_len: Max length to create dimension
        :return: dimensional array with embeddings
        """

        if not os.path.exists(f"{self.numpy_path}/{dataset_name}/{embedding_name}.npz"):
            vec = self.extract(embedding_name, x_.values, max_len)
            np.savez(f"{self.numpy_path}/{dataset_name}/{embedding_name}", vec)
            self.logger.info(f"saved successfully - {self.numpy_path}/{dataset_name}/{embedding_name}.npz")
            return vec
        else:
            self.logger.info("loaded successfully")
            return np.load(f"{self.numpy_path}/{dataset_name}/{embedding_name}.npz", allow_pickle=True)["arr_0"]
