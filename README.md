opeNPSnake
==========

Parses NPS logs and generates useful reports

Winner of the Lochner Foundation Software of the Year Award (TM)
Usage
=====
Invoke opeNPSnake from the command line:
  ```
  $ python opeNPSnake.py
  ```
Help
=====
```
               ,   .,---.,---.          |         
,---.,---.,---.|\  ||---'`---.,---.,---.|__/ ,---.
|   ||   ||---'| \ ||        ||   |,---||  \ |---'
`---'|---'`---'`  `'`    `---'`   '`---^`   ``---'
     |

Parses NPS logs and generates useful reports

Usage: python opeNPSnake.py -i "filepath" [options]

Options:
    -h Prints out this help file
    -i Input file/directory (YOU MUST QUOTE THE FILE PATH)
    -o Output directory (Defaults to the current working directory)
    -P Prints list of log parameterss
    -p Select parameters for parsing [-p arg1:filter1,arg2:filter2:filter3,arg3]
    -c Specifies config file (see sample.conf)
    -t Specify the time frame [-t "* * * * *,* * * * *"] Year, Month, Day, Hour, Minute. * is a wildcard.
    -H Generates output as a pretty HTML document (default)
    -C Generates output as a CSV file
    -T Generates output as a TSV file

```
