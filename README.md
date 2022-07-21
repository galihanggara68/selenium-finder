# Selenium Element Finder

## Intro

You can easily find elements (by css selectors) in this case, using just JSON mapping file.

## Usage

### Clone or Install from pip

Clone this repo to your current directory

> git clone https://github.com/galihanggara68/selenium-finder.git

or install using pip

> pip3 install git+https://github.com/galihanggara68/selenium-finder.git@master

### Import library

First of all import Finder class

```
from Selenium_Finder.finder import Finder
```

### Using Finder class

`Finder` class has 2 parameters `driver` the Selenium WebDriver and `options`_(optional)_ dictionary where you can customize some options within `Finder` class

```
from selenium import webdriver

driver = webdriver.Chrome()

# global_wait default 10 second
# iterable_each_wait default 1 second
options = {"global_wait": 10, "iterable_each_wait": 2}
finder = Finder(driver, options)

driver.get("https://example.com")

# load mapping data
finder.load_mapping("json_mapping.json")

# execute finder
finder.by_json_scheme()

# get successfully mapped data
print(finder.get_mapped_data())
```

## Finder methods

### by_json_scheme()

execute Finder object

### load_mapping(json_path)

load JSON mapping file
_json_path_ JSON file path

### get_mapping()

get current mapping scheme

### set_mapping(new_mapping)

set mapping scheme as current mapping
_new_mapping_ mapping dictionary

### get_mapped_data()

get successful mapped data

## JSON mapping

### Basic mapping

```
{
    [map_name]: {
        "type": ["clickable" | "typable" | "iterable" | "text" | "value" | "attribute"],
        "elem": [css selector element]
    }
}
```

### _text_ and _value_ mapping

```
{
    [map name]: {
        "type": ["text" | "value"],
        "elem": [css selector element]
    }
}
```

### _attribute_ mapping

```
{
    [map name]: {
        "type": "attribute",
        "elem": [css selector element],
        "attribute": [attribute selector]
    }
}
```

### _clickable_ mapping

`effect` propery will executed after element clicked

```
{
    [map name]: {
        "type": "clickable",
        "elem": [css selector element],
        "effect": {
            [another mapping]
        }
    }
}
```

### _typable_ mapping

`text` propery is a keys that sent to element
`enter` boolean, if true it will send enter key

```
{
	"search": {
		"type": "typable",
		"elem": [css selector element],
		"text": [text to send],
		"enter": [true | false]
	},
}
```

### _iterable_ mapping

`map` will be a mapper for each item iterated

```
{
    [map name]: {
        "type": "iterable",
        "elem": [css selector element],
        "map": {
            [map name 1]: [selector 1],
            [map name n]: [selector n],
        }
    }
}
```

## JSON Mapping Example

```
{
	"search": {
		"type": "typable",
		"elem": ".search",
		"text": "Query",
		"enter": true
	},
	"user": {
		"type": "clickable",
		"elem": "a.app-aware-link.artdeco-button[href*=Profile]",
		"effect": {
			"type": "text",
			"elem": "section h1"
		}
	},
	"skills": {
		"type": "iterable",
		"elem": "#skills ~ div ul > li > div",
		"map": {
			"name": "div > div span.t-bold"
		}
	}
}
```
