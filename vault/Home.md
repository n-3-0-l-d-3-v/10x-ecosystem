---
type: dashboard
---
# LifeOS

## Today
```dataview
TABLE WITHOUT ID file.link AS "Daily", mood, energy
FROM "Daily" WHERE file.name = dateformat(date(today), "yyyy-MM-dd")
```

## Habit streaks (current run of consecutive days)
```dataviewjs
const habits = ["deepwork","dsa","workout","music","writing"];
const pages = dv.pages('"Daily"').where(p => /^\d{4}-\d{2}-\d{2}$/.test(p.file.name)).sort(p => p.file.name, "desc");
const byDay = new Map(pages.map(p => [p.file.name, p]));
const rows = habits.map(h => {
  let d = dv.date("today"), n = 0;
  if (!(byDay.get(d.toFormat("yyyy-MM-dd"))?.[h])) d = d.minus({days:1});
  while (byDay.get(d.toFormat("yyyy-MM-dd"))?.[h]) { n++; d = d.minus({days:1}); }
  return [h, n + " day(s)"];
});
dv.table(["Habit","Streak"], rows);
```

## Last 14 days
```dataview
TABLE deepwork, dsa, workout, music, writing, energy
FROM "Daily" SORT file.name DESC LIMIT 14
```

## Active projects
```dataview
TABLE type, status, sensitivity_tier AS tier
FROM "Projects" OR "agents/Vision" WHERE status = "active"
```

## Open tasks
```tasks
not done
due before in 7 days
sort by due
```

## Review queue (Alfred)
```dataview
TABLE next_due, mastery, streak_days
FROM "agents/Alfred" WHERE next_due <= date(today) + dur(3 days)
SORT next_due ASC
```

## Latest agent reports
```dataview
LIST FROM "agents/Wall-E" SORT file.name DESC LIMIT 3
```

## Content calendar
```dataview
TABLE platform, status, publish_on
FROM "Socials" WHERE status != "published" SORT publish_on ASC
```
