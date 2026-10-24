# Folder map

This file holds the instance-specific bucket list for the file organizer. The build interview fills it from the user's actual folders; every later run reads it. Replace every `<placeholder>` below. Do not invent buckets.

## Default folder

- **Path:** `<folder path or Drive link>`

## Buckets

One line per allowed destination. The agent may not create categories outside this list. Always keep the three review paths.

```
<discovered-folder>/     <what belongs here, in their words>
_UNSORTED/               classified but no fitting bucket
_REVIEW/                 low confidence, needs a human
_REVIEW_DELETE/          proposed for deletion by a human
```

If this list still has `<discovered-folder>` and no real folders from the user, the clone is not set up. Stop. Do not fall back to a made-up tree.

## Naming

- **Pattern:** `<pattern, or keep original names>`
- **Entity field:** `<what entity means for them, or unused>`
- **Doctype field:** `<types they use, or unused>`
- **Version field:** `<v1 / v2 / final, or unused>`

If a field cannot be read from the file, keep the original filename. Do not guess a date.

## Do not touch

- `<paths or file types they said to leave alone, or none>`

## Read depth default

- `<in-depth | filenames-only>`

## Cadence

- ongoing — this agent keeps organizing. Do not ask one-time vs ongoing.
