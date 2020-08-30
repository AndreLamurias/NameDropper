from pathlib import Path
import json
import sys
from json2html import json2html
#season_dir = "../30rock/S1_entities/"
season_dir = sys.argv[1]
output_dir = sys.argv[2]
output_dir = Path(output_dir)
output_dir.mkdir(parents=True, exist_ok=True)
all_entities = {}
entities_per_episode = {}
series_characters = ["jack", "liz", "donaghy", "tracy", "frank", "pete", "josh", "don", "geiss",
                         "jonathan", "ken", "kenneth", "parcel"]

pathlist = Path(season_dir).glob(pattern="*")
for path in pathlist:
    if path.name.endswith(".jsonl"):
        entities_per_episode[path.stem] = []
        for line in path.open():
            entity = json.loads(line)
            qid = entity["qid"]
            ename = entity["name"]
            # ignore mention of character names
            if entity["mention"].lower() in series_characters:
                print("ignored", entity["mention"])
                continue
            entities_per_episode[path.stem].append(ename)
            if ename not in all_entities:
                all_entities[ename] = entity
                all_entities[ename]["episodes"] = [path.name]
                all_entities[ename]["mentions"] = [entity["mention"]]
            else:
                all_entities[ename]["episodes"].append(path.name)
                all_entities[ename]["mentions"].append(entity["mention"])
            if "categories" in all_entities[ename]:
                del all_entities[ename]["categories"]
            if "mention" in all_entities[ename]:
                del all_entities[ename]["mention"]
            if "links" in all_entities[ename]:
                del all_entities[ename]["links"]

#print(list(all_entities.values()))
with open(output_dir / "report.html", 'w') as f:
    f.write(json2html.convert({"data": list(all_entities.values())}))
for episode in entities_per_episode:
    with open(output_dir / (episode + "_report.html"), 'w') as f:
        f.write(json2html.convert({"data": [all_entities[e] for e in entities_per_episode[episode]]}))
