# OHA program list

The program list behind the Ontario Home Assistance Team search at ontha.ca/team.

- `programs.json`: every program the search can return. The live site reads this file directly, so a change here appears for every rep within a few minutes.
- `municipalities.json`: the city and community lookup, mapping each place to its regional service area.
- `CHANGELOG.md`: one entry for every weekly check, listing what changed.
- `site/team/`: a copy of the Team pages as uploaded to ontha.ca.
- `tools/`: the script that built the October 2026 list.

To undo a bad update, revert the commit on GitHub. The site picks up the previous version automatically.

Every program lists who runs it and links to its official page. Ontario Home Assistance does not run any of these programs.
