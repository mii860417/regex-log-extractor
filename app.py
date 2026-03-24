import re
from typing import List, Dict, Any

import requests
import streamlit as st


FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSemB7XiPBrg_BJx3k_m0o_JHXfbhleKEdwu78vVOVidEByCdw/formResponse"

FIELD_TOOL_NAME = "entry.38392295"
FIELD_EVENT_TYPE = "entry.1467972143"
FIELD_INPUT_SOURCE = "entry.2139090681"
FIELD_NOTE = "entry.2065255547"


def is_keep_alive() -> bool:
    try:
        return str(st.query_params.get("keep_alive", "")).lower() in {"1", "true", "yes"}
    except Exception:
        return False


def track(tool_name: str, event_type: str, input_source: str = "none", note: str = "") -> None:
    if is_keep_alive():
        return

    data = {
        FIELD_TOOL_NAME: tool_name,
        FIELD_EVENT_TYPE: event_type,
        FIELD_INPUT_SOURCE: input_source,
        FIELD_NOTE: note,
    }

    try:
        requests.post(FORM_URL, data=data, timeout=5)
    except Exception:
        pass


TOOL_NAME = "Regex Log Extractor"
TOOL_SLUG = "regex-log-extractor"


st.set_page_config(
    page_title=TOOL_NAME,
    page_icon="🧩",
    layout="wide",
)


def load_example(example_name: str):
    examples = {
        "Extract user_id from logs": {
            "log": """2026-03-17 10:00:01 INFO login success user_id=12345 session=abc123
2026-03-17 10:00:05 INFO fetch profile user_id=67890 session=def456
2026-03-17 10:00:09 WARN token refresh failed user_id=12345 session=ghi789""",
            "pattern": r"user_id=(\d+)",
            "description": "Extract all user IDs from application logs.",
        },
        "Extract API status codes": {
            "log": """[INFO] GET /api/profile -> status=200 latency=120ms
[INFO] POST /api/order -> status=201 latency=245ms
[ERROR] GET /api/payment -> status=500 latency=980ms""",
            "pattern": r"status=(\d+)",
            "description": "Extract HTTP status codes from API logs.",
        },
        "Extract Android exception names": {
            "log": """01-10 10:00:03.300 E/AndroidRuntime: FATAL EXCEPTION: main
01-10 10:00:03.301 E/AndroidRuntime: java.lang.NullPointerException
01-10 10:00:03.302 E/AndroidRuntime: at com.example.app.MainActivity.onCreate(MainActivity.kt:42)""",
            "pattern": r"java\.lang\.([A-Za-z]+Exception)",
            "description": "Extract Java exception names from Android crash logs.",
        },
        "Extract email addresses": {
            "log": """INFO user email=jane@example.com action=signup
INFO user email=bob@company.org action=login
WARN notify failed email=alice@test.net retry=1""",
            "pattern": r"email=([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,})",
            "description": "Extract email addresses from log lines.",
        },
    }
    return examples[example_name]


def extract_matches(log_text: str, pattern: str, ignore_case: bool) -> Dict[str, Any]:
    flags = re.IGNORECASE if ignore_case else 0

    try:
        compiled = re.compile(pattern, flags)
    except re.error as exc:
        return {
            "success": False,
            "error": str(exc),
            "matches": [],
            "rows": [],
            "group_count": 0,
            "matched_line_count": 0,
        }

    lines = [line for line in log_text.splitlines() if line.strip()]
    rows: List[Dict[str, Any]] = []
    flat_matches: List[str] = []

    for idx, line in enumerate(lines, start=1):
        line_matches = list(compiled.finditer(line))
        if not line_matches:
            continue

        for match in line_matches:
            if match.groups():
                captured_values = list(match.groups())
            else:
                captured_values = [match.group(0)]

            rows.append(
                {
                    "line_number": idx,
                    "line_text": line,
                    "matched_text": match.group(0),
                    "captured_values": captured_values,
                }
            )
            flat_matches.extend(captured_values)

    group_count = compiled.groups
    matched_line_count = len({row["line_number"] for row in rows})

    return {
        "success": True,
        "error": None,
        "matches": flat_matches,
        "rows": rows,
        "group_count": group_count,
        "matched_line_count": matched_line_count,
    }


