---
type: weekly
week: <% tp.date.now("YYYY-[W]WW") %>
---
# Week <% tp.date.now("WW") %>
## Review
```dataview
TABLE deepwork, dsa, workout, music, writing
FROM "Daily" WHERE file.name >= "<% tp.date.now("YYYY-MM-DD", -6) %>" SORT file.name ASC
```
## Wins / Misses / Next week's 3 goals
