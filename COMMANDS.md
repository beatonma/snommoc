# manage.py commands

### `puk_complete`

Updates:

- Constituencies
- All member profiles
- Election results
- Member portraits


### `divisions [-commons|-lords]`

Update division data for the specified House. If no House is specified, both will be updated.


### `bills -async`

Update bill data.


### `aliases`

Should run after `bills` to detect/match BillSponsor names with Person instances.


### `import_boundaries [kml_file]`

Imports constituency boundary data from the given .kml file.

The source file can be retrieved from https://geoportal.statistics.gov.uk/search?collection=Dataset&sort=name&tags=all(BDY_PCON)
and should be updated at least after every election.



### delete_pending

Permenantly delete any DeletionPendingMixin instances that have been marked for
deletion and have reached their expiry date.
