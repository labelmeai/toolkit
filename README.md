<h1 align="center">
  <img src=".readme/icon.png" width="200px"><br/>Labelme Toolkit
</h1>

<h4 align="center">
  Labelme-compatible Tools for Data Processing
</h4>

<div align="center">
  <a href="#toolkit-guide"><b>Toolkit Guide</b></a>
  | <a href="https://github.com/labelmeai/labelme"><b>Labelme↗</b></a>
</div>

## Installation

```bash
pip install labelme-toolkit
```

## Usage

```bash
curl -O https://raw.githubusercontent.com/labelmeai/toolkit/main/labelme_toolkit/_data/dogs.json
# or
# wget https://raw.githubusercontent.com/labelmeai/toolkit/main/labelme_toolkit/_data/dogs.json

labelme-toolkit json-to-mask dogs.json --browse
```

<img src=".readme/dogs_json_to_mask.jpg" width="50%">


## Available tools

```
% labelmetk --help
Usage: labelmetk [OPTIONS] COMMAND [ARGS]...

Options:
  --version   Show the version and exit.
  -h, --help  Show this message and exit.

Commands:
  extract-image          Extract image from a JSON file.
  install-toolkit-pro    Install Toolkit Pro.
  json-to-mask           Convert a Labelme JSON file to a mask.
  json-to-visualization  Convert a Labelme JSON file to a visualization.
  list-labels            List unique labels in the JSON files.
```


## Toolkit Guide

If you're new to Labelme Toolkit, you can get started with
<a href="https://labelme.gumroad.com/l/toolkit?option=vDQ4V5h0nAwWV_Zk5QHkMA%3D%3D"><b>Toolkit Starter Plan</b></a>
(FREE), which contains:

- <b>Installation guide</b> for all platforms: Windows, macOS, and Linux.
- <b>Step-by-step usage guide</b> for each tools.
- <b>Examples data</b> that shows the real use of the tools.

<img src=".readme/toolkit_guide.jpg" width="50%">
