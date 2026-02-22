# Telephony Setup Guide

This guide explains how to connect telephony providers (like Exotel) with LiveKit and set up inbound trunks and dispatch rules.

## Prerequisites

- LiveKit Cloud account or self-hosted LiveKit server
- API credentials for LiveKit
- Telephony provider account (Exotel, Twilio, etc.)

## Step 1: Create Inbound Trunk in LiveKit

An inbound trunk allows LiveKit to receive calls from telephony providers.

### Using LiveKit API

Create an inbound trunk with the following configuration:

```json
{
  "name": "trunk name",
  "numbers": [
    "+91123456789"
  ],
  "krispEnabled": true
}
```
**Note:** Save the `trunkId` from the response - you'll need it for the dispatch rule.

## Step 2: Create Dispatch Rule

A dispatch rule routes incoming calls from trunks to your agent.

### Using LiveKit API

Create a dispatch rule with the following configuration:

```json
{
  "rule": {
    "dispatchRuleIndividual": {
      "roomPrefix": "call-"
    }
  },
  "trunkIds": [
    "replace with inbound trunk id"
  ],
  "name": "dispatch name",
  "roomConfig": {
    "agents": [
      {
        "agentName": "give agent name for explicit dispatch"
      }
    ]
  }
}
```


## Step 3: Verify Setup

1. Make a test call to your configured phone number
2. Check LiveKit dashboard for incoming call
3. Verify agent connects and responds
4. Check logs for any connection issues

## Troubleshooting

### Common Issues

- **No incoming calls**: Verify trunk ID matches in dispatch rule
- **Agent not connecting**: Check agent name matches in dispatch rule
- **Audio issues**: Ensure `krispEnabled: true` for noise cancellation
- **SIP connection failed**: Verify SIP credentials and endpoint URL

