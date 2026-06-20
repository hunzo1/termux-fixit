"""
Database of known pip packages that need special handling on Termux/Android.
Maps pip package name -> Termux pkg equivalent + fix notes.
"""

# pip_name (lowercase) -> {
#   "pkg": termux pkg package name (or None if no pkg exists),
#   "note": short explanation of why it breaks,
#   "fix": exact command(s) to run, as a list of strings,
#   "difficulty": "easy" | "medium" | "hard" | "unsupported"
# }
PIP_TO_PKG = {
    "numpy": {
        "pkg": "python-numpy",
        "note": "No prebuilt wheel for Android arm64; pip tries to compile from source and fails.",
        "fix": ["pkg install python-numpy"],
        "difficulty": "easy",
    },
    "pandas": {
        "pkg": "python-pandas",
        "note": "Depends on numpy; same wheel problem, plus a long compile chain.",
        "fix": ["pkg install python-pandas"],
        "difficulty": "easy",
    },
    "scipy": {
        "pkg": "python-scipy",
        "note": "Needs a Fortran/BLAS toolchain that isn't available via pip on Termux.",
        "fix": ["pkg install python-scipy"],
        "difficulty": "easy",
    },
    "scikit-learn": {
        "pkg": "python-scikit-learn",
        "note": "Depends on numpy/scipy native builds.",
        "fix": ["pkg install python-scikit-learn"],
        "difficulty": "easy",
    },
    "sklearn": {
        "pkg": "python-scikit-learn",
        "note": "This is the old PyPI alias for scikit-learn; install the real package.",
        "fix": ["pkg install python-scikit-learn"],
        "difficulty": "easy",
    },
    "pillow": {
        "pkg": "python-pillow",
        "note": "Needs libjpeg-turbo, freetype and zlib headers that pip can't fetch.",
        "fix": ["pkg install python-pillow"],
        "difficulty": "easy",
    },
    "pil": {
        "pkg": "python-pillow",
        "note": "PIL was renamed to Pillow; install the Termux pillow package.",
        "fix": ["pkg install python-pillow"],
        "difficulty": "easy",
    },
    "lxml": {
        "pkg": "python-lxml",
        "note": "Needs libxml2 and libxslt dev headers.",
        "fix": ["pkg install python-lxml"],
        "difficulty": "easy",
    },
    "cryptography": {
        "pkg": "python-cryptography",
        "note": "Needs a Rust toolchain and OpenSSL headers to build from pip.",
        "fix": ["pkg install python-cryptography"],
        "difficulty": "medium",
    },
    "pyopenssl": {
        "pkg": "python-pyopenssl",
        "note": "Depends on the cryptography package above.",
        "fix": ["pkg install python-cryptography", "pip install pyopenssl"],
        "difficulty": "medium",
    },
    "matplotlib": {
        "pkg": "python-matplotlib",
        "note": "Needs freetype, png and a working backend; pip build fails without them.",
        "fix": ["pkg install python-matplotlib"],
        "difficulty": "easy",
    },
    "opencv-python": {
        "pkg": "opencv-python",
        "note": "OpenCV needs a huge native build chain; the pip wheel doesn't exist for Android.",
        "fix": ["pkg install opencv-python"],
        "difficulty": "medium",
    },
    "cv2": {
        "pkg": "opencv-python",
        "note": "cv2 is the import name for opencv-python.",
        "fix": ["pkg install opencv-python"],
        "difficulty": "medium",
    },
    "psycopg2": {
        "pkg": "postgresql",
        "note": "Needs libpq headers from the postgresql package, then pip can build the binding.",
        "fix": ["pkg install postgresql", "pip install psycopg2-binary"],
        "difficulty": "medium",
    },
    "mysqlclient": {
        "pkg": "mariadb",
        "note": "Needs MariaDB client dev headers.",
        "fix": ["pkg install mariadb", "pip install mysqlclient"],
        "difficulty": "medium",
    },
    "pymysql": {
        "pkg": None,
        "note": "Pure Python MySQL driver, usually installs fine without pkg deps.",
        "fix": ["pip install pymysql"],
        "difficulty": "easy",
    },
    "pyaudio": {
        "pkg": "portaudio",
        "note": "Needs the PortAudio C library which pip can't install.",
        "fix": ["pkg install portaudio", "pip install pyaudio"],
        "difficulty": "medium",
    },
    "sounddevice": {
        "pkg": "portaudio",
        "note": "Wraps PortAudio; same native dependency as pyaudio.",
        "fix": ["pkg install portaudio", "pip install sounddevice"],
        "difficulty": "medium",
    },
    "pycairo": {
        "pkg": "py3cairo",
        "note": "Needs the Cairo graphics library headers.",
        "fix": ["pkg install py3cairo"],
        "difficulty": "easy",
    },
    "pygobject": {
        "pkg": "python-pygobject",
        "note": "Needs gobject-introspection and glib dev headers.",
        "fix": ["pkg install python-pygobject"],
        "difficulty": "medium",
    },
    "bcrypt": {
        "pkg": None,
        "note": "Newer versions need a Rust toolchain to build on Termux.",
        "fix": ["pkg install rust", "pip install bcrypt"],
        "difficulty": "medium",
    },
    "pyzmq": {
        "pkg": "python-pyzmq",
        "note": "Needs the libzmq native library.",
        "fix": ["pkg install python-pyzmq"],
        "difficulty": "easy",
    },
    "zmq": {
        "pkg": "python-pyzmq",
        "note": "zmq is the import name for pyzmq.",
        "fix": ["pkg install python-pyzmq"],
        "difficulty": "easy",
    },
    "grpcio": {
        "pkg": None,
        "note": "Extremely long native compile (Cython + C++); often times out or runs out of memory on phones.",
        "fix": ["pip install --no-binary :all: grpcio", "# Expect a 20-40 min build; low-RAM devices may OOM."],
        "difficulty": "hard",
    },
    "tensorflow": {
        "pkg": None,
        "note": "No official Android/arm64 wheel; not realistically installable on Termux.",
        "fix": ["# Consider tflite-runtime instead, or run inference via a remote API."],
        "difficulty": "unsupported",
    },
    "torch": {
        "pkg": None,
        "note": "No official PyTorch wheel for Termux; community wheels are unstable/version-locked.",
        "fix": ["# Try a community arm64 wheel, or offload training/inference to a server."],
        "difficulty": "unsupported",
    },
    "pyqt5": {
        "pkg": "python-pyqt5",
        "note": "Needs the Qt5 native libraries pip can't ship.",
        "fix": ["pkg install python-pyqt5"],
        "difficulty": "medium",
    },
    "pyside2": {
        "pkg": None,
        "note": "Qt bindings with no Termux package and a very heavy native build.",
        "fix": ["# Not realistically buildable on-device; consider PyQt5 via pkg instead."],
        "difficulty": "unsupported",
    },
    "kivy": {
        "pkg": None,
        "note": "Needs SDL2, a graphics stack, and a long native build chain.",
        "fix": ["pkg install sdl2 sdl2-image sdl2-mixer sdl2-ttf", "pip install kivy"],
        "difficulty": "hard",
    },
    "gdal": {
        "pkg": "gdal",
        "note": "Needs the native GDAL geospatial library.",
        "fix": ["pkg install gdal"],
        "difficulty": "medium",
    },
    "shapely": {
        "pkg": "geos",
        "note": "Needs the GEOS geometry library.",
        "fix": ["pkg install geos", "pip install shapely"],
        "difficulty": "easy",
    },
    "pyodbc": {
        "pkg": "unixodbc",
        "note": "Needs unixODBC driver manager headers.",
        "fix": ["pkg install unixodbc", "pip install pyodbc"],
        "difficulty": "medium",
    },
    "pynacl": {
        "pkg": "libsodium",
        "note": "Needs the libsodium crypto library.",
        "fix": ["pkg install libsodium", "pip install pynacl"],
        "difficulty": "easy",
    },
    "gevent": {
        "pkg": None,
        "note": "Depends on greenlet, which needs a Cython compile that's slow on phone CPUs.",
        "fix": ["pip install greenlet gevent", "# First install can take several minutes."],
        "difficulty": "medium",
    },
    "greenlet": {
        "pkg": None,
        "note": "Cython-compiled; slow but usually succeeds eventually on Termux.",
        "fix": ["pip install greenlet"],
        "difficulty": "medium",
    },
    "uvloop": {
        "pkg": None,
        "note": "Built on libuv internals that don't reliably target Android; frequently fails to build.",
        "fix": ["# Skip uvloop on Termux; asyncio's default loop works fine."],
        "difficulty": "unsupported",
    },
    "asyncpg": {
        "pkg": "postgresql",
        "note": "Needs libpq headers for its C extension.",
        "fix": ["pkg install postgresql", "pip install asyncpg"],
        "difficulty": "medium",
    },
    "cffi": {
        "pkg": "libffi",
        "note": "Needs the libffi native library, a dependency of many other packages too.",
        "fix": ["pkg install libffi", "pip install cffi"],
        "difficulty": "easy",
    },
    "protobuf": {
        "pkg": "protobuf",
        "note": "Newer versions can need the system protoc compiler.",
        "fix": ["pkg install protobuf", "pip install protobuf"],
        "difficulty": "easy",
    },
    "pyarrow": {
        "pkg": None,
        "note": "Very large C++ build (Arrow + Parquet); not practical to compile on a phone.",
        "fix": ["# Not realistically installable on-device; consider reading data with pandas+csv instead."],
        "difficulty": "unsupported",
    },
    "duckdb": {
        "pkg": None,
        "note": "Bundles a large C++ engine; the pip sdist build is heavy and slow on ARM phones.",
        "fix": ["pip install duckdb", "# Expect a long first build; be patient or use sqlite3 instead."],
        "difficulty": "hard",
    },
    "h5py": {
        "pkg": "python-h5py",
        "note": "Needs the HDF5 native library.",
        "fix": ["pkg install python-h5py"],
        "difficulty": "easy",
    },
    "netcdf4": {
        "pkg": "netcdf",
        "note": "Needs the netCDF native library.",
        "fix": ["pkg install netcdf", "pip install netcdf4"],
        "difficulty": "medium",
    },
    "python-levenshtein": {
        "pkg": None,
        "note": "Needs a C compile; rapidfuzz is a drop-in pure-wheel alternative.",
        "fix": ["pip install rapidfuzz", "# rapidfuzz has the same API style and installs instantly."],
        "difficulty": "medium",
    },
    "fasttext": {
        "pkg": None,
        "note": "Heavy C++ compile that frequently fails on ARM/Android.",
        "fix": ["# Consider gensim's fasttext wrapper or a hosted embedding API instead."],
        "difficulty": "hard",
    },
    "gensim": {
        "pkg": None,
        "note": "Depends on numpy/scipy's native build chain plus its own Cython extensions.",
        "fix": ["pkg install python-numpy python-scipy", "pip install gensim"],
        "difficulty": "hard",
    },
    "spacy": {
        "pkg": None,
        "note": "Needs Cython, blis, and multiple native deps; rarely succeeds on Termux.",
        "fix": ["# Not well supported on Termux; consider a lighter NLP lib like nltk for on-device work."],
        "difficulty": "unsupported",
    },
    "pyspark": {
        "pkg": "openjdk-17",
        "note": "Needs a JVM; install Java first.",
        "fix": ["pkg install openjdk-17", "pip install pyspark"],
        "difficulty": "medium",
    },
    "pycocotools": {
        "pkg": None,
        "note": "Needs a Cython compile against numpy headers.",
        "fix": ["pkg install python-numpy", "pip install pycocotools"],
        "difficulty": "medium",
    },
    "dlib": {
        "pkg": None,
        "note": "Massive C++ compile (CMake + BLAS); commonly times out or OOMs on phones.",
        "fix": ["# Not realistically buildable on-device; use a hosted face/landmark API instead."],
        "difficulty": "unsupported",
    },
    "face-recognition": {
        "pkg": None,
        "note": "Depends on dlib, which doesn't build on Termux.",
        "fix": ["# See dlib note - not realistically installable on-device."],
        "difficulty": "unsupported",
    },
    "regex": {
        "pkg": None,
        "note": "Usually fine; only fails if pip's prebuilt wheel index is unreachable.",
        "fix": ["pip install regex"],
        "difficulty": "easy",
    },
    "pyyaml": {
        "pkg": "python-yaml",
        "note": "Has an optional Cython speedup that sometimes triggers a compile.",
        "fix": ["pkg install python-yaml"],
        "difficulty": "easy",
    },
    "ujson": {
        "pkg": None,
        "note": "Small C extension; usually compiles fine but can fail without build-essential.",
        "fix": ["pkg install build-essential", "pip install ujson"],
        "difficulty": "easy",
    },
    "twisted": {
        "pkg": None,
        "note": "Pure Python, but some optional extras need cryptography's native build.",
        "fix": ["pip install twisted"],
        "difficulty": "easy",
    },
}

# Mapping of missing shared-object library names to the Termux pkg that provides them.
SO_LIB_TO_PKG = {
    "libxml2.so": "libxml2",
    "libxslt.so": "libxslt",
    "libjpeg.so": "libjpeg-turbo",
    "libpng.so": "libpng",
    "libfreetype.so": "freetype",
    "libffi.so": "libffi",
    "libssl.so": "openssl",
    "libcrypto.so": "openssl",
    "libsodium.so": "libsodium",
    "libzmq.so": "libzmq",
    "libpq.so": "postgresql",
    "libgeos_c.so": "geos",
    "libhdf5.so": "hdf5",
    "libportaudio.so": "portaudio",
    "libcairo.so": "cairo",
    "libgdal.so": "gdal",
    "libnetcdf.so": "netcdf",
}


def lookup(pip_name: str):
    """Look up a pip package name (case-insensitive) in the database."""
    return PIP_TO_PKG.get(pip_name.strip().lower())


def lookup_so(lib_name: str):
    """Look up a missing .so library name in the database."""
    return SO_LIB_TO_PKG.get(lib_name.strip())
