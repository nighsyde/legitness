# Claude Code Desktop + AWS Bedrock via IAM Identity Center

## Architect's Assessment

### Is This Possible?

**Yes — and it is the officially recommended enterprise authentication path.**

As of mid-2026, Anthropic's Claude Code desktop application (which bundles Claude Code CLI, Claude Cowork, and Chat) natively supports AWS IAM Identity Center (formerly AWS SSO) as a first-class authentication mechanism for Amazon Bedrock. Two distinct sub-paths exist depending on the target audience:

| Auth Sub-Path | Who It Suits | CLI Required | User Experience |
|---|---|---|---|
| **Named AWS Profile (SSO-backed)** | Individual developers already using the AWS CLI | Yes — AWS CLI v2 | `aws sso login` in terminal; app auto-refreshes via `awsAuthRefresh` |
| **In-App AWS Sign-in** | Knowledge workers, broad org rollout, no CLI familiarity | No | Browser-based SSO flow initiated directly inside Claude Code |

This guide focuses on the **Named AWS Profile path** — the most appropriate choice for a Mac developer who already operates in the AWS CLI ecosystem — and the **In-App SSO path** as an alternative.

### Why Identity Center Is the Right Approach

| Concern | Static IAM Access Keys | IAM Identity Center |
|---|---|---|
| Credential lifetime | Long-lived (manual rotation) | Short-lived (8-12 hr sessions, auto-refreshed) |
| CloudTrail identity | Shared key identity | Per-user identity (`AWSReservedSSO_*` role ARN) |
| Revocation | Manual key deactivation | Revoke session in Identity Center console immediately |
| MFA | Must be configured separately | Inherited from IdP (Okta, Entra ID, etc.) |
| Credential sprawl | High — keys stored in `~/.aws/credentials` | Minimal — tokens cached, short-lived |
| Enterprise IdP federation | Not applicable | SAML/OIDC to Okta, Entra ID, Google Workspace |

**Verdict:** IAM Identity Center is the correct enterprise choice. It eliminates long-lived static credentials, provides per-user CloudTrail attribution, and inherits your existing MFA and IdP policies.

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        Mac Developer Machine                     │
│                                                                  │
│   ┌─────────────────┐      aws sso login      ┌──────────────┐ │
│   │  Claude Code    │ ──── (browser flow) ──► │  ~/.aws/     │ │
│   │  Desktop App    │                          │  sso/cache/  │ │
│   │                 │ ◄── short-lived STS ──── │  (tokens)    │ │
│   └────────┬────────┘      credentials         └──────────────┘ │
│            │                                                      │
└────────────┼─────────────────────────────────────────────────────┘
             │  HTTPS / SigV4
             │  bedrock:InvokeModel
             ▼
