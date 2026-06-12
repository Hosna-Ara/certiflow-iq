# Model Deployment Quota Issue

## Summary

Microsoft Foundry resource creation succeeded using the Azure for Students subscription in Southeast Asia. However, model deployment inside Microsoft Foundry failed due to insufficient quota.

## Foundry Resource

Resource name: certiflowAI  
Project: proj-default  
Resource group: rg-habegum-3396  
Region: Southeast Asia  
Subscription: Azure for Students  

## Issue

Attempted deployment of small chat models such as gpt-4o-mini, but Microsoft Foundry showed "Insufficient quota" for available deployment types.

## Current Development Decision

The project will continue with a local multi-agent implementation and Streamlit dashboard while keeping the architecture Foundry-ready. The repository documents the Microsoft Foundry resource, attempted model deployment, quota limitation, and planned integration path.

## Planned Resolution

- Recheck quota availability later.
- Try GitHub-hosted models if available through the hackathon or student access.
- Continue local Microsoft Agent Framework-style implementation.
- Connect to Foundry model deployment if quota becomes available.
