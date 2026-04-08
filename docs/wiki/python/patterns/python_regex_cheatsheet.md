# Python Regex Cheat Sheet

## Core Functions
```python
re.search()
re.match()
re.fullmatch()
re.findall()
re.finditer()
re.sub()
re.split()
```

## Character Classes
```regex
.   any character
\d  digit
\w  word
\s  whitespace
```

## Quantifiers
```regex
*   0 or more
+   1 or more
?   optional
{n} {n,m}
```

## Anchors
```regex
^   start
$   end
  word boundary
```

## Groups
```regex
(abc)       capture
(?:abc)     non-capture
```

## Alternation
```regex
cat|dog
```

## Lookarounds
```regex
(?=abc)
(?!abc)
(?<=abc)
(?<!abc)
```

## Flags
```python
re.I  re.M  re.S  re.X
```

## Tip
Always use raw strings:
```python
r"\d+"
```
