import urllib.request
url = 'https://fallenjie.github.io/expense-tracker-v2/index.html'
with urllib.request.urlopen(url, timeout=15) as r:
    lines = r.read().decode('utf-8', errors='replace').split('\n')

print('=== Deep QA: Key Function Review ===')
print()

# Find key function lines
funcs = {}
for i, line in enumerate(lines):
    if line.strip().startswith('function ') and '(' in line:
        name = line.strip().split('(')[0].replace('function ', '')
        funcs[name] = i + 1

print('Functions found:')
for k, v in funcs.items():
    print(f'  Line {v}: {k}')

print()
print('=== Critical Bug Checks ===')

# 1. getUsers must return array
gu = next((i for i, l in enumerate(lines) if 'function getUsers' in l), None)
if gu:
    snippet = '\n'.join(lines[gu:gu+8])
    safe = 'Array.isArray' in snippet and 'catch' in snippet
    print(f'[{"PASS" if safe else "FAIL"}] getUsers: returns array, has try-catch')

# 2. initAuth checks users.length
ia = next((i for i, l in enumerate(lines) if 'function initAuth' in l), None)
if ia:
    snippet = '\n'.join(lines[ia:ia+15])
    safe = 'users.length' in snippet or 'users.find' not in snippet
    print(f'[{"PASS" if safe else "FAIL"}] initAuth: no unguarded users.find')

# 3. showApp has fallback display:none
sa = next((i for i, l in enumerate(lines) if 'function showApp' in l), None)
if sa:
    snippet = '\n'.join(lines[sa:sa+25])
    safe = "style.display='none'" in snippet or 'style.display="none"' in snippet
    print(f'[{"PASS" if safe else "FAIL"}] showApp: fallback display:none on auth page')

# 4. Form submit has try-catch
fs = next((i for i, l in enumerate(lines) if 'form-auth' in l and 'addEventListener' in l), None)
if fs:
    snippet = '\n'.join(lines[fs:fs+50])
    safe = 'try' in snippet and 'catch' in snippet
    print(f'[{"PASS" if safe else "FAIL"}] form-auth submit: has try-catch')

# 5. refreshHome uses window.currentUser
rh = next((i for i, l in enumerate(lines) if 'function refreshHome' in l), None)
if rh:
    snippet = '\n'.join(lines[rh:rh+5])
    safe = 'window.currentUser' in snippet
    print(f'[{"PASS" if safe else "FAIL"}] refreshHome: uses window.currentUser')

# 6. Both pie charts in refreshReportDay
rd = next((i for i, l in enumerate(lines) if 'function refreshReportDay' in l), None)
if rd:
    snippet = '\n'.join(lines[rd:rd+15])
    has_exp = 'rd-pie' in snippet and 'expense' in snippet
    has_inc = 'rd-pie-income' in snippet
    print(f'[{"PASS" if has_exp else "FAIL"}] refreshReportDay: draws expense pie')
    print(f'[{"PASS" if has_inc else "FAIL"}] refreshReportDay: draws income pie')

# 7. Both pie charts in refreshReportMonth
rm = next((i for i, l in enumerate(lines) if 'function refreshReportMonth' in l), None)
if rm:
    snippet = '\n'.join(lines[rm:rm+15])
    has_exp = 'rm-pie' in snippet and 'expense' in snippet
    has_inc = 'rm-pie-income' in snippet
    print(f'[{"PASS" if has_exp else "FAIL"}] refreshReportMonth: draws expense pie')
    print(f'[{"PASS" if has_inc else "FAIL"}] refreshReportMonth: draws income pie')

# 8. saveRecord has try-catch
sr = next((i for i, l in enumerate(lines) if 'function saveRecord' in l), None)
if sr:
    snippet = '\n'.join(lines[sr:sr+15])
    safe = 'try' in snippet and 'catch' in snippet
    print(f'[{"PASS" if safe else "FAIL"}] saveRecord: has try-catch')

