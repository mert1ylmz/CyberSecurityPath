# PortSwigger Web Security Academy Notları

Bu dizin, PortSwigger Web Security Academy üzerinde tamamlanan lab çözümlerini ve ilgili güvenlik konularının açıklamalarını içermektedir.

## Dizin Yapısı

### 1. Server-Side Vulnerabilities
- **Path Traversal**
  - [File path traversal, simple case](file:///Users/mert/Projects/CyberSecurityPath/portswigger/path-traversal/lab-01-file-path-traversal-simple-case.md)

### 2. Access Control Vulnerabilities
- **Vertical Privilege Escalation**
  - [Unprotected admin functionality](file:///Users/mert/Projects/CyberSecurityPath/portswigger/access-control/lab-01-unprotected-admin-functionality.md)
  - [Unprotected admin functionality with unpredictable URL](file:///Users/mert/Projects/CyberSecurityPath/portswigger/access-control/lab-02-unprotected-admin-with-unpredictable-url.md)
- **Parameter-Based Access Control**
  - [User role controlled by request parameter](file:///Users/mert/Projects/CyberSecurityPath/portswigger/access-control/lab-03-user-role-controlled-by-request-parameter.md)
- **Horizontal Privilege Escalation & IDOR**
  - [User ID controlled by request parameter, with unpredictable user IDs](file:///Users/mert/Projects/CyberSecurityPath/portswigger/access-control/lab-04-user-id-controlled-by-request-parameter-with-unpredictable-user-ids.md)
- **Horizontal to Vertical Privilege Escalation**
  - [User ID controlled by request parameter with password disclosure](file:///Users/mert/Projects/CyberSecurityPath/portswigger/access-control/lab-05-user-id-controlled-by-request-parameter-with-password-disclosure.md)

### 3. Authentication Vulnerabilities
- **Brute Force & Username Enumeration**
  - [Username enumeration via different responses](file:///Users/mert/Projects/CyberSecurityPath/portswigger/authentication/lab-01-username-enumeration-via-different-responses.md)

### 4. Server-Side Request Forgery (SSRF)
- **Basic SSRF**
  - [Basic SSRF against the local server](file:///Users/mert/Projects/CyberSecurityPath/portswigger/ssrf/lab-01-basic-ssrf-against-the-local-server.md)
  - [Basic SSRF against another back-end system](file:///Users/mert/Projects/CyberSecurityPath/portswigger/ssrf/lab-02-basic-ssrf-against-another-back-end-system.md)

### 5. File Upload Vulnerabilities
- **Web Shell Upload**
  - [Remote code execution via web shell upload](file:///Users/mert/Projects/CyberSecurityPath/portswigger/file-upload/lab-01-remote-code-execution-via-web-shell-upload.md)
- **Content-Type Restriction Bypass**
  - [Web shell upload via Content-Type restriction bypass](file:///Users/mert/Projects/CyberSecurityPath/portswigger/file-upload/lab-02-web-shell-upload-via-content-type-restriction-bypass.md)

### 6. OS Command Injection
- **Simple Case**
  - [OS command injection, simple case](file:///Users/mert/Projects/CyberSecurityPath/portswigger/os-command-injection/lab-01-os-command-injection-simple-case.md)

### 7. SQL Injection
- **WHERE Clause & Hidden Data**
  - [SQL injection vulnerability in WHERE clause allowing retrieval of hidden data](file:///Users/mert/Projects/CyberSecurityPath/portswigger/sql-injection/lab-01-sqli-where-clause-hidden-data.md)
- **Login Bypass**
  - [SQL injection vulnerability allowing login bypass](file:///Users/mert/Projects/CyberSecurityPath/portswigger/sql-injection/lab-02-sqli-login-bypass.md)
- **UNION Attacks**
  - [SQL injection UNION attack, determining the number of columns returned by the query](file:///Users/mert/Projects/CyberSecurityPath/portswigger/sql-injection/lab-03-sqli-union-attack-determining-number-of-columns.md)
  - [SQL injection UNION attack, finding a column containing text](file:///Users/mert/Projects/CyberSecurityPath/portswigger/sql-injection/lab-04-sqli-union-attack-finding-column-containing-text.md)
  - [SQL injection UNION attack, retrieving data from other tables](file:///Users/mert/Projects/CyberSecurityPath/portswigger/sql-injection/lab-05-sqli-union-attack-retrieving-data-from-other-tables.md)
  - [SQL injection UNION attack, retrieving multiple values in a single column](file:///Users/mert/Projects/CyberSecurityPath/portswigger/sql-injection/lab-06-sqli-union-attack-retrieving-multiple-values-in-a-single-column.md)
- **Database Examination & Metadata**
  - [SQL injection attack, querying the database type and version on MySQL and Microsoft](file:///Users/mert/Projects/CyberSecurityPath/portswigger/sql-injection/lab-07-sqli-querying-database-type-and-version-mysql-microsoft.md)
  - [SQL injection attack, listing the database contents on non-Oracle databases](file:///Users/mert/Projects/CyberSecurityPath/portswigger/sql-injection/lab-08-sqli-listing-database-contents-non-oracle.md)
- **Blind SQL Injection**
  - [Blind SQL injection with conditional responses](file:///Users/mert/Projects/CyberSecurityPath/portswigger/sql-injection/lab-09-sqli-blind-conditional-responses.md)
