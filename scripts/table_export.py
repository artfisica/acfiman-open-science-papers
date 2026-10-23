"""Self-contained table documents with manuscript metadata and citation numbers."""
import re


def table_document(table, number, preamble, metadata, manuscript):
    table = re.sub(r'\\(?:begin|end)\{table\}(?:\[[^]]*\])?', '', table)
    cited = {key.strip() for group in re.findall(r'\\cite\{([^}]+)\}', table)
             for key in group.split(',')}
    bibliography = ''
    if cited:
        body = re.search(r'\\begin\{thebibliography\}\{[^}]*\}(.*?)\\end\{thebibliography\}',
                         manuscript, re.S).group(1)
        entries = list(re.finditer(r'\\bibitem\{([^}]+)\}(.*?)(?=\\bibitem\{|\Z)', body, re.S))
        missing = cited - {entry[1] for entry in entries}
        if missing:
            raise ValueError('Undefined table citations: ' + ', '.join(sorted(missing)))
        bibliography = '\n' + r'\begin{thebibliography}{99}' + '\n'
        for index, entry in enumerate(entries, 1):
            if entry[1] in cited:
                bibliography += r'\bibitem[' + str(index) + ']{' + entry[1] + '}' + entry[2]
        bibliography += r'\end{thebibliography}' + '\n'
    return (r'\documentclass[11pt,letterpaper]{article}' + '\n' + preamble + '\n' + metadata
            + '\n' + r'\begin{document}\begin{minipage}{160mm}\makeatletter\def\@captype{table}\makeatother'
            + '\n' + r'\setcounter{table}{' + str(number - 1) + '}' + table
            + r'\end{minipage}' + bibliography + r'\end{document}' + '\n')
