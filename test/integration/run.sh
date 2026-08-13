#!/usr/bin/env bash
set -euo pipefail

IMAGE="${1:?usage: test/integration/run.sh <image-tag>}"

# Docker Desktop on Windows/Git-Bash needs a Windows-native path (U:/...) for -v;
# Linux and macOS use the standard POSIX path. `pwd -W` is Git-Bash specific.
if pwd -W >/dev/null 2>&1; then
    SAMPLES="$(cd "$(dirname "$0")/../samples" && pwd -W)"
    export MSYS_NO_PATHCONV=1
else
    SAMPLES="$(cd "$(dirname "$0")/../samples" && pwd)"
fi

FAIL=0

run_case() {
    local name="$1"; shift
    local expected_exit="$1"; shift
    local expected_regex="$1"; shift
    echo "▶ $name"

    # tmpfs on /tmp so cppcheck addons (which need a writable dump location)
    # can use --cppcheck-build-dir=/tmp/... while /work stays read-only.
    local output actual_exit=0
    output=$(docker run --rm --tmpfs /tmp:rw,mode=1777 \
                        -v "$SAMPLES:/work:ro" "$IMAGE" "$@" 2>&1) || actual_exit=$?

    if [ "$actual_exit" -ne "$expected_exit" ]; then
        echo "  FAIL: expected exit $expected_exit, got $actual_exit"
        echo "  --- output ---"
        echo "$output" | sed 's/^/  /'
        echo "  --------------"
        FAIL=1
        return
    fi

    if [ -n "$expected_regex" ] && ! grep -qE "$expected_regex" <<<"$output"; then
        echo "  FAIL: expected output matching /$expected_regex/"
        echo "  --- output ---"
        echo "$output" | sed 's/^/  /'
        echo "  --------------"
        FAIL=1
        return
    fi

    echo "  PASS"
}

# INT-001: cppcheck on PATH via entrypoint
run_case "INT-001 version" 0 "^Cppcheck [0-9]" --version

# INT-003: default CMD (no args) prints help — but we already invoked with --version above.
# Explicit help check:
run_case "INT-003 default help mentions tool name" 0 "Cppcheck" --help

# INT-007 + INT-010: --enable=all on clean file → exit 0, no findings.
# --suppress=missingIncludeSystem: expected in this env since system headers are not present in the image.
run_case "INT-010 clean.c produces no findings" 0 "" --enable=all --error-exitcode=1 --suppress=missingIncludeSystem clean.c

# INT-011: --error-exitcode=1 on defective input → non-zero, defect string reported
run_case "INT-011 buggy.c defect + non-zero exit" 1 "arrayIndexOutOfBounds" --enable=all --error-exitcode=1 buggy.c

# INT-012: without --error-exitcode, defects reported but exit is zero
run_case "INT-012 buggy.c defect + zero exit (no --error-exitcode)" 0 "arrayIndexOutOfBounds" --enable=all buggy.c

# INT-013: XML output format
run_case "INT-013 XML output" 0 "<errors>" --xml --enable=all buggy.c

# INT-040: MISRA addon runs AND rule-texts file was loaded.
# We assert on the *human-readable* rule text ("The goto statement should not be used"),
# which only appears when misra.py successfully loaded the bundled rule-texts file.
# This step fails loudly if:
#   • the rule-texts file is missing from the image,
#   • python3 is missing at runtime,
#   • cppcheck cannot execute addons (build lacks the required support),
#   • the misra-c2012.py shim is missing or the rule-texts path in it is wrong.
# --cppcheck-build-dir=/tmp: the addon requires a writable dump location; /work is bound ro.
run_case "INT-040 MISRA addon + bundled rule-texts" 0 \
    "The goto statement should not be used.*\[misra-c2012-15\.1\]" \
    --enable=style --addon=misra-c2012 --cppcheck-build-dir=/tmp misra_bad.c

if [ "$FAIL" -eq 0 ]; then
    echo "All integration tests passed."
else
    echo "One or more integration tests failed."
fi
exit "$FAIL"
