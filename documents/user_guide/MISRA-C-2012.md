# MISRA C:2012

The image bundles the MISRA Consortium's official rule-texts file (CC BY-NC-ND 4.0) at `/opt/cppcheck/share/cppcheck/misra_c_2012_for_cppcheck.txt` and a shim addon at `/opt/cppcheck/share/cppcheck/addons/misra-c2012.py` that pre-supplies the rule texts to `misra.py`.

## Invoke the addon

```bash
docker run --rm -v "$(pwd):/work:ro" ghcr.io/dermot-murphy/cppcheckdocker:latest \
    --enable=style --addon=misra-c2012 --cppcheck-build-dir=/tmp src/
```

Output includes the human-readable guideline text next to each finding:

```
src/main.c:6:5: style: The goto statement should not be used [misra-c2012-15.1]
```

## `--cppcheck-build-dir=/tmp` is mandatory with a read-only mount

Cppcheck's addon step needs a writable location for the intermediate `.dump` files each rule uses. `/work` is bind-mounted read-only in the example above, so cppcheck cannot write there. Pointing `--cppcheck-build-dir` at `/tmp` (writable in the container) resolves this without giving up the read-only source mount.

If you drop `:ro` from the mount and let cppcheck write into `/work`, you can omit `--cppcheck-build-dir`.

## License

The bundled `misra_c_2012_for_cppcheck.txt` is redistributed unmodified under [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/). It is not a substitute for the full MISRA C:2012 guidelines document, which must be purchased separately from [misra.org.uk](https://misra.org.uk/) for commercial use.

## What is inside the image (MISRA paths)

| Path | Purpose |
|:-----|:--------|
| `/opt/cppcheck/share/cppcheck/misra_c_2012_for_cppcheck.txt` | MISRA C:2012 rule-texts file (CC BY-NC-ND 4.0) |
| `/opt/cppcheck/share/cppcheck/addons/misra.py` | Upstream MISRA addon shipped with cppcheck |
| `/opt/cppcheck/share/cppcheck/addons/misra-c2012.py` | CppCheckDocker shim that pre-supplies the rule-texts file to `misra.py` |
