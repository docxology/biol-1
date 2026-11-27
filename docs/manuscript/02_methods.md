# Inventory methods {#sec:inventory-methods}

The audit fixes the public reference at commit
`19b2fd0647ba55de77fbbb385eda7a4ba6fe05de`. We enumerate tracked blobs with
`git ls-tree -rz`, split the NUL-delimited entries into path and object ID,
and classify paths by their top-level collection [@gitlstree]. This method
works from a blobless checkout because the inventory reads Git trees only.

The organized collection comprises the course, category directories, module
bundles, and top-level per-module quiz folders. We exclude landing documents
and bulk views from that collection. We count format pairs by shared filename
stems within a category. We compare both quiz paths and object IDs between the
per-module folders and the module bundles. For each bulk view, we compare the
complete set of blob IDs with the organized collection. An equal ID within
this Git snapshot identifies the same file bytes.

The machine-readable results include totals, paired format counts, and missing
or additional object counts for each bulk view. The figure uses those computed
values directly.
