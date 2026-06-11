# Microsoft Foundry Access Issue

## Summary

Microsoft Foundry resource creation failed under the UTAS Azure for Students subscription due to Azure policy restrictions.

## Error

RequestDisallowedByAzure

The Azure error states that the Foundry resource is disallowed because the subscription policy maintains a set of best available regions where resources can be deployed.

## Account

UTAS organisational account:
habegum@utas.edu.au

Subscription:
Azure for Students

## Attempts Made

The project was attempted through:

- Microsoft Foundry portal: ai.azure.com
- Azure Portal: portal.azure.com

Regions attempted included:

- East US
- East US 2
- Australia East
- West US
- West US 3
- Sweden Central
- France Central
- UK South

## Current Impact

Microsoft Foundry cloud resource creation is blocked. Local project development is continuing with a Foundry-ready multi-agent architecture, synthetic data, synthetic knowledge documents, Streamlit dashboard, evaluation tests, and safety documentation.

## Resolution Plan

- Submit Azure support request with full error details.
- Ask which regions are allowed for Foundry under Azure for Students.
- Continue local multi-agent development while waiting for support.
- Connect to Microsoft Foundry once subscription/resource access is resolved.
