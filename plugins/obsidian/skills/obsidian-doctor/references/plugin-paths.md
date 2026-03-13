# Plugin Path Fields Reference

Which JSON fields in each plugin/core config contain folder paths. Use this to know exactly where to look and fix stale paths.

## Plugin Configs (`.obsidian/plugins/*/data.json`)

### periodic-notes
- `calendarSets[].day.folder` -- Daily notes folder
- `calendarSets[].day.templatePath` -- Daily template path
- `calendarSets[].week.folder` / `.templatePath`
- `calendarSets[].month.folder` / `.templatePath`
- `calendarSets[].quarter.folder` / `.templatePath`
- `calendarSets[].year.folder` / `.templatePath`
- Legacy fields: `daily.folder`, `weekly.folder`, etc.

### notebook-navigator
- `periodicNotesFolder` -- root folder for periodic notes
- `calendarTemplateFolder` -- template folder path
- `calendarCustomDailyPattern` / `calendarCustomWeekPattern` / `calendarCustomMonthPattern` / `calendarCustomQuarterPattern` / `calendarCustomYearPattern`
- `calendarCustomDailyTemplate` / `calendarCustomWeekTemplate` / `calendarCustomMonthTemplate` / `calendarCustomQuarterTemplate` / `calendarCustomYearTemplate`

### auto-mover
- Rules array: each rule has a `dest` field (destination folder)
- `excludedFolders[]` -- folders excluded from auto-move

### templater-obsidian
- `templates_folder` -- folder containing templates
- `excluded_folder` -- folder excluded from templater processing

### obsidian-eagle-plugin
- `cacheFolderName` -- Eagle image cache folder within vault

### homepage
- `defaultNote` -- note path for homepage (check both desktop and mobile entries)

### zotlit
- `literatureNoteFolder` -- where literature notes are created
- `template.folder` -- template folder for Zotero notes

### omnisearch
- `ignoredFolders[]` -- folders excluded from search indexing

### obsidian-linter
- `foldersToIgnore[]` -- folders excluded from linting

## Core Configs (`.obsidian/*.json`)

### workspace.json
- `lastOpenFiles[]` -- array of recently opened file paths
- Pane state objects may contain `file` fields with note paths

### workspaces.json
- Each workspace snapshot contains file paths in pane state objects
- Structure: `workspaces.{name}.{...}.state.file`

### hotkeys.json
- Templater command IDs embed template paths (e.g., `templater-obsidian:<templates-folder>/...`)

### templates.json
- `folder` -- templates folder path

### bookmarks.json
- Bookmarked items contain `path` fields pointing to files/folders
- Nested groups can contain bookmarks at any depth

### webviewer.json
- `markdownPath` -- folder path for saved web content

## Patterns to Watch

1. **Numbered prefixes**: Some vaults use decade-prefix convention (e.g., `60. Saint/61. Sermon/`). When a parent folder is renamed, child folder references may also need updating.

2. **Nested paths**: A path like `10. Time/01. Calendar/01. Daily Notes` -- if `10. Time` is renamed, all nested references break.

3. **Template paths vs folder paths**: Some fields store full file paths (including `.md`), others store just folder paths. Match accordingly.

4. **Slash sensitivity**: Some configs use trailing slash, others don't. Check both `"Old Folder"` and `"Old Folder/"`.
