from pydantic import BaseModel

from google.cloud.firestore_v1.base_query import FieldFilter
from google.cloud.firestore_v1.base_collection import BaseCollectionReference
from google.cloud.firestore_v1.document import DocumentReference

from firebase import db


class WordDoc(BaseModel):
	word: str
	etymology: str
	morphemes: list[DocumentReference]

	class Config:
		arbitrary_types_allowed = True


def get_word_doc_from_db(word: str):
	words_ref: BaseCollectionReference = db.collection("words")
	query_ref = words_ref.where(filter=FieldFilter("word", "==", word))
	docs = query_ref.stream()

	words: list[WordDoc] = []
	for doc in docs:
		dict = doc.to_dict()
		words.append(WordDoc.model_validate(dict))
	
	return words[0] if words else None