def detect_input_source(
    log_text: str,
    pattern: str,
    default_log: str,
    default_pattern: str,
    example_choice: str,
) -> str:
    is_exact_example = (
        example_choice != "None"
        and log_text.strip() == default_log.strip()
        and pattern.strip() == default_pattern.strip()
    )
    return "example" if is_exact_example else "custom"


def is_qualified_custom_input(log_text: str, pattern: str, input_source: str) -> bool:
    return (
        input_source == "custom"
        and len(log_text.strip()) > 20
        and len(pattern.strip()) > 0
    )


st.title("🧩 Regex Log Extractor")
st.caption(
    "Paste logs and a regex pattern to extract values like user IDs, status codes, exception names, emails, and more."
)

if "tracked_visitor" not in st.session_state:
    track(TOOL_SLUG, "visitor")
    st.session_state["tracked_visitor"] = True

with st.sidebar:
    st.header("Examples")
    example_choice = st.selectbox(
        "Load a sample",
        [
            "None",
            "Extract user_id from logs",
            "Extract API status codes",
            "Extract Android exception names",
            "Extract email addresses",
        ],
    )

    st.markdown("---")
    st.markdown("### What this tool does")
    st.markdown(
        """
- Apply regex patterns to logs
- Extract matching values
- Show which lines matched
- Support capture groups
"""
    )

if example_choice != "None":
    example = load_example(example_choice)
    default_log = example["log"]
    default_pattern = example["pattern"]
    default_description = example["description"]
else:
    default_log = ""
    default_pattern = ""
    default_description = ""

if default_description:
    st.info(default_description)

col1, col2 = st.columns([1.5, 1])

with col1:
    log_text = st.text_area(
        "Log Input",
        value=default_log,
        height=320,
        placeholder="Paste logs here...",
    )

with col2:
    pattern = st.text_input(
        "Regex Pattern",
        value=default_pattern,
        placeholder=r"e.g. user_id=(\d+)",
    )
    ignore_case = st.checkbox("Ignore case", value=False)

    st.markdown("### Tips")
    st.markdown(
        r"""
- Use `(...)` to capture values
- If no capture group exists, the full match will be returned
- Example: `status=(\d+)`
- Example: `java\.lang\.([A-Za-z]+Exception)`
"""
    )

analyze_clicked = st.button("Extract Values", type="primary")

if analyze_clicked:
    input_clean = log_text.strip()
    pattern_clean = pattern.strip()

    if not input_clean:
        st.error("Please paste log content first.")
        st.stop()

    if not pattern_clean:
        st.error("Please enter a regex pattern.")
        st.stop()

    input_source = detect_input_source(
        log_text=log_text,
        pattern=pattern,
        default_log=default_log,
        default_pattern=default_pattern,
        example_choice=example_choice,
    )

    track(
        tool_name=TOOL_SLUG,
        event_type="click",
        input_source=input_source,
    )

    result = extract_matches(
        log_text=log_text,
        pattern=pattern,
        ignore_case=ignore_case,
    )

    if not result["success"]:
        st.error(f"Invalid regex pattern: {result['error']}")
        st.stop()

    if is_qualified_custom_input(log_text, pattern, input_source):
        track(
            tool_name=TOOL_SLUG,
            event_type="qualified",
            input_source=input_source,
        )

    st.success("Extraction complete")

    summary_col1, summary_col2, summary_col3 = st.columns(3)
    summary_col1.metric("Total Extracted Values", len(result["matches"]))
    summary_col2.metric("Matched Lines", result["matched_line_count"])
    summary_col3.metric("Capture Groups", result["group_count"])

    st.markdown("## Extracted Values")
    if result["matches"]:
        unique_values = list(dict.fromkeys(result["matches"]))
        for value in unique_values:
            st.code(value)
    else:
        st.warning("No matches found.")

    st.markdown("## Match Details")
    if result["rows"]:
        for row in result["rows"]:
            with st.expander(f"Line {row['line_number']}"):
                st.markdown(f"**Original line:** `{row['line_text']}`")
                st.markdown(f"**Matched text:** `{row['matched_text']}`")
                st.markdown("**Captured values:**")
                for captured in row["captured_values"]:
                    st.code(captured)
    else:
        st.info("No matching lines found.")

st.markdown("---")
st.markdown(
    """
- Extract `user_id` or `session_id` from logs  
- Extract HTTP status codes from API logs  
- Extract exception names from stack traces or crash logs  
- Extract emails, timestamps, request IDs, or custom fields  
"""
)
st.caption("If this tool helped you, please ⭐ the GitHub repo.")
