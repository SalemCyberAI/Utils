# Integrate Salem with Crowdstrike

This integration was designed for Crowdstrike

## Objective

The purpose of this integration is to send new alerts from Crowdstrike to Salem

## Approach

This integration leverages Azure Logic App workflow automation.  The design is to poll the CS API for new alerts, format those alerts and send them to Salem

To implement the logic app we will use an Azure Resource Manager (ARM) template to initiate and configure a consumption-based logic app.  If you already have a standard logic app, it would be advisable to take the logic app workflow code and add it to your existing logic app workspace.  Additionally, if you want to use advanced networking controls such as private endpoints and vNet integration, you will need to use a standard plan logic app.  

## What you'll need

* It may go without saying, but you need an Azure subscription, be a user of Microsoft Defender (Cloud or ATP) and have an active Salem (Salem Cyber) implementation.  You'll also need sufficient permissions to deploy new Azure resources, configure Microsoft Defender workflow automation and access Salem resources.
* The connection string from the 'alerts' EventHub namespace in the Salem EventHub.  You can find this key in the Azure portal for the event hub resource in the Salem managed resource group.  The key will already exist, however, you can generate a new key if you wish.  If you do create a new key, ensure the key has 'send' permissions.
* The API connection details from the crowdstrike console (CID, Secret and Base URL).  Information on how to create a new API connection can be found here [Crowdstrike Docs](https://www.crowdstrike.com/blog/tech-center/get-access-falcon-apis/)

## Getting Started

### Deploy Logic App to Azure

Select the below link to deploy this Defender to Salem integration in Azure

[Deploy to Azure](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2FSalemCyberAI%2FUtils%2Fmain%2FCrowdstrike%2FARM%2FDeployToAzure%2FmainTemplate.json)

### Update Event Hub network settings

The consumption plan log apps (which this is) use a fixed set of public IP addresses and you must update the network configuration of the Salem Event Hub to allow connections from these IPs.  You can find the IP ranges based on the region you deployed your logic app into, [here](https://learn.microsoft.com/en-us/connectors/common/outbound-ip-addresses)

If you want to use vNet integration or private endpoints to communicate between the logic app and the Salem event hub, you need to create a standard plan logic app.  Only the standard plan apps have advanced networking features.

### Key Vault Connection

The logic app is designed to read the CS API secret from a KeyVault.  The KeyVault is not included in this deployment.  You will need to use an existing KeyVault or create a new one.  Once the Logic app is created, you will need to add permission for the Logic App to read KeyVault Secrets.  To do this, assign the system-managed identity for the newly created logic app, the "Key Vault Secret User" role from IAM in the KeyVault Resource.

## Having Trouble?

Open an issue to start a discussion if you're finding a problem with the integration.
