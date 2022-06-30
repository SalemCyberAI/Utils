param($Subscription,$ResourceGroupName,$ParameterFile,$TemplateFile)
. .\ConvertToHash.ps1

# Set Subscription Scope
Try {
    Set-AzContext -Subscription $Subscription -WarningAction Stop| Out-Null
}
Catch {
    # Attempt to Authenticate
    write-host "Follow pop-up prompt to login"
    Connect-AzAccount -Subscription $Subscription | Out-Null
}

# Collect Tempalate and Params
$paramsJson = Get-Content $ParameterFile| ConvertFrom-Json
$params = @{}
$paramsJson.parameters.PSObject.Properties |ForEach-Object {$params[$_.Name] = $_.Value.value}
$params.Remove('applicationResourceName')
$params.Remove('managedResourceGroupId')
"appId", "appObjectId", "appTenantId", "appSecret" | ForEach-Object {$params[$_] = "00000000-0000-0000-0000-000000000000"}
$template = Get-Content $TemplateFile | ConvertFrom-Json | ConvertPSObjectToHashtable

# initilize Variables and Constants
$n=0
$RGResource = @{
  type = "Microsoft.Resources/resourceGroups"
  apiVersion = "2021-04-01"
  name = "mrg-salem_cyber-20220218000000"
  location = "[variables('resourcesLocation')]"
}
$MSIResource = @{
    type = "Microsoft.ManagedIdentity/userAssignedIdentities"
    apiVersion = "2018-11-30"
    name = "[variables('identityResourceName')]"
    location = "[variables('resourcesLocation')]"
}
[System.Collections.ArrayList]$resources = $template.resources
$resources.Add($RGResource) | Out-Null

# Iterate over resources
$resources | ForEach-Object {
    $SingleResourceTemplate = @{
        parameters = $template.parameters
        resources = @($MSIResource,$_)
        outputs = @{}
        contentVersion = $template.contentVersion
        variables = $template.variables
    }
    $SingleResourceTemplate['$schema'] = $template.'$schema'
    if ($SingleResourceTemplate.resources[1].ContainsKey('dependsOn')) {
        $SingleResourceTemplate.resources[1].'dependsOn' = @($MSIResource.name)
    }
    $res = Test-AzResourceGroupDeployment -ResourceGroupName $ResourceGroupName -TemplateObject $SingleResourceTemplate -TemplateParameterObject $params
    
    if ($res.Message -and $res.Message -eq 'The template deployment failed because of policy violation. Please see details for more information.' ) {
        Write-Host '****************************'
        Write-Host $SingleResourceTemplate.resources[1].Type -ForegroundColor DarkYellow
        Write-Host $res.Details.Message
        Write-Host '****************************'
        $n += 1
    }
}

# Send Check Complete Message
Write-Host 
Write-Host "Check Complete"
Write-Host "Identified $n Azure Policy violations"
Write-Host


