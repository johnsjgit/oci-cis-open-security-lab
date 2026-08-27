# OCI CIS Open Security Lab

A safe, portfolio-focused reference for connecting **open-source security evidence** to **Oracle Cloud Infrastructure (OCI)** controls. It models a practical workflow without requiring a live tenancy, API key, OCID, or production data.

## Purpose

This project shows how a cloud security architect can combine host hardening, vulnerability evidence, and centralized monitoring with OCI-native posture management.

It is **CIS-inspired**, not an implementation or redistribution of CIS Benchmarks. The repository only uses high-level control references; always consult the current CIS publications and the relevant tool documentation for authoritative requirements.

## Architecture flow

~~~mermaid
flowchart LR
    A[OCI tenancy and compartments] --> B[Compute or OKE workload]
    Z[OCI Security Zones] -. preventive guardrails .-> A
    B --> C1[OpenSCAP - baseline checks]
    B --> C2[Lynis - host audit]
    B --> C3[Trivy - image and IaC scan]
    B --> C4[Wazuh agent - security telemetry]
    C1 --> D[Normalized finding schema]
    C2 --> D
    C3 --> D
    C4 --> D
    D --> E[CIS-inspired control mapping]
    E --> F[OCI Logging and Object Storage]
    E --> G[OCI Cloud Guard correlation]
    E --> H[Security operations dashboard]
~~~

See [the detailed architecture](docs/architecture.md) for responsibilities and boundaries.

## What the repository demonstrates

- A private-by-default architecture around OCI workloads.
- Evidence collection through open-source tools, not embedded credentials.
- A small Python CLI that converts sample findings to a common JSON report.
- A clear separation between preventive OCI controls, open-source assessment, and human-led remediation.
- Mapping fields that help a security team prioritize findings; they are not a certification claim.

## Quick start

~~~powershell
python src/normalize_findings.py examples/sample-findings.json
~~~

The command reads local example data only. It does not call OCI, create resources, or send telemetry.

## Project structure

~~~text
docs/architecture.md             Detailed flow and integration boundaries
examples/sample-findings.json    Safe fictional security findings
src/normalize_findings.py        Standard-library report normalizer
~~~

## Tool and service roles

| Layer | Example responsibility |
| --- | --- |
| OpenSCAP / Lynis | Evaluate host configuration and hardening evidence. |
| Trivy | Report container, dependency, and IaC risks. |
| Wazuh | Collect and correlate endpoint security telemetry. |
| OCI Cloud Guard | Assess OCI configuration and activity risks. |
| OCI Security Zones | Prevent selected unsafe OCI resource operations. |
| OCI Logging / Object Storage | Retain operational evidence according to the organization’s policy. |

## Security principles

1. No secrets in source control; runtime identities and secret managers belong outside the repository.
2. No automatic remediation is enabled by default; a team must approve any response workflow.
3. Sample findings use fictional assets only.
4. Control mappings are traceability aids, not proof of compliance or a replacement for an audit.

## Roadmap

- Add OCI CLI collection adapters that read from a least-privilege profile.
- Add a Wazuh decoder example and a dashboard schema.
- Add Terraform examples that contain no tenancy-specific values.
- Add a GitHub Actions workflow that tests the normalizer against safe fixtures.

## License

MIT.