┌─────────────────────────────────────────────────────────────────┐
│                          AWS Account                            │
│                                                                  │
│   ┌─────────────────────┐    ┌──────────────────────────────┐  │
│   │ IAM Identity Center  │    │       Amazon Bedrock         │  │
│   │                      │    │                              │  │
│   │  ┌────────────────┐  │    │  ┌────────────────────────┐ │  │
│   │  │ Permission Set │  │    │  │  Claude Models:        │ │  │
│   │  │ ClaudeCodeBed- │  │    │  │  • Claude Sonnet 4.6   │ │  │
│   │  │ rockAccess     │  │    │  │  • Claude Opus 4.x     │ │  │
│   │  │                │  │    │  │  • Claude Haiku 4.x    │ │  │
│   │  │ Inline Policy: │  │    │  └────────────────────────┘ │  │
│   │  │ bedrock:Invoke │  │    │                              │  │
│   │  │ Model (+ more) │  │    └──────────────────────────────┘  │
│   │  └────────────────┘  │                                      │
│   │                      │    ┌──────────────────────────────┐  │
│   │  ┌────────────────┐  │    │       AWS CloudTrail         │  │
│   │  │  User/Group    │  │    │  Per-user invocation logs    │  │
│   │  │  Assignment    │  │    │  (AWSReservedSSO_* ARN)      │  │
│   │  └────────────────┘  │    └──────────────────────────────┘  │
│   └─────────────────────┘                                       │
└─────────────────────────────────────────────────────────────────┘
```

---

## Prerequisites

Before starting, confirm the following:

- [ ] AWS account with **IAM Identity Center enabled** (enabled via AWS Console or Organizations; cannot be done via CloudFormation)
- [ ] You have **organization management account** access, or at minimum, IAM Identity Center admin rights
- [ ] **Amazon Bedrock model access** enabled for the models you want (Claude Sonnet, Opus, Haiku) in your target region
- [ ] **AWS CLI v2** installed on the Mac (`aws --version` → should show `aws-cli/2.x.x`)
- [ ] **Claude Code desktop** downloaded from [claude.com/download](https://claude.com/download) (v2.x+)
- [ ] A target AWS account ID (12-digit) where Bedrock will be called

---

## Part 1: AWS-Side Setup

### Step 1 — Enable Amazon Bedrock Model Access

1. Sign in to the AWS Console in your **target account** (the account users will invoke Bedrock from).
2. Navigate to **Amazon Bedrock** → **Model catalog**.
3. Locate each Claude model you plan to use (Sonnet, Opus, Haiku) and click **Request access** / **Submit use case details**.
4. Access is granted immediately after form submission.
5. Verify in **Model access** that each model shows **Access granted**.

> **Region note:** Model access is per-region. Enable models in the same region you will configure as `AWS_REGION` on developer machines.

### Step 2 — Create the Bedrock IAM Permission Set in Identity Center

1. Open **IAM Identity Center** in the AWS Console.
2. In the left menu, choose **Multi-account permissions** → **Permission sets**.
3. Click **Create permission set**.
4. Select **Custom permission set**.
5. Set the following:

   | Field | Value |
   |---|---|
   | Name | `ClaudeCodeBedrockAccess` |
   | Description | `Allows Claude Code desktop to invoke Amazon Bedrock Claude models` |
   | Session duration | `PT8H` (8 hours — adjust to your org policy, max 12h recommended) |

6. On the **Policies** page, choose **Inline policy** and paste the following:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowBedrockModelInvocation",
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel",
        "bedrock:InvokeModelWithResponseStream",
        "bedrock:ListInferenceProfiles",
        "bedrock:GetInferenceProfile",
        "bedrock:ListFoundationModels"
      ],
      "Resource": [
        "arn:aws:bedrock:*:*:inference-profile/*",
        "arn:aws:bedrock:*:*:application-inference-profile/*",
        "arn:aws:bedrock:*:*:foundation-model/*"
      ]
    },
    {
      "Sid": "AllowMarketplaceSubscriptionViaBedrock",
      "Effect": "Allow",
      "Action": [
        "aws-marketplace:ViewSubscriptions",
        "aws-marketplace:Subscribe"
      ],
      "Resource": "*",
      "Condition": {
        "StringEquals": {
          "aws:CalledViaLast": "bedrock.amazonaws.com"
        }
      }
    }
  ]
}
```

7. Click **Next** → **Create**.

> **Why these permissions?**
> - `bedrock:InvokeModel` and `bedrock:InvokeModelWithResponseStream` — core actions Claude Code uses for every request.
> - `bedrock:ListInferenceProfiles` / `bedrock:GetInferenceProfile` — allows Claude Code to resolve inference profile ARNs and avoid extra round-trips on each new model.
> - `bedrock:ListFoundationModels` — supports model discovery at startup.
> - `aws-marketplace:Subscribe` (scoped to Bedrock) — required for initial model access registration.

### Step 3 — Create a Bedrock Access Group in Identity Center (Recommended)

Using a group as the access control boundary keeps permissions management clean: the CloudFormation stack controls *what* members can do; group membership controls *who* can do it.

1. Open **IAM Identity Center** → **Groups**.
2. Click **Create group**.
3. Set **Group name** to `claude-code-developers` (or your naming convention).
4. Optionally add a description: `Members have Claude Code Bedrock access`.
5. Click **Create group**.
6. Note the **Group ID** (UUID format) shown on the group's detail page — you will need this for the CloudFormation template parameter `BedrockGroupId` and for Step 3b.

