
<div align="center">
    <a href="https://twitter.com/intent/follow?screen_name=eko_noc">
	<img alt="follow on Twitter" src="https://img.shields.io/twitter/follow/eko_noc.svg?label=follow%20%40eko_noc&style=social">
    </a>
</div>

---

<div align="center">
    <img alt="Python" src="https://img.shields.io/badge/language-python-informational.svg">
</div>

---

<div align="center">
    <img alt="Logo" src="https://noc.eko.party/web/image?model=res.company&id=1&field=logo&unique=05122020014537">
</div>

---

# urlReplacer

## Description

Detect and Replace URLs.
If you are planning to move your assets  to a CDN this program can make all the changes by choosing the extension of the files to be analyzed and the extension of the files to detect and replace the URL.

By default the program will go through the entire directory specified locating files with extensions php, html and js to search href, src and srcset within them to change the URL if it matches certain extensions
(jpg, jpeg, gif, png, tiff, js, css, scss, ico, svg, webm, mp4)

Every changed file is backed up with the extension .bak
But it is fully customizable.

## Installation

### Clone repository

```shell
git clone https://gitlab.com/ekonoc/urlreplacer.git
cd urlReplacer
```

### Usage

```shell
python3 urlReplacer.py -h
```