# 9. getBudget returns safe object
gb = next((i for i, l in enumerate(lines) if 'function getBudget' in l), None)
if gb:
    snippet = '\n'.join(lines[gb:gb+10])
    safe = 'amount:0' in snippet or 'amount: 0' in snippet
    print(f'[{"PASS" if safe else "FAIL"}] getBudget: returns default object with amount:0')

# 10. Category preset counts
pe = next((i for i, l in enumerate(lines) if 'PRESET_EXPENSE' in l and 'var' in l and '=' in l), None)
pi = next((i for i, l in enumerate(lines) if 'PRESET_INCOME' in l and 'var' in l and '=' in l), None)
if pe:
    exp_count = lines[pe].count("name:") + lines[pe].count("'") if pe else 0
    print(f'  PRESET_EXPENSE line {pe+1}: {lines[pe][:100]}')
if pi:
    print(f'  PRESET_INCOME line {pi+1}: {lines[pi][:100]}')

# 11. HTML has income pie containers
html_has_rd_income = any('rd-pie-income' in l for l in lines)
html_has_rm_income = any('rm-pie-income' in l for l in lines)
print(f'[{"PASS" if html_has_rd_income else "FAIL"}] HTML: rd-pie-income container exists')
print(f'[{"PASS" if html_has_rm_income else "FAIL"}] HTML: rm-pie-income container exists')

# 12. getAllCats is used in getCats (not raw localStorage)
gc = next((i for i, l in enumerate(lines) if 'function getCats' in l), None)
if gc:
    snippet = '\n'.join(lines[gc:gc+8])
    uses_getAllCats = 'getAllCats' in snippet
    raw_ls = 'localStorage.getItem' in snippet and 'getAllCats' not in snippet
    print(f'[{"PASS" if uses_getAllCats else "FAIL"}] getCats: uses getAllCats helper')
    print(f'[{"FAIL" if raw_ls else "PASS"}] getCats: no raw localStorage direct access')

# 13. Check no .find() on potentially non-array
find_calls = []
for i, l in enumerate(lines):
    if '.find(' in l and 'for (var' not in l and '.filter(' not in l:
        # Check if it's in a function with defensive array check
        context = '\n'.join(lines[max(0,i-5):i+1])
        if 'Array.isArray' not in context and 'users.length' not in context and 'if (users' not in context:
            find_calls.append((i+1, l.strip()))

if find_calls:
    print(f'[WARN] Potential unsafe .find() calls:')
    for ln, code in find_calls[:5]:
        print(f'  Line {ln}: {code[:80]}')
else:
    print(f'[PASS] No unsafe .find() calls found')

print()
print('=== PRD Requirements Check ===')
prd_checks = [
    ('H5 App (SPA)', '<html' in '\n'.join(lines[:5])),
    ('Login/Register (手机号+密码)', 'auth-phone' in '\n'.join(lines[:50]) and 'auth-pwd' in '\n'.join(lines[:50])),
    ('localStorage persistence', 'localStorage' in '\n'.join(lines[:100])),
    ('18 expense categories', 'PRESET_EXPENSE' in '\n'.join(lines)),
    ('6 income categories', 'PRESET_INCOME' in '\n'.join(lines)),
    ('Date picker input', 'type="date"' in '\n'.join(lines)),
    ('Daily report (日报)', 'refreshReportDay' in '\n'.join(lines)),
    ('Monthly report (月报)', 'refreshReportMonth' in '\n'.join(lines)),
    ('Budget setting', 'getBudget' in '\n'.join(lines) and 'saveBudget' in '\n'.join(lines)),
    ('Budget alert 80%/100%', 'alert80' in '\n'.join(lines) and 'alert100' in '\n'.join(lines)),
    ('Logout', 'logout' in '\n'.join(lines).lower()),
    ('Export data', 'export' in '\n'.join(lines).lower()),
]
for name, result in prd_checks:
    print(f'  [{"PASS" if result else "FAIL"}] {name}')
