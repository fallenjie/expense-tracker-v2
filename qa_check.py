import urllib.request
url = 'https://fallenjie.github.io/expense-tracker-v2/index.html'
with urllib.request.urlopen(url, timeout=15) as r:
    content = r.read().decode('utf-8', errors='replace')

checks = [
    ('File size > 50KB', len(content) > 50000),
    ('Has localStorage', 'localStorage' in content),
    ('Has conic-gradient pie', 'conic-gradient' in content),
    ('Has getUsers function', 'function getUsers' in content),
    ('Has window.currentUser', 'window.currentUser' in content),
    ('Has rd-pie-income (income pie)', 'rd-pie-income' in content),
    ('Has rm-pie-income (income pie)', 'rm-pie-income' in content),
    ('Has drawPie function', 'function drawPie' in content),
    ('Has form-auth', 'form-auth' in content),
    ('Has showApp function', 'function showApp' in content),
    ('Has initAuth function', 'function initAuth' in content),
    ('Has refreshHome function', 'function refreshHome' in content),
    ('Has refreshReportDay', 'function refreshReportDay' in content),
    ('Has refreshReportMonth', 'function refreshReportMonth' in content),
    ('Has getBudget function', 'function getBudget' in content),
    ('Has saveRecord function', 'function saveRecord' in content),
    ('Has logout', 'logout' in content.lower()),
    ('Has budget alert', 'alert' in content and 'budget' in content.lower()),
    ('Has preset categories', 'PRESET_EXPENSE' in content and 'PRESET_INCOME' in content),
    ('Has date picker', 'type="date"' in content),
]

print('=== QA Static Checks ===')
for name, result in checks:
    status = 'PASS' if result else 'FAIL'
    print(f'  [{status}] {name}')

print()
print('=== Storage Functions ===')
storage_funcs = ['getUsers', 'setUsers', 'getLastUser', 'setLastUser',
    'getAllRecords', 'setAllRecords', 'getRecords', 'saveRecord', 'deleteRecord',
    'getAllCats', 'setAllCats', 'getCats', 'getCustomCats', 'saveCat', 'deleteCat',
    'getAllBudgets', 'getBudget', 'saveBudget',
    'getAllAlerted', 'setAllAlerted']
for f in storage_funcs:
    found = f in content
    print(f'  {"OK" if found else "MISSING"}: {f}')

print()
print('=== Key Code Snippets ===')
# getUsers
idx = content.find('function getUsers')
print('getUsers():', content[idx:idx+200] if idx >= 0 else 'MISSING')

# initAuth
idx2 = content.find('function initAuth')
print('initAuth():', content[idx2:idx2+200] if idx2 >= 0 else 'MISSING')

# refreshReportDay pie calls
idx3 = content.find('rd-pie-income')
print('rd-pie-income ref:', 'OK' if idx3 >= 0 else 'MISSING')

idx4 = content.find('rm-pie-income')
print('rm-pie-income ref:', 'OK' if idx4 >= 0 else 'MISSING')

# window.currentUser
idx5 = content.find('window.currentUser')
print('window.currentUser:', 'OK' if idx5 >= 0 else 'MISSING')

print()
print('Total file size:', len(content), 'bytes')
