import subprocess
import json

def get_sharepoint_navigation():
    powershell_command = """
    #warnung as UTF8 so you can remove them
    [Console]::OutputEncoding = [System.Text.Encoding]::UTF8
    $sourceSite = "site-URL"
    connect-PnPOnline -Url $sourceSite -OSLogin -ClientId "" -Tenant yourTenant
    
    Get-PnPNavigationNode -Location TopNavigationBar -Tree
    """
    powershellPath = "C:\\Program Files\\PowerShell\\7\\pwsh.exe"
    
    result = subprocess.run([powershellPath, '-ExecutionPolicy', 'ByPass', '-Command', powershell_command],
                            capture_output=True, text=True, encoding='utf-8')
    
    return result.stdout

def parse_hierarchy(data):
    lines = data.split('\n')
    hierarchy = []
    stack = [hierarchy]

    for line in lines:
        if line.strip():
            indent_level = (len(line) - len(line.lstrip())) // 2
            node = line.strip()
            parts = node.split(' - ')
            if len(parts) >= 3:
                title, url = parts[1], parts[2]
                new_node = {"Title": title, "Url": url, "Children": []}
                while len(stack) > indent_level + 1:
                    stack.pop()
                current_level = stack[-1]
                current_level.append(new_node)
                stack.append(new_node["Children"])

    return hierarchy
    
data = get_sharepoint_navigation()

hierarchy = parse_hierarchy(data)


with open('sharepointData_hub.json', 'w') as f:
    json.dump(hierarchy, f, indent=4)
    
    

