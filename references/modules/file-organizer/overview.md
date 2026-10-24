# Module guide: File Organizer

> Integrated capability: classification method and naming convention for a file-organization agent. Allowed buckets, default folder, and naming fields live in `references/taxonomy.md` and are filled at build time from the user's own folders. Use on every run before any file is moved.

# File triage and taxonomy

Gives the organizer agent a fixed classification scheme and a naming convention so that runs are repeatable and two runs a month apart produce the same structure.

## When to use

On every run of the file-organization agent, before any file is moved.

## One-time setup — read the config

Instance specifics live in `references/taxonomy.md`: the default folder, the allowed buckets, naming fields, do-not-touch paths, and the read-depth default. If that file still has `<placeholder>` values, stop. The builder fills it during setup from the user's actual folders. Do not invent a folder tree.

## Classification

Assign each file to exactly one bucket from the config. If no category fits, assign `_UNSORTED` and say why. Do not invent categories.

Assign confidence: high, medium, or low. Anything below high goes to `_REVIEW` rather than being moved silently.

## Naming convention

Rename only when the config's pattern is filled and the fields can be determined from the file. Default pattern when the user confirmed one:

```
YYYY-MM-DD_<entity>_<doctype>_<version>.<ext>
```

Use the entity / doctype / version meanings recorded in the config. If any field cannot be determined, keep the original filename and flag the file. Do not guess a date.

## Duplicate detection procedure

1. Compute a content hash for every file. On Google Drive, `files.list` exposes `md5Checksum` for files with binary content — use it directly rather than re-downloading. Native Google Docs/Sheets/Slides have no MD5; compare exported content or revision history instead.
2. Group by identical hash. These are exact duplicates.
3. For documents with different hashes but very similar content, report them as near duplicates with a similarity note. Do not move or merge them. Let the human decide which is current.
4. Never assume the newest file is the correct one. The user decides which copy to keep.

## Output contract

Return a table with these columns and no others:

```
current_path | proposed_path | category | confidence | reason | duplicate_of | action
```

## Failure handling

If the target folder is larger than you can process in one pass, do not sample. Process it in explicit batches, report the batch boundaries, and tell the user how many files remain.
