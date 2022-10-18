# Integrate Salem with MS Defender

This integration was designed from Microsoft Defender for Cloud but should work with other Microsoft defender products.

## Objective

The purpose of this integration is to send new alerts from Microsoft Defender to Salem

## Approach

This integration leverages Azure Logic Apps and Defender workflow automation.  The design is to use workflow automation in Defender and an alert trigger to send all or a subset of alerts generated in Defender directly to Salem, as they occur.

To implement the logic app we will use an Azure Resource Manager (ARM) template to initiate and configure a consumption-based logic app.  If you already have a standard logic app, it would be advisable to take the logic app workflow code and add it to your existing logic app workspace.  Additionally, if you want to use advanced networking controls such as private endpoints and vNet integration, you will need to use a standard plan logic app.  

## What you'll need

* It may go without saying, but you need an Azure subscription, be a user of Microsoft defender and have an active Salem (Salem Cyber) implementation.  You'll also need sufficient permissions to deploy new Azure resources, configure Microsoft Defender workflow automation and access Salem resources.
* The connection string from the 'alerts' EventHub namespace in the Salem EventHub.  You can find this key in the azure portal for the event hub resource in the Salem managed resource group.  The key will already exist, however, you can generate a new key if you wish.  If you do create a new key, ensure the key has 'send' permissions.

## Getting Started

### Deploy Logic App to Azure

Select the below link to deploy this Defender to Salem integration in Azure

[Deploy to Azure](https://portal.azure.com/#create/Microsoft.Template)

### Add Defender workflow automation

1. Log into the [Defender for Cloud Console](https://portal.azure.com/#view/Microsoft_Azure_Security)

2. Under Workflow automation, select 'Add workflow automation

    * Select 'Security alert' in the Defender for Cloud data type dropdown
    * Select the subscription and logic app created above.  The Logic App name was by default 'Defender_to_Salem'.

3. Test the new integration by triggering the automated response for a security alert. From the Security alert page: select an alert > take action > Trigger automated response > select 'Defender_to_Salem' > Trigger .  You should be able the see if the automation was successful by selecting 'Defender_to_Salem' and reviewing the run status.

## Having Trouble?

Open an issue to start a discussion if you're finding a problem with the integration.
