# Regular Expressions (Regex) Cheatsheet
1. Basic Characters
```text
abc        # Matches exact sequence "abc"
.          # Any character except newline
\          # Escape special character
```

2. Character Classes
```text
[abc]      # One of a, b, or c
[^abc]     # NOT a, b, or c
[a-z]      # Any lowercase letter
[A-Z]      # Any uppercase letter
[0-9]      # Any digit
```
Common Shorthands
```text
\d         # Digit (0-9)
\D         # Non-digit
\w         # Word character (a-z, A-Z, 0-9, _)
\W         # Non-word character
\s         # Whitespace (space, tab, newline)
\S         # Non-whitespace
```

3. Quantifiers (Repetition)
```
*          # 0 or more
+          # 1 or more
?          # 0 or 1 (optional)
{n}        # Exactly n times
{n,}       # n or more times
{n,m}      # Between n and m times
```

Examples
```text
\d+        # One or more digits
a{2,4}     # "aa", "aaa", or "aaaa"
```

4. Anchors (Position)
```text
^          # Start of string (or line in multiline mode)
$          # End of string (or line)
\b         # Word boundary
\B         # Not a word boundary
```
Examples
```text
^Hello     # String starting with "Hello"world
$     # String ending with "world"
\bcat\b    # Whole word "cat"
```

5. Groups & Capturing
```text
(abc)      # Capturing group
(?:abc)    # Non-capturing group
```
Example
```text
(\d{3})-(\d{2})-(\d{4})  # Captures parts of an SSN
```

6. Alternation (OR)
```text
cat|dog    # Matches "cat" or "dog"
```
With grouping
```text
(grand|great)parent
```

7. Lookarounds (Advanced)
```text
(?=abc)    # Positive lookahead
(?!abc)    # Negative lookahead
(?<=abc)   # Positive lookbehind
(?<!abc)   # Negative lookbehind
```
Examples
```text
\d+(?=%)   # Number followed by %
(?<!\$)\d+ # Numbers not preceded by $
```

8. Flags / Modifiers
```text
i          # Case-insensitive
g          # Global (find all matches)
m          # Multiline (^ and $ match lines)
s          # Dot matches newline
```
```Python
re.compile("hello", re.I | re.M)
```

9. Common Patterns
Email (simple)
```text
^[\w.-]+@[\w.-]+\.\w+$
```
URL (basic)
```text
https?://[^\s]+
```

Phone (US-style)
```text
\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}
```

Date (YYYY-MM-DD)
```text
\d{4}-\d{2}-\d{2}
```

10. Greedy vs Lazy
```text
.*         # Greedy (matches as much as possible).*?        # Lazy (matches as little as possible)
```
Example
```Python
<.*>       # Matches entire HTML block
<.*?>      # Matches a single tag
```

11. Escaping Special Characters
Must escape:
```Python
. ^ $ * + ? ( ) [ ] { } | \
```
Example:
```
\.\*\?     # Matches literal ".*?"
```

12. Quick Testing Tips

- Use regex101.com or regexr.com
- Test with both matching and non-matching examples
- Start simple, then add complexity

All examples assume:
```Python
import re
```

# Python Regular Expressions (re) – Cheatsheet
1. Core Matching Functions
```Python
re.search(pattern, text)     # First match anywhere in string
re.match(pattern, text)      # Match only at start of string
re.fullmatch(pattern, text)  # Entire string must match
re.findall(pattern, text)    # All matches as list
re.finditer(pattern, text)   # Iterator of Match objects
re.sub(pattern, repl, text)  # Replace matches
re.split(pattern, text)      # Split by regex
```

2. Basic Patterns
```Python
abc        # Literal match
.          # Any character except newline
\          # Escape special character
```
Python string tip:
Use raw strings to avoid double escaping:
```Python
re.search(r"\d+", text)   # recommended
```

3. Character Classes
```Python
[abc]      # a, b, or c
[^abc]     # not a, b, or c
[a-z]      # lowercase letter
[A-Z]      # uppercase letter
[0-9]      # digit
```

Built‑in Shorthand Classes
```Python
\d         # digit (0–9)
\D         # non-digit
\w         # word char (a-z, A-Z, 0-9, _)
\W         # non-word char
\s         # whitespace
\S         # non-whitespace
```

4. Quantifiers (Repetition)
```Python
*          # 0 or more
+          # 1 or more
?          # 0 or 1
{n}        # exactly n
{n,}       # n or more
{n,m}      # between n and m
```
Examples
```Python
\d+        # one or more digits
[a-z]{3}   # exactly 3 lowercase letters
```

5. Anchors (Position)
```Python
^          # start of string
$          # end of string
\b         # word boundary
\B         # not a word boundary
```
Example
```Python
re.search(r"^Hello", text)
```

6. Groups & Capturing
```Python
(abc)      # capturing group
(?:abc)    # non-capturing group
```
Accessing groups
```Python
m = re.search(r"(\d{3})-(\d{2})", "123-45")m.group(0)   # '123-45'm.group(1)   # '123'm.groups()   # ('123', '45')
```

7. Alternation (OR)
```Python
cat|dog
```
Grouped
```Python
(grand|great)parent
```

8. Lookarounds (Fully Supported in Python)
```Python
(?=abc)    # positive lookahead
(?!abc)    # negative lookahead
(?<=abc)   # positive lookbehind
(?<!abc)   # negative lookbehind
```

Examples
```Python
\d+(?=%)     # digits followed by %
(?<!\$)\d+   # digits not preceded by $
```

9. Greedy vs Lazy
```Python
.*          # greedy
.*?         # lazy (non-greedy)
```
Example
```Python
re.search(r"<.*?>", "<tag>text</tag>").group()# '<tag>'
```

10. Flags (re Options)
```Python
re.I   # IGNORECASE
re.M   # MULTILINE (^ and $ affect each line)
re.S   # DOTALL (. matches newline)
re.X   # VERBOSE (whitespace + comments)
```
Example
```Python
re.search(r"^abc", text, re.I | re.M)
```

11. Verbose / Readable Regex
```Python
pattern = r"""    ^\d{4}        # year
                  -\d{2}        # month    
                  -\d{2}$       # day
"""
re.match(pattern, date, re.X)
```

12. Common Python Regex Patterns
Email (simple)
```Python
^[\w.-]+@[\w.-]+\.\w+$
```
URL
```Python
https?://[^\s]+
```
US Phone Number
```Python
\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}
```
Date (YYYY-MM-DD)
```Python
\d{4}-\d{2}-\d{2}
```

13. Substitution with Backreferences
```Python
re.sub(r"(\w+), (\w+)", r"\2 \1", "Doe, John")  # 'John Doe'
```

14. Performance Tip
Compile patterns you reuse:
```Python
pattern = re.compile(r"\d+")
pattern.findall(text)
```

15. Debugging & Testing

- Use regex101.com (select Python flavor)
- Print .group() / .groups() when debugging
- Test with edge cases
