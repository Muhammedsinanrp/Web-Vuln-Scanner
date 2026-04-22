import requests

target = input("Enter URL (e.g. http://testphp.vulnweb.com): ")

# Make sure URL starts correctly
if not target.startswith("http"):
    target = "http://" + target

xss_payload = "<script>alert(1)</script>"
sql_payload = "' OR '1'='1"

def scan_xss(url):
    test_url = url + "?q=" + xss_payload
    try:
        response = requests.get(test_url, timeout=5)
        if xss_payload in response.text:
            print(f"[VULNERABLE] XSS detected at: {test_url}")
        else:
            print("[INFO] No XSS detected")
    except Exception as e:
        print("[ERROR] XSS scan failed:", e)

def scan_sql(url):
    test_url = url + "?id=" + sql_payload
    try:
        response = requests.get(test_url, timeout=5)
        errors = ["sql", "mysql", "syntax", "ora-", "database error"]
        
        if any(error in response.text.lower() for error in errors):
            print(f"[VULNERABLE] SQL Injection detected at: {test_url}")
        else:
            print("[INFO] No SQL Injection detected")
    except Exception as e:
        print("[ERROR] SQL scan failed:", e)

print("\nStarting scan...\n")

scan_xss(target)
scan_sql(target)

print("\nScan complete.")