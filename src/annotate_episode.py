import sys
import tagme
import wikipedia
import spacy
nlp = spacy.load("en_core_web_sm")

# Set the authorization token for subsequent calls.
with open("tagme_token", 'r') as f:
    tagme.GCUBE_TOKEN = f.read().strip()



def annotate(text):
    person_entities = []
    parsed_text = nlp(text)
    # Get person entities only
    for e in parsed_text.ents:
        if e.label_ == "PERSON":
            if e.text not in person_entities:
                person_entities.append(e.text)
    print(person_entities)
    # TODO: remove series character names
    entity_text = ", ".join(list(person_entities))
    entities = []
    try:
        episode = tagme.annotate(entity_text)
    except:
        print("error getting entities for ", entity_text)
        return None
    # Use annotations with a score higher than 0.1
    for ann in episode.get_annotations(0.1):
        eid = ann.entity_id
        ename = ann.entity_title
        escore = ann.score
        try:
            page = wikipedia.page(pageid=eid, preload=True)
            page_categories = page.categories
            # working under the assumption that any real people mention have XXXX births category
            if any([c.endswith("births") for c in page_categories]):
                page_summary = page.summary
                print(escore, eid, ename, ann.mention, page_categories[0])
                entities.append({"name": ename, "qid": eid, "categories": page_categories,
                                 "score": escore, "summary": page_summary, "links": page.links,
                                 "mention": ann.mention})
        except:
            print("error getting", ann, eid)
            continue
    return entities

if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        script = f.read()
    annotate(script)
