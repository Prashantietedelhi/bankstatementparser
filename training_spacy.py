import spacy
import plac
import random
from pathlib import Path
from spacy.util import minibatch, compounding
import json

TRAIN_DATA = json.load(open("new_training_data"))
labels = []
for i in TRAIN_DATA:
    i =  i[1]['entities']
    i = [j[2] for j in i]
    labels.extend(i)

labels = (list(set(labels)))
# labels.remove("BankAddress")
print(labels)


def main(model=None, new_model_name='bankstatement', output_dir="bankstatement", n_iter=10):
    """Set up the pipeline and entity recognizer, and train the new entity."""
    if model is not None:
        nlp = spacy.load(model)  # load existing spaCy model
        print("Loaded model '%s'" % model)
    else:
        nlp = spacy.blank('en')  # create blank Language class
        print("Created blank 'en' model")

    # Add entity recognizer to model if it's not in the pipeline
    # nlp.create_pipe works for built-ins that are registered with spaCy
    if 'ner' not in nlp.pipe_names:
        ner = nlp.create_pipe('ner')
        nlp.add_pipe(ner)
    # otherwise, get it, so we can add labels to it
    else:
        ner = nlp.get_pipe('ner')

    """ADD MULTIPLE LABELS TO NER MODEL"""
    # add labels
    for _, annotations in TRAIN_DATA:
        for ent in annotations.get('entities'):
            ner.add_label(ent[2])

    # get names of other pipes to disable them during training
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']
    with nlp.disable_pipes(*other_pipes):  # only train NER
        optimizer = nlp.begin_training()
        for itn in range(n_iter):
            random.shuffle(TRAIN_DATA)
            losses = {}
            for text, annotations in TRAIN_DATA:
                nlp.update([text], [annotations], sgd=optimizer, drop=0.35,
                           losses=losses)
            print(losses)

    # test the trained model
    test_text = 'Bank of America Business Advantage'
    doc = nlp(test_text)
    print("Entities in '%s'" % test_text)
    for i, ent in enumerate(doc.ents):
        print("Entity number %s is %s in text: '%s'" % (i, ent.label_, ent.text))

    # save model to output directory
    if output_dir is not None:
        output_dir = Path(output_dir)
        if not output_dir.exists():
            output_dir.mkdir()
        nlp.meta['name'] = new_model_name  # rename model
        nlp.to_disk(output_dir)
        print("Saved model to", output_dir)

        # test the saved model
        print("Loading from", output_dir)
        nlp2 = spacy.load(output_dir)
        doc2 = nlp2(test_text)
        for ent in doc2.ents:
            print(ent.label_, ent.text)

# def main(model=None, new_model_name="bankstatement", output_dir="bankstatement", n_iter=10):
#     """Set up the pipeline and entity recognizer, and train the new entity."""
#     random.seed(0)
#     if model is not None:
#         nlp = spacy.load(model)  # load existing spaCy model
#         print("Loaded model '%s'" % model)
#     else:
#         nlp = spacy.blank("en")  # create blank Language class
#         print("Created blank 'en' model")
#     # Add entity recognizer to model if it's not in the pipeline
#     # nlp.create_pipe works for built-ins that are registered with spaCy
#     if "ner" not in nlp.pipe_names:
#         ner = nlp.create_pipe("ner")
#         nlp.add_pipe(ner)
#     # otherwise, get it, so we can add labels to it
#     else:
#         ner = nlp.get_pipe("ner")
#     for LABEL in labels:
#         print(LABEL)
#         ner.add_label(LABEL)  # add new entity label to entity recognizer
#     ner.add_label("VEGETABLE")
#     # Adding extraneous labels shouldn't mess anything up
#     # ner.add_label("VEGETABLE")
#     if model is None:
#         optimizer = nlp.begin_training()
#     else:
#         optimizer = nlp.resume_training()
#     move_names = list(ner.move_names)
#     # get names of other pipes to disable them during training
#     other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]
#     with nlp.disable_pipes(*other_pipes):  # only train NER
#         sizes = compounding(1.0, 4.0, 1.001)
#         # batch up the examples using spaCy's minibatch
#         for itn in range(n_iter):
#             random.shuffle(TRAIN_DATA)
#             batches = minibatch(TRAIN_DATA, size=sizes)
#             losses = {}
#             for batch in batches:
#                 texts, annotations = zip(*batch)
#                 nlp.update(texts, annotations, sgd=optimizer, drop=0.35, losses=losses)
#             print("Losses", losses)
#
#     # test the trained model
#     test_text = "Wilmington, DE 19850"
#     doc = nlp(test_text)
#     print("Entities in '%s'" % test_text)
#     for ent in doc.ents:
#         print(ent.label_, ent.text)
#
#     # save model to output directory
#     if output_dir is not None:
#         output_dir = Path(output_dir)
#         if not output_dir.exists():
#             output_dir.mkdir()
#         nlp.meta["name"] = new_model_name  # rename model
#         nlp.to_disk(output_dir)
#         print("Saved model to", output_dir)
#
#         # test the saved model
#         print("Loading from", output_dir)
#         nlp2 = spacy.load(output_dir)
#         # Check the classes have loaded back consistently
#         assert nlp2.get_pipe("ner").move_names == move_names
#         doc2 = nlp2(test_text)
#         for ent in doc2.ents:
#             print(ent.label_, ent.text)


main()