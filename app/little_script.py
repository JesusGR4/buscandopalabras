#!/usr/bin/python3
import pandas as pd

char = input("Escriba una cadena: ")
char2 = input("Escriba la cadena por la que sustituir: ")
length1 = input("Escriba el rango inicial: ")
length2 = input("Escriba el rango final: ")
conditions = [
	'.*%s.*' % char,
	'^.{%s,%s}$' % (length1, length2),
]

# Combine conditions
rgx_str = ''.join(['(?=%s)' % c for c in conditions ])

# Read words from file
df = pd.read_csv('diccionario.txt', dtype='str')

# New Column: Change 'b' to 'v'
df['b'] = df[df['a'].str.contains(rgx_str)]['a'].str.replace(char, char2)

# Kw
df['c'] = df['a'] + ' o ' + df['b']
# reverse
df['d'] = df['b'] + ' o ' + df['a']

# Remove NaN rows and save kw to csv
df['c'].dropna().to_csv('kw.csv', index=False)
# Remove NaN rows and save reverse kw to csv
df['d'].dropna().to_csv('kw_reverse.csv', index=False)
