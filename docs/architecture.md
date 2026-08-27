# Architecture and flow boundaries

## Design intent

The lab separates three concerns:

1. **Prevent** unsafe OCI resource changes with Security Zones and sound IAM, network, and encryption design.
2. **Assess** workload and supply-chain evidence with open-source tools.
3. **Detect and respond** through Cloud Guard, OCI Logging, Wazuh, and a human-operated remediation process.

~~~mermaid
sequenceDiagram
    participant W as OCI workload
    participant T as Open-source tools
    participant N as Normalizer
    participant O as OCI observability
    participant S as Security team

    W->>T: Local scan or telemetry collection
    T->>N: JSON finding evidence
    N->>N: Validate schema and map domain
    N->>O: Optional approved export path
    O->>S: Correlated security context
    S->>W: Approved remediation or exception
~~~

## Integration model

| Component | Input | Output | Security boundary |
| --- | --- | --- | --- |
| OpenSCAP / Lynis | Host state | Assessment findings | Run with the minimum host privilege needed. |
| Trivy | Image, filesystem, or IaC | Vulnerability and misconfiguration findings | Scan only approved artifacts. |
| Wazuh | Endpoint events | Correlated telemetry | Protect agent enrollment material outside Git. |
| Normalizer | Tool JSON | Common JSON report | Performs no network calls. |
| OCI Logging / Object Storage | Approved report export | Retained evidence | Use least-privilege IAM and retention rules. |
| Cloud Guard | OCI resource and activity signals | Problems and recommendations | Tune recipes and responders through change control. |

## Deployment note

The example intentionally stops at a local report. A production integration should use a workload identity or an OCI dynamic group with least-privilege policies, a managed secret store, encrypted transport, classification-aware retention, and an approved change path for remediation.
