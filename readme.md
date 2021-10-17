# Text Analyzer

Text Analyzer is a Python program that is able of creating statistic 
reports as .csv per input file. Some of the more useful attributes of this 
report are the number of letters and words inside the file, the filler words 
that may be extra on your text file, some words that do not belong to a normal 
English dictionary (See English dictionary sources below) and their location 
in the file, the top 5 most used and least used words in the file including 
its frequencies each, and many counters of digits, numbers, upper case letters 
and more. 

Input files are txt files per default and these should enter the 
input directory before running the program.

This program has its usages for people who write essays or official documents 
and reports and want to analyze the structure of their document without having 
to manually scan through all the words by themselves.

It can guide the user to go through certain lines and give compelling info of 
each word written. The program does not specifically tell the user where to 
make changes, but it will give some insights about each file written and gives 
a more personalized experience by giving the user the freedom to choose how 
they can enhance each document as intended.

## Prerequisites
User needs to have Python 3 installed and have all json dependencies which
should be located in the program zip

## Installation

Distribution of this program is via zip, after you managed to get a zip file, 
extract it anywhere you find it convenient, and you have it ready for usage.
Another option is to clone the [github repo](https://github.com/Leodolz/text_file_analyzer)

## English dictionary sources
Between the many attributes of each report there are two that are based on 
json files which come inside the zip file. The first one is a json dictionary 
of valid English words which can be found 
[in this GitHub repo](https://github.com/dwyl/english-words) [[1]](#1) as the 
source of validation for validating English words. The other source is another 
json file created following the first 15 words listed in 
[this page](https://www.grammarcheck.net/filler-words/) [[2]](#2) as the source of 
validating which filler words are in the document. 

These two .json files are mandatory to run the program and come inside the "valid_words" folder.


## Usage

In order to run the program, simply go to the root folder 
(text_analyzer) and in this directory you should find many other 
directories alongside with a single file named "text_analyzer.py". 
Use python command as below
```python
python3 text_analyzer.py
```
A user interaction via console will be launched, follow instructions and start
generating reports. There is a sample txt file at the input
folder, feel free to test it or delete it.

## References
<a id="1">[1]</a> 
dwyl community (August 23, 2020),
[dwyl/english-words](https://github.com/dwyl/english-words),
https://www.github.com

<a id="2">[2]</a> 
Jennifer Frost (July 19, 2021),
[30 Filler Words You Can Cut Out of Your Writing (Infographic)](https://www.grammarcheck.net/filler-words/),
https://www.grammarcheck.net

