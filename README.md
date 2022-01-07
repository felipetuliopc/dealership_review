# dealership_review

Dealership Review is an application that scraps the page
[DealerRater](https://www.dealerrater.com/) for the top three negative reviews
for a specific dealership, the [McKaig Chevrolet Buick](https://www.dealerrater.com/dealer/McKaig-Chevrolet-Buick-A-Dealer-For-The-People-review-23685/).

## How it works

## Installation

This app was developed on Python 3.8.10. To install it: https://www.python.org/downloads/release/python-3810/ .

After that, a package manager is needed. `pip` is being used:

```
python3 -m pip install --user --upgrade pip
```

It is recommended to install the `virtualenv` package to manage virtual environments:

```
python3 -m pip install --user virtualenv
```

The last couple steps could be followed [here](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#installing-pip).

The next step creates a virtual environment, _activates_ it and install the packages required:

```
python3 -m venv env

source env/bin/activate

make install_requirements
```

## Usage

## Tests

## License

Dealership Review is released under the MIT License. See the bundled `LICENSE`_ file
for details.

