from os import listdir
from os.path import isfile, join
from urllib.parse import quote
import partitura as pt


def list_scores(fp="scores"):
    files = [
        join(fp, f) for f in listdir(fp) if isfile(join(fp, f)) and f.endswith(".mxl")
    ]
    result = {}
    for sf in files:
        score = pt.load_score(sf)
        result[score.title] = sf

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
                {title}:
                <a href="https://app.musetrainer.com/#/play?file={url}">Play Online</a>
                &middot;
                <a href="{link}">Download</a>
            </li>
            """
    with open("index.html", "w") as f:
        f.write(html.replace("{LI_LIST}", li_list))


def generate_readme(scores):
    pass


def generate():
    scores = list_scores()
    generate_readme(scores)
    generate_index(scores)


if __name__ == "__main__":
    generate()
