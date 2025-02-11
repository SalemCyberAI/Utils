# Salem Bot for Slack
Salem has released for support for Slack for both oAuth and Salem Chat.  

Before installing the Slack app, you'll need to install Salem.  See https://docs.salemcyber.com/initiation-guides/quickstart-deploy-salem for details on how to deploy Salem.

## Create Slack App
1. Visit the Slack Apps Page for your workspace https://api.slack.com/apps
2. Create a new app from a manifest
3. Select YAML and then copy and paste the contents of Salem_Slack_manifest.yaml
4. Before moving on, you'll need to change two update the two request_url values to reflect the name of your Salem instance.  This value can be found in the Salem Azure Manageded Application Outputs (botAppName) for self hosted Salem, or requested from Salem support.
5. Verify the App parameters and select "create"

## Authorize Slack App

The Salem bot service needs to be authorized to use this Slack app.  This is done from the Azure Portal and the Azure Bot resource which is located in the Salem managed resource group.

1. From the Azure Bot Resoruce, navigate to Channels
2. Find the Slack channel and add the following parameters fro your Slack app (found on the apps basic information settings)
    * Client ID
    * Client Secret
    * Signing Secret
3. Keep the default selection of Permission Scopes
4. Select the link to Authorize the app, and follow the propts.

## Provide Details to Salem Support

At present, some settings can only be updated by Salem support.  Please reach out to your Salem support contact or mailto:support@salemcyber.com and provide the following values:

* slackSigningSecret: Slack App > Basic Information (scroll down) > App Credentials > Signing Secret
* slackBotToken: Slack App > OAuth & Permissions > Bot User OAuth Token

## Slack OAuth
If you are planning on using Slack OAuth to authenticate users, you'll need to configure oAuth settings in the Azuer Bot App.

1. From the Azure bot resource in the Azure portal.  Navigate to Configuration
2. Select "Add OAuth Connection Settings"
3. Provide the following parameters:
    * Name: **Slack**
    * Service Proiver: **Slack**
    * Client ID: From the Slack app basic information settings
    * Client secret: from the Slack app basic information settings
    * Scopes: **identity.basic,identity.email**
4. Save
5. Select the new connection (Name 'Slack') in the table
6. Test Connection
