# 🧩 Regex Log Extractor

**Regex Log Extractor** is a simple Streamlit tool for extracting values from logs using regular expressions.

Paste your log content, enter a regex pattern, and the tool will:

- Find matching lines
- Extract captured values
- Show the exact matched text
- Help developers and QA engineers inspect logs faster

Built with **Python + Streamlit**.

---

# 🚀 Demo

Try the tool online:

https://your-app-name.streamlit.app

---

# ❓ Why This Tool Exists

Logs often contain useful values hidden inside noisy text, such as:

- user IDs
- session IDs
- HTTP status codes
- request IDs
- exception names
- email addresses

This tool helps you quickly extract those values without manually scanning long logs.


## Example use cases

- Extract `user_id=12345` from application logs
- Extract `status=500` from API logs
- Extract `NullPointerException` from Android crash logs
- Extract emails or other custom fields from structured logs

# ✨ Features

- Apply regex patterns to logs
- Support capture groups
- Extract values line by line
- Show matching lines and matched text
- Includes built-in frontend examples for instant testing

# 🖥 Run Locally

Install dependencies
```
pip install -r requirements.txt
```

Run the Streamlit app
```
streamlit run app.py
```

Then open your browser:
```
http://localhost:8501
```

# 📁 Project Structure
```
logcat-error-filter
│
├── app.py
├── requirements.txt
└── README.md
```


# 🔍 Search Keywords

Developers may search for tools like this using keywords such as:

- regex log extractor

- extract values from logs

- regex log parser

- extract fields from logs

- regex tester for logs

- log pattern extractor

# 🔗 Related Tools

You may also be interested in:

- Crash Log Analyzer : https://crash-log-analyzer.streamlit.app
- Stack Trace Root Cause Finder : https://stack-trace-root-cause-finder.streamlit.app
- Logcat Error Filter : https://logcat-error-filter.streamlit.app
- API Error Parser : https://api-error-parser.streamlit.app
- Log Diff Analyzer : https://log-diff-analyzer.streamlit.app

These tools help developers debug logs more efficiently.