### Step 3b — Assign the Permission Set to the Group

**Option A — via the CloudFormation template (recommended):**

Supply `BedrockGroupId` and `BedrockGroupName` when deploying the template. The stack automatically creates the `AWS::SSO::Assignment`. See the CloudFormation section below.

**Option B — manual console assignment:**

1. In IAM Identity Center, go to **AWS accounts**.
2. Select the checkbox next to your **target account** (where Bedrock is enabled).
3. Click **Assign users or groups**.
4. Switch to the **Groups** tab and select `claude-code-developers`.
5. Click **Next**.
6. Select **ClaudeCodeBedrockAccess** from the permission sets list.
7. Click **Submit**.

Wait 1–2 minutes for provisioning to complete.

### Step 3c — Add Individual Users to the Group

Now and whenever onboarding a new developer:

1. In IAM Identity Center, go to **Groups** → `claude-code-developers`.
2. Click **Add users**.
3. Search for and select the user(s) to onboard.
4. Click **Add users**.

The user gains Bedrock access within 1–2 minutes (Identity Center propagation time) — no stack redeployment required.

### Step 4 — Record Your Identity Center Values

You will need these values when configuring the Mac:

| Value | Where to Find It | Example |
|---|---|---|
| **SSO Start URL** | IAM Identity Center → Settings → AWS access portal URL | `https://d-1234567890.awsapps.com/start` |
| **SSO Region** | IAM Identity Center → Settings → Region | `us-east-1` |
| **Account ID** | AWS Console → top-right account menu | `123456789012` |
| **Permission set name** | IAM Identity Center → Permission sets | `ClaudeCodeBedrockAccess` |
| **Bedrock Region** | Where you enabled models | `us-east-1` or `us-west-2` |
| **Group ID** | IAM Identity Center → Groups → (select group) → Group ID | `a1b2c3d4-e5f6-7890-abcd-ef1234567890` |

### Step 4b — Deploy the CloudFormation Template

The `claude-code-bedrock-identity-center.yaml` template automates Steps 2 and 3b. Run this once per AWS account you want to onboard. Supply the values recorded in Step 4 plus the `BedrockGroupId` from Step 3.

```bash
aws cloudformation deploy \
  --template-file claude-code-bedrock-identity-center.yaml \
  --stack-name claude-code-bedrock-idc \
  --capabilities CAPABILITY_NAMED_IAM \
  --region us-east-1 \
  --parameter-overrides \
      IdentityCenterInstanceArn="arn:aws:sso:::instance/ssoins-XXXXXXXXXXXXXXXXX" \
      SsoStartUrl="https://d-1234567890.awsapps.com/start" \
      SsoRegion="us-east-1" \
      TargetAccountId="123456789012" \
      BedrockRegion="us-east-1" \
      BedrockGroupId="a1b2c3d4-e5f6-7890-abcd-ef1234567890" \
      BedrockGroupName="claude-code-developers"
```

**Key parameters:**

| Parameter | Required | Description |
|---|---|---|
| `IdentityCenterInstanceArn` | Yes | Instance ARN from Identity Center → Settings |
| `SsoStartUrl` | Yes | Access portal URL (`https://d-*.awsapps.com/start`) |
| `SsoRegion` | Yes | Identity Center home region |
| `TargetAccountId` | Yes | 12-digit account ID where Bedrock is invoked |
| `BedrockRegion` | Yes | Region where models are enabled |
| `BedrockGroupId` | Optional | Identity Center Group UUID — creates `AWS::SSO::Assignment` automatically |
| `BedrockGroupName` | Optional | Human-readable label for outputs and tags (not looked up in Identity Center) |
| `SessionDurationHours` | Optional | Session length 1–12 hrs (default: 8) |
| `PermissionSetName` | Optional | Permission set name (default: `ClaudeCodeBedrockAccess`) |

After deployment, retrieve the ready-to-paste config blocks:

```bash
aws cloudformation describe-stacks \
  --stack-name claude-code-bedrock-idc \
  --query 'Stacks[0].Outputs' \
  --output table
```

