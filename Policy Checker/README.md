# PolicyCheck
Check Salem Resource Deployment against existing Azure Policies in a specified Azure Subscription and Resource Group.  This utility doesn't install or update any Azure resources, it only validates that Salem resources can be deployed.

## Prerequisites
You must have permissions to install Azure resources in the specified Repository.  The policy check only returns indications of policy violations, not other types of errors.

Azure Az Powershell is required. [Docs here](https://docs.microsoft.com/en-us/powershell/azure/install-az-p)

`Install-Module -Name Az -Scope CurrentUser -Repository PSGallery -Force`

Clone this repository and run the policy checker locally from the downloaded directory

## Syntax
``
.\PolicyCheck.ps1
    -Subscription
    -ResourceGroupName
    -TemplateFile
    -ParameterFile
``

- Subscription: the name or ID of the existing Azure Subscription that you plan to deploy Salem into

- ResrouceGroupName: the name of the existing Azure resource group that you plan to deploy salem into

- TemplateFile: the file path to the Salem ARM template.  You can request this file from Salem Cyber by contacting us at info@salemcyber.com

- ParameterFile: the file path to the Salem Parameter file.  This is a json file you generate in the Azure Marketplace.  When you go to create an instance of Salem, you enter all the relevant information and at the bottom of the 'Review + create' tab you will see a link to Download a template for automation.  Copy the content from the 'parameters' tab into a new .json file, and reference that file path here.