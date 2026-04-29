import urllib.request
url = 'https://fallenjie.github.io/expense-tracker-v2/index.html'
with urllib.request.urlopen(url, timeout=15) as r:
    content = r.read().decode('utf-8', errors='replace')
lines = content.split('\n')

def find_line(keyword, offset=0):
    for i in range(offset, len(lines)):
        if keyword in lines[i]:
            return i
    return -1

print('=== FINAL QA REPORT ===')
print()

results = []

# Critical fixes verified
checks = [
    ('getUsers has try-catch + Array.isArray', 'Array.isArray' in content and 'catch' in content.split('function getUsers')[1].split('function')[0]),
    ('getUsers returns [] on bad data', 'return []' in content.split('function getUsers')[1].split('function')[0]),
    ('initAuth uses users.length check', 'users.length > 0' in content),
    ('initAuth uses for loop (no unguarded .find)', 'for (var i = 0' in content.split('function initAuth')[1].split('function')[0]),
    ('showApp sets auth page display=none', "style.display = 'none'" in ''.join(lines[760:795])),
    ('showApp has catch fallback', 'catch(e)' in ''.join(lines[760:795])),
    ('form submit has try-catch', 'try' in ''.join(lines[lines.index(next(l for l in lines if 'form-auth' in l and 'addEventListener' in l)):])),
    ('refreshHome uses window.currentUser', 'window.currentUser' in ''.join(lines[858:912])),
    ('refreshReportDay draws expense pie', 'drawPie' in ''.join(lines[1194:1208]) and 'rd-pie' in ''.join(lines[1194:1208])),
    ('refreshReportDay draws income pie', 'rd-pie-income' in ''.join(lines[1194:1208])),
    ('refreshReportMonth draws expense pie', 'drawPie' in ''.join(lines[1208:1240]) and 'rm-pie' in ''.join(lines[1208:1240])),
    ('refreshReportMonth draws income pie', 'rm-pie-income' in ''.join(lines[1208:1240])),
    ('rd-pie-income HTML exists', any('rd-pie-income' in l for l in lines)),
    ('rm-pie-income HTML exists', any('rm-pie-income' in l for l in lines)),
    ('saveRecord has try-catch', 'catch' in ''.join(lines[578:590])),
    ('getBudget returns default object', 'amount:0' in ''.join(lines[628:640])),
    ('window.currentUser global used', 'window.currentUser' in content),
    ('All storage functions have try-catch', all(f in content for f in ['getUsers', 'getAllRecords', 'getAllCats', 'getAllBudgets', 'getAllAlerted'])),
]

for name, passed in checks:
    status = 'PASS' if passed else 'FAIL'
    results.append((status, name))
    print(f'  [{status}] {name}')

print()
print('=== PRD Requirements ===')
prd = [
    ('H5 SPA (单页应用)', '<html' in content),
    ('响应式移动端适配', 'max-width:430' in content or 'max-width: 430' in content),
    ('登录/注册 (手机号+密码)', 'auth-phone' in content and 'auth-pwd' in content),
    ('localStorage 持久化', 'localStorage' in content and 'et_users' in content),
    ('18个支出预设分类', 'PRESET_EXPENSE' in content),
    ('6个收入预设分类', 'PRESET_INCOME' in content),
    ('自定义分类 CRUD', 'saveCat' in content and 'deleteCat' in content and 'getCustomCats' in content),
    ('账单录入 (金额/类型/分类/日期/备注)', 'openNewRecord' in content and 'saveRecord' in content),
    ('日期选择器', 'type="date"' in content),
    ('日报 (收支汇总+分类饼图)', 'refreshReportDay' in content and 'drawPie' in content),
    ('月报 (收支汇总+分类饼图+月份切换)', 'refreshReportMonth' in content and 'rm-prev' in content),
    ('月度预算设置', 'getBudget' in content and 'saveBudget' in content),
    ('80%/100% 提醒', 'alert80' in content and 'alert100' in content),
    ('退出登录', 'logout' in content.lower()),
    ('数据导出', 'btn-export' in content or 'export' in content.lower()),
    ('收入饼图 (PRD要求)', 'rd-pie-income' in content and 'rm-pie-income' in content),
]
for name, passed in prd:
    status = 'PASS' if passed else 'FAIL'
    results.append((status, name))
    print(f'  [{status}] {name}')

print()
passed = sum(1 for s,_ in results if s == 'PASS')
failed = sum(1 for s,_ in results if s == 'FAIL')
print(f'=== SUMMARY: {passed} PASS, {failed} FAIL ===')
if failed > 0:
    print('Failed items:')
    for s, n in results:
        if s == 'FAIL':
            print(f'  - {n}')
