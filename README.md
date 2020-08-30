# Name Dropper

## Introduction
This project aims at automatically linking references to real people on TV episodes to Wikipedia pages.
My motivation was that while rewatching 30 rock, every episode has many references to real-world people (not characters), 
which I was not familiar with.
I found myself checking several names on Wikipedia while watching an episode, so I developed this script to do it automatically for me.

## Dependencies

* spacy - identifies the named entities of a document so that we don't have to link the full text to wikipedia;
* tagme - provides a Wikipedia Entity Linking API;
* wikipedia - The wikipedia python library is an interface to the MediaWiki API to obtain more info about each entity.

## Usage

Assuming you have the transcription of one or more episodes in a specific directory, you can run the following command:

```bash
python src/annotate_season.py episodes_dir/ output_dir/
```

This command will write one jsonl file per episode, where each line is an entity identified.
We can explore these entities with the `analyse_season.py` and `write_season_episodes_tables.py` script.
While the former tries to link personalities mention across various episodes, the former generates html reports on each episode.

## TODO
- [ ] Generalize for any tv show
- [ ] Use argpase
- [ ] improve HTML reports
