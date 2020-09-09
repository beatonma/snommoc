# manage.py commands


### `profiles [-all]`
Update constituencies and profile data for active members.

With `-all`, update profile data for all members (i.e. active and historic).


### `portraits`
Update member portraits/profile photos.


### `divisions [-commons|-lords]`

Update division data for the specified House. If no House is specified, both will be updated.


### `bills -async`

Update bill data.


### `aliases`

Should run after `bills` to detect/match BillSponsor names with Person instances.


### `electionresults`
Update election results for all constituencies in all elections.


### `import_boundaries [kml_file]`

Imports constituency boundary data from the given .kml file.

The source file can be retrieved from https://geoportal.statistics.gov.uk/search?collection=Dataset&sort=name&tags=all(BDY_PCON)
and should be updated at least after every election.


### `delete_pending`

Permenantly delete any DeletionPendingMixin instances that have been marked for
deletion and have reached their expiry date.
