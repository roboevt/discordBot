# Simply a dictionary mapping years to links.
# To add another year add another entry with the year and new link.

# At some point this should be reworked to automatically pull from github, so that adding another year's rules is as
# simple as adding it to the github repository, instead of having to change this bot's code.

# Could also add a way to return the score and placement of the team for various years.

class Rules:
    years = {1997: 'https://github.com/WUDBF/WUDBF2021/blob/master/Rules%20Archive/1997_dbf_rules.pdf',
             1998: 'https://github.com/WUDBF/WUDBF2021/blob/master/Rules%20Archive/1998_dbf_rules.pdf',
             1999: 'https://github.com/WUDBF/WUDBF2021/blob/master/Rules%20Archive/1999_dbf_rules.pdf',
             2000: 'https://github.com/WUDBF/WUDBF2021/blob/master/Rules%20Archive/2000_dbf_rules.pdf',
             2001: 'https://github.com/WUDBF/WUDBF2021/blob/master/Rules%20Archive/2001_dbf_rules.pdf',
             2002: 'https://github.com/WUDBF/WUDBF2021/blob/master/Rules%20Archive/2002_dbf_rules.pdf',
             2003: 'https://github.com/WUDBF/WUDBF2021/blob/master/Rules%20Archive/2003_dbf_rules.pdf',
             2004: 'https://github.com/WUDBF/WUDBF2021/blob/master/Rules%20Archive/2005-rules.pdf',
             2005: 'https://github.com/WUDBF/WUDBF2021/blob/master/Rules%20Archive/2005-rules.pdf',
             2006: 'https://github.com/WUDBF/WUDBF2021/blob/master/Rules%20Archive/2006_dbf_rules.pdf',
             2007: 'https://github.com/WUDBF/WUDBF2021/blob/master/Rules%20Archive/2007_dbf_rules.pdf',
             2008: 'https://github.com/WUDBF/WUDBF2021/blob/master/Rules%20Archive/2008_dbf_rules.pdf',
             2009: 'https://github.com/WUDBF/WUDBF2021/blob/master/Rules%20Archive/2009_dbf_rules.pdf',
             2010: 'https://github.com/WUDBF/WUDBF2021/blob/master/Rules%20Archive/2010_dbf_rules.pdf',
             2011: 'https://github.com/WUDBF/WUDBF2021/blob/master/Rules%20Archive/2011_dbf_rules.pdf',
             2012: 'https://github.com/WUDBF/WUDBF2021/blob/master/Rules%20Archive/2012_dbf_rules.pdf',
             2013: 'https://github.com/WUDBF/WUDBF2021/blob/master/Rules%20Archive/2013_dbf_rules.pdf',
             2014: 'https://github.com/WUDBF/WUDBF2021/blob/master/Rules%20Archive/2014_dbf_rules.pdf',
             2015: 'https://github.com/WUDBF/WUDBF2021/blob/master/Rules%20Archive/2015_dbf_rules.pdf',
             2016: 'https://github.com/WUDBF/WUDBF2021/blob/master/Rules%20Archive/2016_dbf_rules.pdf',
             2017: 'https://github.com/WUDBF/WUDBF2021/blob/master/Rules%20Archive/dbf-rules-2017.pdf',
             2018: 'https://github.com/WUDBF/WUDBF2021/blob/master/Rules%20Archive/dbf-rules-2018.pdf',
             2019: 'https://github.com/WUDBF/WUDBF2021/blob/master/Rules%20Archive/dbf-rules-2019.pdf',
             2020: 'https://github.com/WUDBF/WUDBF2021/blob/master/Rules%20Archive/dbf-rules-2020.pdf',
             2021: 'https://github.com/WUDBF/WUDBF2021/blob/master/Rules%20Archive/dbf-rules-2021-final-v01.pdf',
             2022: 'https://github.com/WUDBF/WUDBF2021/blob/master/Rules%20Archive/dbf-rules-2022.pdf'
             }
    {2020: 'Placement: 1, Score: 46', 2021:'Placment: 4, Score:65'}