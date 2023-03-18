from os import listdir
from os.path import isfile, join
from urllib.parse import quote
from parser import MusicXMLDocument


def list_scores(fp="scores"):
    files = [
        join(fp, f) for f in listdir(fp) if isfile(join(fp, f)) and f.endswith(".mxl")
    ]
    result = {}
    for sf in files:
        doc = MusicXMLDocument(sf)
        work_text = sf.split("/")[1].replace("_", " ").replace(".mxl", "")

        work = doc._score.find("work")
        if work is not None:
            work_title = work.find("work-title")
            if work_title is not None:
                work_text = work_title.text
        else:
            movement = doc._score.find("movement-title")
            if movement is not None:
                work_text = movement.text

        title = work_text
        if title in result:
            count = 2
            while title in result:
                title = work_text + f" ({count})"
                count += 1

        result[title] = sf

    return result


def generate_index(scores):
    html = """
<!doctype html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link href="https://musetrainer.com/dist/output.css" rel="stylesheet">
  <title>MuseTrainer - Library</title>
  <meta name="description" content="Public Domain MusicXML files">
</head>
<body>
  <div class="container">
    <div class="content">
      <h1>Library</h1>
      <h2>Public Domain MusicXML files</h2>
      <p>
        <ol>
          {LI_LIST}
        </ol>
      </p>
      <p>
        <a href="https://github.com/orgs/musetrainer/discussions/new?category=scores">Request new scores</a>
      </p>
    </div>
    <div class="footer">
      <div>
        <a href="https://musetrainer.com/legal.html">Legal</a> &middot; <a href="https://musetrainer.com/privacy.html">Privacy</a> &middot; <a href="https://musetrainer.com/support.html">Support</a>
      </div>
      <div>
        &copy; <a href="https://musetrainer.com">MuseTrainer</a>
      </div>
    </div>
  </div>
</body>

    """
    titles = sorted(scores.keys())
    li_list = ""
    for title in titles:
        link = f"https://musetrainer.com/library/{scores[title]}"
        url = quote(link.encode("utf-8"))
        li_list += f"""
            <li>
                {title}
                &middot;
                <a href="https://app.musetrainer.com/#/play?file={url}">Play</a>
                &middot;
                <a href="{link}">Download</a>
            </li>
            """
    with open("index.html", "w") as f:
        f.write(html.replace("{LI_LIST}", li_list))


def generate_readme(scores):
    readme = """
# MuseTrainer public domain MusicXML library


https://musetrainer.com/library


## Generate

```sh
poetry install
poetry run python scripts/generate.py
```

## List

"""
    titles = sorted(scores.keys())
    li_list = ""
    for title in titles:
        link = f"https://musetrainer.com/library/{scores[title]}"
        url = quote(link.encode("utf-8"))
        li_list += f"""
- {title} &middot; [Play](https://app.musetrainer.com/#/play?file={url}) &middot; [Download]({link})"""
    with open("README.md", "w") as f:
        f.write(readme + li_list)


def generate():
    scores = list_scores()
    generate_readme(scores)
    generate_index(scores)


if __name__ == "__main__":
    generate()
