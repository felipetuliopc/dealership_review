# dealership_review

Dealership Review is an application that scraps the page
[DealerRater](https://www.dealerrater.com/) for the top three negative reviews
for a specific dealership, the [McKaig Chevrolet Buick](https://www.dealerrater.com/dealer/McKaig-Chevrolet-Buick-A-Dealer-For-The-People-review-23685/).

## How the score is calculated

The score is a value between (0,100). It is calculated based on the following
factors that were scrapped from the [DealerRater](https://www.dealerrater.com/)
web page:

- The overall rating;
- The employees ratings;
- The specific ratings (Customer Service, Friendliness, Pricing, ...),
- If the dealer was recommended or not;
- The review message;

#### Overall Rating

The overall rating varies from (0,50) and it corresponds to **(0, 20)** of the
score.

#### Employees Ratings

Each employee rating varies from (0,50). To aggregate those values to the
score, an average rating is taken from them and a **(0, 10)** value is added.

#### Specific Ratings

Following the same steps from employees ratings, an average is taken, and
it represents a **(0, 20)** value from the final score.

#### Recommend Dealer

Since this is a very important question, if the dealer is recommended, **40**
points is summed up to the score; otherwise, **no point** is given.

#### Review Message

The message is scanned for specific negative and positive words. Each positive
word **adds 1 points** and negative word  **subtracts 1 point**. However, there
is a ceiling of **10 points** for positive words, and a floor of **-10 points**
fo negative ones.

## Installation

This app was developed on Python 3.8.10. Follow [those steps to install it](https://www.python.org/downloads/release/python-3810/).

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

To run tests, simply:

```
make test
```

## License

Dealership Review is released under the MIT License.

