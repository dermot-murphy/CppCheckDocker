# ASPICE Release Records

This directory holds per-release evidence files produced by the [SPL.2 Software Release Plan](../CppCheckDocker_SPL2_Software_Release_Plan.md).

## Filenames

| Pattern | Content | Template |
|:--------|:--------|:---------|
| `CCD-SVD-<tag>.md` | Software Version Description — what was released, from where, containing what, verified how | [`CCD-SVD-001`](../CppCheckDocker_SVD_Software_Version_Description.md) |
| `CCD-QTR-<tag>.md` | Qualification Test Record — signed run of the QT cases in [CCD-SWE6-001](../CppCheckDocker_SWE6_Qualification_Test.md) §4 | Template in [CCD-SWE6-001 §4](../CppCheckDocker_SWE6_Qualification_Test.md) |

`<tag>` is the release tag, e.g. `2.21.1-r1`.

## Retention

Records are committed to Git and are therefore permanent and version-controlled. Do not delete or overwrite past records — supersede them with a new dated entry inside the same file if a correction is needed, and note the change in the file's Document Control table.
