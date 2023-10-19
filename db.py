from type import Analysis, WordDoc

from google.cloud.firestore_v1.document import DocumentReference

from firebase import initialize_firebase

(db) = initialize_firebase()


def get_word_doc_from_db(word: str):
	doc_ref = db.collection("words").document(word)
	doc_snapshot = doc_ref.get()
	
	return WordDoc.model_validate(doc_snapshot.to_dict()) if doc_snapshot.exists else None

def write_analysis_to_db(analysis: Analysis):
	batch = db.batch()

	morpheme_refs: list[DocumentReference] = []

	for morpheme_with_etymology in analysis.morphemes_with_etymology:
		doc_ref = db.collection("morphemes_with_etymology").document(morpheme_with_etymology.text)
		doc_snapshot = doc_ref.get()

		morpheme_refs.append(doc_ref)

		if not doc_snapshot.exists:
			batch.create(doc_ref, morpheme_with_etymology.model_dump())
	
	word_ref = db.collection("words").document(analysis.word)
	word_doc = WordDoc(
		word=analysis.word,
		etymology=analysis.etymology,
		morphemes_refs=morpheme_refs	
	)

	batch.create(word_ref, word_doc.model_dump())

	batch.commit()
