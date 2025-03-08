function Parse-Navigation {
    param (
        [string]$filePath
    )
    $jsonContent = Get-Content -Path $filePath -Raw | ConvertFrom-Json
    return $jsonContent
}


function Import-Navigation {
    param (
        [array]$nodes
    )
    foreach ($node in $nodes) {
        $newNode = Add-PnPNavigationNode -Location TopNavigationBar -Title $node.Title -Url $node.Url
        if ($node.Children.Count -gt 0) {
            foreach ($child in $node.Children){
                $newChild = Add-PnPNavigationNode -Location TopNavigationBar -Title $child.Title -Url $child.Url -Parent $newNode.Id
                if($child.Children.Count -gt 0){
                    foreach ($lastChild in $child.Children){
                        Add-PnPNavigationNode -Location TopNavigationBar -Title $lastChild.Title -Url $lastChild.Url -Parent $newChild.Id
                    }
                }
            }
        }
    }
}

$filePath = "sharepointData_hub.json"



$parsedNavigation = Parse-Navigation -filePath $filePath

$targetSiteUrl = "Target SharePoint Site"
connect-PnPOnline -Url $targetSiteUrl -OSLogin -ClientId "Client ID" -Tenant yourTenant


Import-Navigation -nodes $parsedNavigation