import json
import sys
from pathlib import Path
from annotate_episode import annotate
#season_dir = "../30rock/S2/"
season_dir = sys.argv[1]
#output_dir = "../30rock/S2_entities/"
output_dir = sys.argv[2]
output_dir = Path(output_dir)
output_dir.mkdir(parents=True, exist_ok=True)
pathlist = Path(season_dir).glob(pattern="*")
for path in pathlist:
    if not path.name.endswith(".jsonl"): # skip results files
        print(path)
        with open(path) as f:
            output_file = Path(output_dir / (path.name + ".jsonl")).open('w')
            script = f.read()
            entities = annotate(script)
            for e in entities:
                output_file.write(json.dumps(e) + "\n")
            output_file.close()
