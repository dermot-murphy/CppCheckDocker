# CppCheckDocker gh-pages

This orphan branch stores the runtime image-size history for
CppCheckDocker (issue #42). Each merge to `develop` or `main` appends
a row to `image_size_history.csv` and re-renders
`image_size_trend.svg`.

- `image_size_history.csv` - `timestamp,commit,branch,size_bytes`
- `image_size_trend.svg` - chart rendered by `scripts/plot_image_size.py`

The chart is embedded in the repository README via
`raw.githubusercontent.com/<owner>/<repo>/gh-pages/image_size_trend.svg`.
