# Yelp Recommendations

## Overview

Yelp Recommendations is a Python-based project that allows users to search and retrieve business recommendations from Yelp based on specified search terms and locations. The project leverages web scraping techniques to extract information from Yelp search results, making it easier to find recommendations for various businesses.

## Features

- Search for businesses on Yelp based on specific terms and locations.
- Extract and display key information about businesses from Yelp search results.
- Utilize web scraping to retrieve information in an automated manner.
- Simple and clean code structure to facilitate further development and customization.

## Installation Instructions

To set up and install the Yelp Recommendations project, follow these steps:

1. **Clone the Repository:**

    ```sh
    git clone https://github.com/Yuriy/Yelp-Recommendations.git
    cd Yelp-Recommendations
    ```

2. **Set Up a Virtual Environment:**

    It's recommended to use a virtual environment to manage dependencies. You can create one using `venv`:

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install Dependencies:**

    Install the required Python libraries using `pip`:

    ```sh
    pip install -r requirements.txt
    ```

4. **Run the Script:**

    ```sh
    python search.py
    ```

## Usage Examples

To use the Yelp Recommendations project, you can run the `search.py` script with the appropriate search term and location. Here's an example of how to search for "coffee" in "San Francisco":

```python
from search import get_businesses_from_search

term = "coffee"
location = "San Francisco"
businesses = get_businesses_from_search(term, location)

for business in businesses:
    print(business)
```

You can easily modify the `term` and `location` variables to suit your search needs.

## Code Summary

### Code Structure:
- **search.py**: Contains the main functionality for searching businesses on Yelp.

### Key Files:
- **search.py**: Implements the `get_businesses_from_search` function that constructs the Yelp search URL, fetches search results, and parses the relevant business information using BeautifulSoup.

Here's an overview of the `search.py` file:

```python
#!/usr/bin/env python

import sys
import urllib
import urlparse
from BeautifulSoup import BeautifulSoup
from collections import defaultdict
from operator import itemgetter

def get_businesses_from_search(term, location):
    search_url = "http://www.yelp.com/search?find_desc=%s&ns=1&find_loc=%s" % (urllib.quote(term), urllib.quote(location))
    conn = urllib.urlopen(search_url)
    contents = conn.read()
    soup = BeautifulSoup(contents)
    for result in soup("div", {"class": "businessresult clearfix"}):
        pass  # Parsing logic to extract business details
```

## Contributing Guidelines

We welcome contributions to the Yelp Recommendations project. To contribute:

1. Fork the repository on GitHub.
2. Create a new branch with a descriptive name for your feature or bugfix.
3. Make your changes and ensure they are well-tested.
4. Submit a pull request with a detailed description of your changes.

Please make sure to follow the existing code style and include appropriate tests for any new features.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.