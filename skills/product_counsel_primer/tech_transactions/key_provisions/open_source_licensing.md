---
name: open-source-licensing
description: Open Source Licensing
tags:
  - compliance
  - licensing
  - open-source
version: '1.0'
confidence_level: MEDIUM
category: key_provisions
validated_by: Synthetic Generation
validated_date: '2024-10-20'
skill_tier: foundational
mentoring_priority: 2
validation_type: synthetic
source_type: expert_judgment
---

# Open Source Licensing

```yaml
skill_id: open_source_licensing
domain: intellectual_property
sub_domains: [oss_compliance, copyleft, permissive_licenses, gpl, mit, apache]
transaction_types: [software_licensing, technology_licensing, strategic_partnerships]
confidence: 0.70
validation_status: synthetic_quick
requires: [ip_law, software_licensing]
complements: [ip_ownership_assignment, warranties_representations]
skill_tier: foundational
mentoring_priority: 2
```

## Overview

Open source software (OSS) licenses govern use, modification, and distribution of publicly available source code. Key considerations:
- **License compatibility**: Can different OSS licenses be combined?
- **Copyleft obligations**: Must derivative works be open sourced?
- **Commercial use restrictions**: Can OSS be used in commercial products?
- **Attribution requirements**: Must original authors be credited?
- **Patent grants and retaliation**: What patent rights are granted/terminated?

**Critical for**: Any software development using third-party libraries, frameworks, or components.

---

## Major License Categories

### Permissive Licenses (Non-Copyleft)

**MIT License** - Most permissive, minimal restrictions
```
Key terms:
- ✅ Use, modify, distribute (including proprietary)
- ✅ Sublicense and sell
- ✅ No disclosure of source required
- ⚠️ Must include original license/copyright notice
- ⚠️ No warranty, no liability
```

**Apache 2.0** - Permissive with patent grant
```
Key terms:
- ✅ Use, modify, distribute (including proprietary)
- ✅ Express patent grant from contributors
- ⚠️ Must include NOTICE file, state changes
- ⚠️ Patent retaliation (patent grant terminates if you sue)
- ⚠️ Cannot use trademarks without permission
```

**BSD Licenses** (2-Clause, 3-Clause)
```
Similar to MIT with additional clauses:
- 3-Clause BSD: Cannot use project name for endorsement
- 2-Clause BSD: Very similar to MIT
```

### Copyleft Licenses (Reciprocal)

**GPL v2 / GPL v3** - Strong copyleft
```
Key terms:
- ✅ Use, modify, distribute
- ⚠️ Derivative works MUST be GPL-licensed
- ⚠️ Must provide source code to recipients
- ⚠️ "Viral" - proprietary code linked with GPL becomes GPL
- ⚠️ GPLv3 adds patent grant and anti-tivoization

CRITICAL: Linking GPL code into proprietary software triggers copyleft
```

**LGPL** (Lesser GPL) - Weak copyleft
```
Key terms:
- ✅ Can link LGPL libraries into proprietary applications
- ⚠️ Modifications to LGPL library itself must remain LGPL
- ⚠️ Must allow users to replace LGPL library (dynamic linking preferred)
```

**AGPL** (Affero GPL) - Network copyleft
```
Key terms:
- Same as GPL BUT
- ⚠️ SaaS/web services must provide source to users
- ⚠️ "Network use" triggers disclosure (not just distribution)
- ⚠️ Very restrictive for cloud/SaaS applications
```

### Weak Copyleft / File-Level Licenses

**Mozilla Public License (MPL) 2.0**
```
Key terms:
- ✅ File-level copyleft (not full program)
- ✅ Can combine with proprietary code in separate files
- ⚠️ Modifications to MPL files must stay MPL
- ⚠️ Patent grant included
```

**Eclipse Public License (EPL)**
```
Similar to MPL - module-level copyleft
Common in Java ecosystem
```

---

## Critical Compliance Issues

### GPL Contamination Risk

**The Risk**: Linking GPL code into proprietary software makes entire work GPL-derivative
```
Scenario: Company uses GPL library in proprietary SaaS application
Result: Entire application may need to be open sourced under GPL
```

**Safe Practices**:
- Inventory all OSS components (use tools: Black Duck, Snyk, FOSSA)
- Avoid GPL in proprietary products (use LGPL or permissive instead)
- If GPL required: Use separate process, communicate via network/IPC
- Get legal review before using any copyleft license

### Patent Considerations

**Apache 2.0 Patent Grant**:
```
✅ Contributors grant patent license for their contributions
⚠️ Patent retaliation: If you sue Apache project for patent infringement,
   your patent license terminates
```

**GPL v3 Patent Provisions**:
```
✅ Implicit patent grant for GPL contributions
✅ Anti-Tivoization: Cannot use hardware restrictions to prevent
   modification of GPL software
```

**MIT/BSD - No Patent Grant**:
```
⚠️ No express patent license
⚠️ May have implied license, but legally uncertain
```

### Attribution Requirements

**All OSS Licenses Require**:
```
- Include original copyright notices
- Include copy of license text
- Preserve attribution in documentation
```

**Common Compliance Method**:
```
Create "Third-Party Notices" or "Open Source Licenses" file
List all OSS components with:
- Component name and version
- License type
- Copyright notice
- Link to license text
```

