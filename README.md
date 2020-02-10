# scrape
a proof of concept on harvesting email addresses related to certain keywords

# how it works
given a text file *defaulttxt* here each line contains keywords related to a person, company, etc. the program uses online search to look for email addresses related to those keywords. It scrapes the results and extracts email addresses. It will generate a csv file *result.txt* where each line starts by its number and continues with found emails separated by a comma

# warnings
- program is slow, it's a POC and not meant to be fast, it is slow especially when returned pages are binary files (pdf, docs...)
- please do not misuse!