The `AwsConfigFileBlock` output is your `~/.aws/config` stanza. The `ClaudeCodeSettingsBlock` output is your `claude_code_settings.json`. Copy both directly to developer machines.

---

## Part 2: Mac Developer Machine Setup

### Step 5 — Install / Verify AWS CLI v2

```bash
# Verify version
aws --version
# Expected: aws-cli/2.x.x Python/3.x.x Darwin/...

# If not installed:
curl "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o "AWSCLIV2.pkg"
sudo installer -pkg AWSCLIV2.pkg -target /
```

### Step 6 — Configure the AWS SSO Profile

Add a named profile to `~/.aws/config`. You can run the interactive wizard or add it manually.

**Option A — Interactive (recommended for first-time):**

```bash
aws configure sso
# SSO session name: corp-sso
# SSO start URL: https://d-1234567890.awsapps.com/start
# SSO region: us-east-1
# (Browser opens → approve access)
# Account ID: 123456789012
# Permission set: ClaudeCodeBedrockAccess
# CLI default region: us-east-1
# CLI output format: json
# Profile name: claude-bedrock
```

**Option B — Manual (for scripted/MDM deployment):**

Add this block to `~/.aws/config`:

```ini
[profile claude-bedrock]
sso_session = corp-sso
sso_account_id = 123456789012
sso_role_name = ClaudeCodeBedrockAccess
region = us-east-1
output = json

[sso-session corp-sso]
sso_start_url = https://d-1234567890.awsapps.com/start
sso_region = us-east-1
sso_registration_scopes = sso:account:access
```

### Step 7 — Authenticate with SSO

```bash
aws sso login --profile claude-bedrock
# A browser window opens → sign in with your corporate credentials
# Terminal shows: Successfully logged into Start URL: https://d-...
```

Verify the session is valid:

```bash
aws sts get-caller-identity --profile claude-bedrock
# Should return your account ID and the AWSReservedSSO_ClaudeCodeBedrockAccess_* role ARN
```

### Step 8 — Configure Claude Code for Bedrock

**Option A — Using the built-in wizard (easiest):**

1. Open Claude Code desktop.
2. At the login prompt, choose **3rd-party platform** → **Amazon Bedrock**.
3. Select **AWS Profile** and choose `claude-bedrock` from the dropdown.
4. The wizard verifies model access and saves the configuration automatically.

**Option B — Manual environment variable configuration:**

Edit your Claude Code user settings file:

- macOS: `~/Library/Application Support/Claude/claude_code_settings.json`

```json
{
  "awsAuthRefresh": "aws sso login --profile claude-bedrock",
  "env": {
    "CLAUDE_CODE_USE_BEDROCK": "1",
    "AWS_PROFILE": "claude-bedrock",
    "AWS_REGION": "us-east-1",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "us.anthropic.claude-sonnet-4-6",
    "ANTHROPIC_DEFAULT_OPUS_MODEL": "us.anthropic.claude-opus-4-8",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "us.anthropic.claude-haiku-4-5-20251001-v1:0"
  }
}
```

> **`awsAuthRefresh` note:** This command runs automatically when Claude Code detects expired AWS credentials. It opens a browser window for re-authentication — no terminal interaction required mid-session.

### Step 9 — Verify the Connection

Inside Claude Code, run:

```
/status
```

You should see:
- **Provider:** `Amazon Bedrock`
- **Region:** `us-east-1` (or your configured region)
- **Model:** The pinned Sonnet or Opus model ID

Then send a test message. If you get a response, the setup is complete.

**Troubleshooting verification:**

```bash
# Test Bedrock access directly from the CLI
aws bedrock-runtime invoke-model \
  --profile claude-bedrock \
  --region us-east-1 \
  --model-id us.anthropic.claude-sonnet-4-6 \
  --body '{"anthropic_version":"bedrock-2023-05-31","max_tokens":50,"messages":[{"role":"user","content":"ping"}]}' \
  --cli-binary-format raw-in-base64-out \
  /tmp/bedrock-test.json && cat /tmp/bedrock-test.json
```

---

## Alternative Path: In-App AWS Sign-In (No AWS CLI Required)

