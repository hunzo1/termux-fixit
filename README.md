	<div align="center">

# fixit

**Fix Python errors that only happen on Termux — automatically.**

Pipe in a traceback, get back the exact `pkg install` command that fixes it.
No more guessing. No more generic Stack Overflow answers that don't apply to Android.

</div>

---

## The problem

If you've written Python on Termux, you've hit one of these:

```
ModuleNotFoundError: No module named 'numpy'
error: externally-managed-environment
Failed building wheel for lxml
ImportError: libxml2.so: cannot open shared object file
```

`pip install numpy` doesn't just work on Termux the way it does on a normal Linux machine — there's no prebuilt wheel for Android's arm64 architecture, so pip tries to compile from source and fails. The real fix is almost always `pkg install python-numpy` instead. The problem is knowing *which* packages need that, and what the Termux equivalent is actually called.

`fixit` knows. It reads the error and tells you.

---

## Install

Copy and paste this into Termux:

```bash
git clone https://github.com/hunzo1/termux-fixit
cd termux-fixit
pip install -e .
```

That's it — `fixit` is now available as a command anywhere in your terminal.

> **Heads up:** make sure the second command actually puts you inside the folder containing `pyproject.toml`. If you ever download a zip instead of cloning, it can extract into a nested folder with the same name — run `ls` to confirm before installing.

**Optional — colored output:**

```bash
pip install rich
```

`fixit` works perfectly in plain text without this. Installing `rich` just makes the output prettier.

---

## Usage

**Fix a traceback by piping it straight in:**

```bash
python script.py 2>&1 | fixit
```

**Fix an error you've already saved to a file:**

```bash
fixit --file error.txt
```

**Check a `requirements.txt` for Termux compatibility before installing anything:**

```bash
fixit scan requirements.txt
```

This flags every package that needs special handling, and tells you upfront which ones (looking at you, `tensorflow` and `dlib`) aren't realistically installable on a phone at all — so you stop wasting battery on a build that was never going to finish.

**Look up a single package by name:**

```bash
fixit lookup pandas
```

---

## What it covers

A built-in database of 50+ packages that commonly break on Termux:

| Category | Examples |
|---|---|
| Scientific stack | numpy, pandas, scipy, scikit-learn, matplotlib |
| Images & vision | pillow, opencv-python, pycairo, dlib |
| Databases | psycopg2, mysqlclient, asyncpg |
| Crypto & networking | cryptography, pynacl, pyzmq, grpcio |
| Not realistically possible on-device | tensorflow, torch, pyarrow, spacy, dlib |

Plus pattern detection for:

- `externally-managed-environment` errors
- Missing shared library (`.so`) errors
- Missing C compiler errors
- `Failed building wheel for X` errors

---

## Why this exists

Termux runs Python on Android without the Linux package ecosystem most pip packages assume exists. Anything with a C extension — which is most of the popular scientific and crypto libraries — usually has no prebuilt wheel for Android's architecture, so pip falls back to compiling from source and breaks. The fix is well known to experienced Termux users but undocumented anywhere centralized. `fixit` is that missing reference, built into a tool instead of a wiki page.

---

## Contributing

Hit a package that breaks on Termux and isn't in the database yet? Open an issue or a pull request with the error output and the `pkg install` command that fixed it for you. The whole database lives in one file — `fixit/packages.py` — and it's a plain Python dict, so adding an entry takes about thirty seconds.

---

## License

MIT