---

## Contractual OSS Provisions

### Vendor Representations

**Standard Vendor Representation**:
```
"Vendor represents that Software does not include any open source software
licensed under GPL, AGPL, or other copyleft license that would require
Customer's proprietary software to be open sourced or disclosed."
```

**More Detailed**:
```
"Vendor represents that:
(a) Software includes only OSS under permissive licenses (MIT, Apache 2.0, BSD)
(b) Complete list of OSS components provided in Exhibit A
(c) Software does not link to or incorporate GPL/AGPL code
(d) Vendor maintains OSS compliance program and conducts license scans"
```

### Customer Obligations (When Receiving OSS)

```
"Customer acknowledges Software includes OSS components listed in Exhibit B.
Customer shall:
(a) Comply with all OSS license obligations
(b) Include required attribution notices in distributions
(c) Not remove copyright notices or license files
(d) If redistributing modified versions, comply with each license's
    requirements (including source disclosure for copyleft licenses)"
```

### Indemnification Carve-Out

**Issue**: Vendor typically won't indemnify for OSS IP claims

```
"Vendor's IP indemnification (Section X) does NOT apply to:
(a) Open source software components listed in Exhibit C
(b) Customer's modification of OSS components
(c) Customer's failure to comply with OSS license requirements"
```

**Rationale**: Vendor doesn't control OSS, so can't indemnify. Customer accepts OSS license terms directly from authors.

---

## Due Diligence Checklist

When reviewing technology involving OSS:

### Vendor Due Diligence
- [ ] Request complete OSS inventory (bill of materials)
- [ ] Identify all GPL/AGPL/copyleft components
- [ ] Verify OSS compliance program exists
- [ ] Review OSS scanning tools/processes used
- [ ] Assess contamination risk (proprietary code linked with GPL?)

### License Compatibility
- [ ] Can different OSS licenses in product coexist?
- [ ] Any GPL + proprietary code linkage?
- [ ] Any AGPL in SaaS application (triggers network copyleft)?
- [ ] Patent grant conflicts?

### Commercial Use
- [ ] Are there "non-commercial use only" restrictions?
- [ ] Any Creative Commons "NC" (non-commercial) licenses?
- [ ] Any "research use only" restrictions?

### Compliance Obligations
- [ ] What attribution is required?
- [ ] Must source code be disclosed (copyleft)?
- [ ] Must changes be documented?
- [ ] Are there trademark restrictions?

---

## Industry Best Practices

**OSS Compliance Program Should Include**:
1. **Automated scanning**: Integrate into CI/CD pipeline (Snyk, Black Duck, WhiteSource)
2. **Approval process**: Legal review before adopting new OSS dependency
3. **Bill of Materials**: Maintain current list of all OSS components
4. **Training**: Developer training on OSS compliance
5. **Vendor management**: Require vendors to disclose OSS usage

**Red Flags**:
- No OSS inventory/bill of materials
- GPL code linked into proprietary product
- AGPL in SaaS/cloud application
- "We'll provide OSS list later" (means they don't know)
- Vendor refuses OSS representations

---

## Common Pitfalls

1. **"It's free so we can use it however"** - FALSE. OSS has license obligations.
2. **"MIT license has no restrictions"** - FALSE. Requires attribution, disclaims warranty.
3. **"GPL only applies if we distribute"** - MOSTLY FALSE. AGPL applies to SaaS/network use.
4. **"We modified OSS so it's ours now"** - FALSE. Derivative works subject to original license.
5. **"Our legal team approved GPL use"** - Verify they understood copyleft implications.

---

## References and Validation

**CAUTION**: This is a quick-reference Skills file and has not been validated by legal experts.

**Confidence Level**: 0.6 (Synthetic Quick Version - Not Expert-Validated)

**For Expert Review**:
Kevin Keller should validate:
- [ ] License compatibility matrices
- [ ] GPL contamination triggers (linking, IPC, separate processes)
- [ ] AGPL network copyleft scope
- [ ] Patent grant and retaliation provisions
- [ ] Indemnification carve-out standard language
- [ ] Due diligence best practices

**Recommended Backfill**: Expand to include specific license compatibility matrix, case law examples, compliance tool comparisons, industry-specific considerations.

---

## Cross-References

**Related Key Provisions** (tech_transactions):
- `ip_ownership_assignment.md` - OSS affecting IP ownership/contamination
- `indemnification.md` - OSS carve-outs from IP indemnification
- `warranties_representations.md` - OSS compliance representations
- `confidentiality_nda.md` - OSS contribution vs. proprietary code

**Contract Intelligence Skills** (from 4,900+ real contracts):
- `software-license-expected-clauses.md` - OSS provisions in commercial licenses
- `ip-ownership-taxonomy.md` - IP ownership and OSS considerations
- `indemnification-taxonomy.md` - OSS carve-outs in indemnification

**Cognitive Patterns** (apply to OSS analysis):
- `S3` - Multi-domain synthesis (legal, technical, business OSS implications)
- `S4` - Systematic risk assessment (copyleft contamination risk)
- `S9` - Hierarchical due diligence (OSS audit priority by risk)
- `BI3` - Context-aware risk (OSS acceptable for internal vs. product?)