For users who do not have the AWS CLI, Claude Code supports a fully in-app OAuth device-authorization flow. This requires Claude Code v1.6.0 or later.

### Configure via the Developer Menu

1. Open Claude Code desktop.
2. Click **Developer** → **Configure third-party inference**.
3. Set **Inference provider** to `Bedrock`.
4. Fill in the **SSO fields**:

| Field | Value |
|---|---|
| AWS SSO start URL | `https://d-1234567890.awsapps.com/start` |
| AWS SSO region | `us-east-1` |
| AWS SSO account ID | `123456789012` |
| AWS SSO role name | `ClaudeCodeBedrockAccess` |
| AWS region | `us-east-1` |

5. Under **Models**, add: `us.anthropic.claude-sonnet-4-6`
6. Click **Save**.

On next launch, the app shows a **Sign in with AWS** screen. Clicking it opens the IAM Identity Center portal in the browser. After authentication, credentials are stored encrypted in macOS Keychain and silently refreshed during sessions.

---

## Session Management

| Scenario | Behavior |
|---|---|
| Session is valid | Claude Code starts and works immediately |
| Session expired (Named Profile) | Claude Code detects expiry, runs `aws sso login --profile claude-bedrock` automatically, browser opens for re-auth |
| Session expired (In-App SSO) | App shows **Sign in again** prompt; one browser click re-authenticates |
| Identity Center token revoked by admin | Same as expired; user must re-authenticate |
| Forced logout | Admin deletes the user's active session in Identity Center → next request triggers re-auth |

The IAM Identity Center **access portal session duration** (in Identity Center → Settings → Authentication) controls how long users stay signed in across app restarts. Default is 8 hours; can be extended up to 90 days.

---

## Security Considerations

1. **No long-lived credentials** — all credentials are short-lived STS tokens derived from the Identity Center session.
2. **Per-user CloudTrail logs** — every `bedrock:InvokeModel` call is attributed to the specific `AWSReservedSSO_ClaudeCodeBedrockAccess_*` role ARN, which encodes the user's Identity Center username.
3. **Revocation** — remove the user's Identity Center assignment or delete their active session to immediately cut off access.
4. **Scope limitation** — the inline policy grants only the Bedrock actions required; no `*` admin access.
5. **MFA inheritance** — MFA requirements are enforced by your IdP (Okta, Entra ID, etc.) at the Identity Center portal level.
6. **Keychain storage** — on macOS, Claude Code stores the Identity Center refresh token in the system Keychain, encrypted with DPAPI equivalents.

---

## Recommended Model IDs (July 2026)

Use cross-region inference profile IDs with the `us.` prefix for automatic regional failover:

| Use Case | Model ID |
|---|---|
| Primary / complex tasks | `us.anthropic.claude-opus-4-8` |
| Balanced cost/performance | `us.anthropic.claude-sonnet-4-6` |
| Fast / background tasks | `us.anthropic.claude-haiku-4-5-20251001-v1:0` |

---

## Troubleshooting

| Symptom | Likely Cause | Fix |
|---|---|---|
| `AccessDeniedException` | Missing `bedrock:InvokeModel` in permission set, or SCP blocking Bedrock | Verify inline policy; check Org-level SCPs |
| Model shows as unavailable | Model access not enabled in Bedrock console | Go to Bedrock → Model access → enable the model in your region |
| Browser opens in a loop | Corporate VPN / TLS proxy interrupting SSO flow | Remove `awsAuthRefresh`; run `aws sso login` manually before starting Claude Code |
| `Error 002: Access not allowed` | Claude Code requesting a model ID not enabled in your account | Run `/setup-bedrock` wizard to re-detect enabled models and re-pin |
| Wrong account identity | Multiple `~/.aws/config` profiles; Claude Code using `default` | Set `AWS_PROFILE=claude-bedrock` explicitly in settings `env` block |
| Region mismatch | Model enabled in `us-east-1` but `AWS_REGION=us-west-2` | Match `AWS_REGION` to the region where you enabled model access |
| Zero token counts in `/context` | Claude Code version < v2.1.196 | Update Claude Code to v2.1.196 or later |
