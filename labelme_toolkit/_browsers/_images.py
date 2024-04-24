import os
import tempfile
import webbrowser
from typing import Dict
from typing import List

import jinja2

here = os.path.abspath(os.path.dirname(__file__))


def browse_images(image_paths_per_group: Dict[str, List[str]], prefix=""):
    rows = []
    for group_name, image_paths in image_paths_per_group.items():
        row = [group_name]
        for image_path in image_paths:
            row.append(os.path.abspath(image_path))
        rows.append(row)

    JINJA2_TEMPLATE = """\
<head>
  <link rel="stylesheet" type="text/css" href="{{ MODERN_NORMALIZE_CSS }}">
  <style>
    table {
      border-collapse: collapse;
    }
    tr {
      border-bottom: 1pt solid black;
    }

    /* Hide scrollbar for Chrome, Safari and Opera */
    .hide-scrollbar::-webkit-scrollbar {
      display: none;
    }
    /* Hide scrollbar for IE, Edge and Firefox */
    .hide-scrollbar {
      -ms-overflow-style: none;  /* IE and Edge */
      scrollbar-width: none;  /* Firefox */
    }
  </style>
</head>

<body>
  <div style="margin: 10px 10px 10px 10px;">
    <table>
      {% for row in rows %}
        <tr>
          {% for col in row %}
            {% if loop.index == 1 %}
              <td rowspan="2">{{ col }}</td>
            {% else %}
              <td class="hide-scrollbar" style="max-width: 300px; overflow: scroll;">{{ basename(col) }}</td>
            {% endif %}
          {% endfor %}
        </tr>
        <tr>
          {% for col in row %}
            {% if loop.index == 1 %}
            {% else %}
              <td><img src="{{ col }}" width="300px"></td>
            {% endif %}
          {% endfor %}
        </tr>
      {% endfor %}
    </table>
  </div>
</body>
"""  # noqa: E501

    html = jinja2.Template(JINJA2_TEMPLATE).render(
        MODERN_NORMALIZE_CSS=os.path.join(here, "css", "modern-normalize.min.css"),
        rows=rows,
        basename=os.path.basename,
    )

    html_file = tempfile.mktemp(suffix=".html", prefix=prefix)
    with open(html_file, "w") as f:
        f.write(html)

    webbrowser.open(f"file://{html_file}")
