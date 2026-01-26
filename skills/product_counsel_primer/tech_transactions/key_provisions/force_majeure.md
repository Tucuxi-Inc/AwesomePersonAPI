---
name: force-majeure
description: Force Majeure
tags:
  - events
  - excused-performance
  - force-majeure
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

# Force Majeure

```yaml
skill_id: force_majeure
domain: contract_provisions
sub_domains: [impossibility, impracticability, excuse_of_performance, acts_of_god, pandemic]
transaction_types: [all_transaction_types]
confidence: 0.70
validation_status: synthetic
requires: [contract_law, termination_provisions]
complements: [service_levels, liability_limitations, warranties_representations]
skill_tier: foundational
mentoring_priority: 2
```

## Overview

Force majeure clauses excuse contractual performance when extraordinary events beyond a party's control make performance impossible, illegal, or impracticable. They address:
- **Qualifying events** (natural disasters, war, government action, strikes, pandemics)
- **Notice requirements** (timing and content)
- **Excuse of performance** (suspension vs. discharge)
- **Mitigation obligations** (reasonable efforts to overcome)
- **Termination rights** (if event persists too long)

**Critical for**: All technology transactions, especially those with:
- Time-critical performance obligations
- International components (geopolitical risks)
- Infrastructure dependencies (utilities, internet, cloud providers)
- Labor-intensive services (strikes, workforce availability)

**Why It Matters**: Force majeure allocates risk of extraordinary, unforeseeable events. Without it, parties may be liable for breach even when performance is genuinely impossible. Post-COVID-19, force majeure clauses receive heightened scrutiny.

---

## Core Principles

### What is Force Majeure?

**Force majeure** (French: "superior force") excuses non-performance due to events:
1. **Beyond reasonable control** of the affected party
2. **Unforeseeable** at time of contract formation
3. **Unavoidable** despite reasonable precautions
4. **Materially prevent** contractual performance

**Not a Default Rule**: Unlike common law doctrines of impossibility or frustration of purpose, force majeure is purely contractual. If the contract lacks a force majeure clause, parties must rely on common law doctrines (which are narrower).

### Common Law Background

**Impossibility** (Restatement (Second) of Contracts § 261):
- Performance impossible due to unforeseen event
- Event must make performance objectively impossible (not just more difficult or expensive)
- Narrow application: destruction of subject matter, death/incapacity, supervening illegality

**Impracticability** (UCC § 2-615):
- Performance impracticable due to unforeseen event
- Event occurrence was a "basic assumption" of the contract
- Non-occurrence of event was implicit condition
- Broader than impossibility but still narrow

**Frustration of Purpose** (Restatement § 265):
- Principal purpose of contract substantially frustrated
- Non-occurrence was basic assumption
- Very rare application

**Key Limitation**: Common law doctrines require total or near-total impossibility. Force majeure clauses can provide relief for lesser impediments if properly drafted.

---

## Standard Force Majeure Provision

### Basic Structure

```
"FORCE MAJEURE

Neither party shall be liable for any failure or delay in performance
under this Agreement (except for payment obligations) to the extent such
failure or delay is caused by a Force Majeure Event.

'Force Majeure Event' means an event beyond the reasonable control of
the affected party, including but not limited to:

(a) Acts of God (earthquake, flood, fire, storm, hurricane)
(b) War, invasion, terrorism, civil unrest, riot
(c) Government action (embargo, regulation, order)
(d) Labor disputes (strike, lockout) affecting third parties
(e) Pandemic, epidemic, quarantine
(f) Utility failure (power, internet, telecommunications)
(g) Failure of third-party service providers or suppliers

The affected party must:
1. Provide prompt written notice of the Force Majeure Event
2. Use commercially reasonable efforts to mitigate effects
3. Resume performance as soon as reasonably possible

If a Force Majeure Event prevents performance for more than [30/60/90]
days, either party may terminate this Agreement upon written notice."
```

**Key Components:**
- **Scope**: What obligations are excused (typically all except payment)
- **Definition**: What qualifies as force majeure
- **Notice**: Requirements for claiming force majeure
- **Mitigation**: Obligations to minimize impact
- **Termination**: How long before parties can terminate

---

## Force Majeure Event Definitions

### Specific vs. General Language

**Specific Enumeration** (Vendor-Friendly):
```
"Force Majeure Event means only the following:
(a) earthquake, flood, or fire;
(b) war or terrorism;
(c) governmental order or regulation"
```
- **Pros**: Clarity, predictability
- **Cons**: Omitted events not covered (pandemic excluded unless listed)

**General Catch-All** (Balanced):
```
"Force Majeure Event means events beyond a party's reasonable control,
including but not limited to acts of God, war, terrorism, government
action, labor disputes, pandemic, utility failure, and internet
backbone failure."
```
- **Pros**: Flexibility, covers unforeseen event types
- **Cons**: Potential disputes about what qualifies

**Overly Broad** (Customer-Unfriendly):
```
"Force Majeure Event means any event beyond Vendor's control that
prevents or delays performance."
```
- **Problem**: Could excuse normal business risks (supplier delays, financial difficulties)
- **Fix**: Add specificity and foreseeability requirement

### Common Force Majeure Events

#### Acts of God (Natural Disasters)
```
"Acts of God including earthquake, flood, fire, storm, hurricane,
tornado, tsunami, volcanic eruption, or other extreme natural event"
```
**Technology Context:**
- Data center flooding (Hurricane Katrina, Sandy)
- Earthquake affecting cloud infrastructure (Japan 2011)
- Wildfire causing power shutdowns (California)

**Limitation**: Must be truly extraordinary. Normal weather (snow in Minnesota) not force majeure.

#### War and Terrorism
```
"War (declared or undeclared), invasion, armed conflict, terrorism,
civil unrest, riot, insurrection, revolution, coup d'état"
```
**Technology Context:**
- Cyber warfare disrupting internet infrastructure
- Geopolitical conflicts affecting international services (Russia-Ukraine affecting European data centers)
- Terrorism affecting physical infrastructure

#### Government Action
```
"Government or regulatory action, including laws, orders, regulations,
embargoes, sanctions, import/export restrictions, quarantines, or
requests from law enforcement or national security agencies"
```
**Technology Context:**
- GDPR compliance preventing data transfers
- Export control regulations blocking software delivery
- Government internet shutdowns (India, Iran)
- National security blocking technology acquisitions
- COVID-19 lockdown orders

**Key Distinction**:
- **Specific to this contract**: New regulation makes this specific performance illegal → Force majeure
- **General regulatory change**: New data privacy law requires expensive compliance → NOT force majeure (parties bear their own regulatory compliance costs)

#### Labor Disputes
```
"Labor disputes, including strikes, lockouts, or other industrial
disturbances, affecting the party's workforce or essential
third-party suppliers"
```

**Key Limitation - Own Employees**:

**Vendor-Friendly**: "Labor disputes including strikes, lockouts, or slowdowns"
- Includes vendor's own employees
- Vendor not liable if workforce strikes

**Customer-Friendly**: "Labor disputes affecting third parties, but excluding disputes with the party's own employees"
- Vendor bears risk of managing own workforce
- Only third-party labor disputes (e.g., shipping, utilities) qualify

**Balanced**: "General labor disputes or strikes affecting multiple industries, but excluding disputes solely affecting the party's own workforce unless part of industry-wide action"

#### Pandemics and Epidemics
```
"Pandemic, epidemic, widespread disease outbreak, public health
emergency, or quarantine declared by governmental authority or the
World Health Organization"
```

**Post-COVID-19 Evolution**:

**Pre-COVID Standard**: Often omitted or buried in general language

**Post-COVID Standard**: Explicitly addressed with specific provisions

**Carve-Outs for Pandemics**:
```
"Force Majeure Event includes pandemics, provided that:
(a) Financial impacts alone (loss of revenue, increased costs) do
    not constitute force majeure
(b) Party must show pandemic directly prevents performance (e.g.,
    government lockdown closing facilities, workforce unavailability
    due to illness exceeding 30%)
(c) If performance is possible through remote work, work-from-home
    arrangements, or reasonable alternative methods, pandemic does
    not excuse performance"
```

**Pandemic-Specific Provisions** (See "Post-COVID Considerations" below)

#### Utility and Infrastructure Failures
```
"Failure of utilities (electricity, water, gas, heating, cooling),
telecommunications, internet service providers, or internet backbone
infrastructure, where such failure is beyond the party's control"
```

**Key Limitation - Own Infrastructure**:
```
Customer-Friendly: "Utility failures beyond Vendor's control, excluding
failures of Vendor's own equipment, systems, or infrastructure"

Explanation: Vendor's server crash ≠ force majeure
             Regional power outage → force majeure
```

**Cloud Service Dependencies**:
```
"Failure or significant disruption of third-party cloud infrastructure
providers (AWS, Azure, Google Cloud) that materially prevents performance
and affects multiple customers"
```

**Important**: This is heavily negotiated. Customers argue vendor chose cloud provider (should bear risk). Vendors argue AWS outages are force majeure events.

#### Cyber Attacks
```
"Denial-of-service attacks, malware, ransomware, or other cyber attacks
that materially disrupt performance, excluding attacks reasonably
preventable through industry-standard security practices"
```

**Key Issue**: When is cyber attack force majeure vs. vendor's security failure?

**Balanced Approach**:
```
"Cyber attacks qualify as force majeure if:
(a) Attack is unprecedented in scale or sophistication
(b) Vendor maintained industry-standard security practices
(c) Attack affects multiple industry participants (not targeting
    Vendor specifically due to Vendor's security weaknesses)"
```

**Example**:
- ✅ Force Majeure: Stuxnet-level sophisticated nation-state attack
- ❌ NOT Force Majeure: Phishing attack due to lack of employee training

### Exclusions from Force Majeure

**Standard Exclusions**:
```
"Force Majeure Event does NOT include:

(a) Economic conditions (financial hardship, market changes, cost increases)
(b) Failure to obtain financing or credit
(c) Supplier or subcontractor failures (unless supplier itself affected by
    force majeure event)
(d) Breakdown of party's own equipment, systems, or infrastructure
(e) Labor disputes with party's own employees (unless industry-wide)
(f) Foreseeable events (e.g., known hurricane season in Florida)
(g) Events caused by party's negligence or willful misconduct
(h) Events that merely make performance more expensive or less profitable"
```

**Critical Principle**: Force majeure excuses extraordinary events, not normal business risks.

---

## Notice Requirements

### Standard Notice Provision

```
"The party claiming force majeure (the 'Affected Party') must:

1. Provide written notice to the other party within [3/5/10] business
   days after the Force Majeure Event begins

2. The notice must include:
   (a) Description of the Force Majeure Event
   (b) Expected duration and impact on performance
   (c) Obligations affected
   (d) Steps being taken to mitigate impact

3. Provide regular updates (at least every [7/14/30] days) on status
   and anticipated resumption of performance

4. Provide written notice within [3/5] business days after Force
   Majeure Event ends and performance can resume"
```

**Key Timing Issues**:

**Short Notice Period** (Customer-Friendly):
```
"Notice within 3 business days of event"
- Ensures customer learns quickly
- May be unrealistic for sudden catastrophic events
```

**Longer Notice Period** (Vendor-Friendly):
```
"Notice within 15 business days of event"
- More realistic for assessing impact
- Customer left in dark longer
```

**Balanced**: 5-10 business days for initial notice, with ongoing updates

**Consequence of Late Notice**:
```
"Failure to provide timely notice shall waive the Affected Party's
right to claim force majeure for the period before notice was given."

OR (harsher):

"Failure to provide notice within the required timeframe shall
constitute a waiver of force majeure relief entirely."
```

---

## Scope of Excuse

### What Obligations Are Excused?

**All Non-Payment Obligations** (Vendor-Friendly):
```
"Force Majeure Event excuses all performance obligations except
payment obligations."
```

**Partial Excuse** (Customer-Friendly):
```
"Force Majeure Event excuses only those specific obligations directly
prevented by the event. Obligations not directly affected remain in
full force and effect."
```

**Example**:
- Scenario: Hurricane damages vendor's East Coast data center
- Vendor-Friendly: All performance excused (even if West Coast systems operational)
- Customer-Friendly: Only East Coast services excused; West Coast services must continue

**Balanced Approach**:
```
"Force Majeure Event excuses performance to the extent, and only for
the duration, that the event directly prevents performance. Partially
affected obligations shall be performed to the extent reasonably
practicable."
```

### Payment Obligations

**Standard Rule**: Force majeure does NOT excuse payment obligations.

```
"Payment obligations are not subject to force majeure and shall
continue regardless of Force Majeure Events."
```

**Rationale**: Money is fungible; financial hardship is not force majeure.

**Exception - Services Not Rendered**:
```
"Customer's obligation to pay fees is suspended during any period when
Vendor cannot provide the Services due to a Force Majeure Event,
provided that subscription fees shall continue for periods when Services
are partially available and Customer receives material benefit."
```

**Practical Application**:
- SaaS unavailable due to force majeure → Customer doesn't pay for downtime period
- Usage-based pricing → Customer only pays for actual usage (automatically adjusted)
- Annual prepaid subscription → May negotiate credit for extended outages

---

## Mitigation Obligations

### Standard Mitigation Provision

```
"The Affected Party shall:

1. Use commercially reasonable efforts to mitigate the effects of the
   Force Majeure Event and resume performance as soon as practicable

2. Develop and implement a remediation plan, including:
   (a) Interim workarounds or alternative performance methods
   (b) Timeline for full resumption of performance
   (c) Resource allocation to overcome the event

3. Provide regular status updates to the non-affected party

The Affected Party's failure to use reasonable mitigation efforts shall
disqualify the party from force majeure relief."
```

**What "Commercially Reasonable Efforts" Means**:

**Not Required**:
- Extraordinary expense (e.g., vendor doesn't have to rebuild entire data center at 10x cost)
- Illegal actions
- Actions that endanger safety

**Required**:
- Reasonable alternative methods (e.g., shift to backup data center)
- Communication with customers
- Reallocating resources
- Working with suppliers to find alternatives

**Technology-Specific Mitigation**:
```
Cloud Service Outage Mitigation:
"If primary cloud provider (AWS US-East-1) experiences Force Majeure
Event, Vendor shall use commercially reasonable efforts to:
(a) Failover to backup region (US-West-2) within 4 hours
(b) Activate disaster recovery procedures
(c) Communicate status and timeline to Customer"
```

### Mitigation Costs

**Who Bears Mitigation Costs?**

**Vendor Bears Cost** (Standard):
```
"Affected Party shall bear all costs of mitigation efforts."
```

**Shared Cost** (Sometimes Negotiated):
```
"If Customer requests mitigation measures beyond commercially reasonable
efforts (e.g., emergency infrastructure rebuild), Customer shall reimburse
Vendor's reasonable costs upon mutual agreement."
```

---

## Duration and Termination

### Termination Rights

**Standard Termination Provision**:
```
"If a Force Majeure Event continues for more than [30/60/90] consecutive
days, either party may terminate this Agreement upon [10/30] days'
written notice to the other party.

Upon such termination:
(a) Customer shall pay for services received through termination date
(b) Vendor shall refund any prepaid fees for services not rendered
(c) Both parties shall cooperate in orderly transition
(d) Neither party shall have liability for termination under this section"
```

**Key Variables**:

**Termination Threshold** (30/60/90 days):
- **30 days** (Customer-Friendly): Quick exit if vendor can't perform
- **90 days** (Vendor-Friendly): More time to remediate
- **60 days** (Balanced): Standard in most commercial agreements

**Notice Period** (10/30 days):
- **Immediate termination**: Rarely seen (harsh)
- **30 days notice**: Allows planning, orderly transition
- **Notice after cure period**: Additional time beyond force majeure period

**Who Can Terminate?**

**Either Party** (Standard):
```
"Either party may terminate upon 90 days of continued force majeure"
```
- Fair to both sides
- Non-affected party can exit if service unavailable too long
- Affected party can exit if cannot perform

**Non-Affected Party Only** (Customer-Friendly):
```
"If Vendor cannot perform due to force majeure for >60 days, Customer
may terminate. Vendor may not terminate due to Customer force majeure
unless Customer's breach is material."
```
- Protects customer's right to exit
- Vendor committed to providing service despite customer issues

### Suspension vs. Termination

**Automatic Suspension** (Common):
```
"Performance obligations are automatically suspended during Force Majeure
Event. Upon event conclusion, obligations resume automatically without
need for notice or cure period (except for payment obligations which
continue)."
```

**Partial Suspension**:
```
"If Force Majeure Event affects only certain Services or geographic
regions, suspension applies only to affected Services/regions. All
unaffected obligations continue in full force."
```

**Extension of Term**:
```
"If Force Majeure Event suspends performance for >30 days, the Term
shall be extended by the period of suspension, unless either party
elects to terminate under Section [X]."
```
- Ensures customer receives full contracted term
- Vendor doesn't lose contract duration due to force majeure

---

## Integration with Other Provisions

### Force Majeure and SLAs

**Standard Approach**: Force majeure events excluded from SLA calculations

```
"Service Level Agreement Exclusion:
Downtime caused by Force Majeure Events shall be excluded from Monthly
Uptime calculations under the SLA, provided Vendor:
(a) Provides notice of force majeure within 24 hours
(b) Uses commercially reasonable efforts to restore service
(c) Provides regular status updates"
```

**Key Issue**: What if vendor's "force majeure" is actually poor planning?

**Customer-Protective Limitation**:
```
"Force Majeure Events excuse SLA obligations only if:
(a) Event is genuinely unforeseeable and beyond vendor control
(b) Vendor maintained industry-standard redundancy and disaster recovery
(c) Vendor's architectural choices did not materially contribute to impact

Example: Regional AWS outage may qualify, but only if Vendor implemented
multi-region redundancy per industry standards for critical services."
```

### Force Majeure and Liability

**Does Force Majeure Limit Liability?**

**Standard**: Force majeure excuses performance (no breach), thus no liability

```
"No Liability During Force Majeure:
Neither party shall be liable for any failure or delay in performance
caused by Force Majeure Event, including any direct, indirect,
consequential, or incidental damages."
```

**Customer-Protective Limitation**:
```
"Force Majeure and Liability:
(a) Force majeure excuses performance and eliminates breach liability
(b) However, Vendor remains liable for:
    - Failure to provide required notice
    - Failure to use reasonable mitigation efforts
    - Damages caused by Vendor's negligence or willful misconduct
    - Payment obligations and indemnification obligations
(c) Nothing in this section limits Vendor's data protection,
    confidentiality, or IP indemnification obligations"
```

### Force Majeure and Warranties

**Effect on Warranties**:

**Vendor Position**: Force majeure suspends all warranties
```
"All warranties suspended during Force Majeure Event"
```

**Customer Position**: Force majeure excuses performance, not warranties
```
"Force Majeure Event excuses performance timelines but does not waive
warranties. Upon resumption of performance, all warranties apply."
```

**Balanced**:
```
"Warranties are suspended during Force Majeure Event but resume
immediately upon event conclusion. Vendor shall use commercially
reasonable efforts to ensure resumed performance meets all warranty
standards."
```

---

## Post-COVID-19 Considerations

### Pandemic-Specific Provisions

**Explicit Pandemic Language** (Now Standard):
```
"PANDEMIC AND PUBLIC HEALTH EMERGENCIES

(a) Qualifying Events: Pandemic, epidemic, or public health emergency
    declared by WHO, CDC, or applicable government authority qualifies
    as Force Majeure Event.

(b) Financial Impacts Excluded: Economic impacts alone (reduced revenue,
    increased costs, supply chain cost increases) do not constitute
    force majeure.

(c) Remote Work Capability: If performance is reasonably possible through
    remote work, work-from-home arrangements, or digital alternatives,
    pandemic does not excuse performance unless government orders
    specifically prohibit such alternatives.

(d) Workforce Availability Threshold: Workforce illness/unavailability
    must exceed [30%] of essential personnel for [14] consecutive days
    to qualify as force majeure.

(e) Supply Chain Disruptions: Pandemic-related supplier delays qualify
    as force majeure only if:
    - Supplier is directly affected by government lockdown orders
    - No alternative suppliers available despite reasonable efforts
    - Delay exceeds [60] days

(f) Government Orders: Lockdowns, shelter-in-place, quarantine, or
    business closure orders qualify as force majeure to the extent they
    directly prevent performance."
```

### COVID-19 Lessons

**What COVID-19 Taught About Force Majeure**:

1. **Specificity Matters**: General language ("acts of God") ambiguous for pandemics

2. **Financial Hardship ≠ Force Majeure**: Economic impacts don't excuse performance
   - Revenue loss from market downturn ≠ force majeure
   - Increased costs (PPE, remote work setup) ≠ force majeure
   - Must show pandemic directly prevented performance

3. **Remote Work Changes Analysis**: If service can be provided remotely, pandemic may not excuse performance

4. **Duration Uncertainty**: COVID-19 lasted years; termination provisions written for weeks/months

5. **Geographic Specificity**: Pandemic affected different regions at different times; needed geographic precision

**Post-COVID Negotiation Points**:

**Customer-Friendly**:
```
"Pandemic constitutes force majeure only if government orders
specifically prohibit the affected party's business operations and
performance cannot reasonably be provided remotely or through
alternative means."
```

**Vendor-Friendly**:
```
"Any pandemic declared by WHO or applicable government authority
qualifies as force majeure, excusing performance to the extent
reasonably affected."
```

**Balanced**:
```
"Pandemic qualifies as force majeure if it directly prevents
performance through government closure orders, workforce unavailability
>30%, or supply chain failure, but does not excuse performance
reasonably achievable through remote work or alternative methods."
```

### Foreseeability After COVID-19

**Key Issue**: Is the next pandemic "foreseeable" now?

**Arguments**:

**Customer Position**: "COVID-19 happened. Pandemics are now foreseeable. Vendors should build resilience (remote work capability, geographic redundancy)."

**Vendor Position**: "COVID-19 scale was unprecedented. Future pandemics of similar magnitude remain unforeseeable force majeure events."

**Emerging Standard**:
```
"Pandemic Force Majeure - Foreseeability:
The parties acknowledge the COVID-19 pandemic occurred. Future pandemics
of similar or greater magnitude and impact qualify as force majeure
events, provided that:

(a) Vendor maintains reasonable business continuity measures including:
    - Remote work capability for ≥80% of workforce
    - Geographic redundancy for critical infrastructure
    - Documented pandemic response plan

(b) Pandemic must meet WHO definition of 'Public Health Emergency of
    International Concern' (PHEIC) or result in government-mandated
    business closures affecting Vendor's operations

(c) Financial impacts alone (cost increases, revenue decline) do not
    constitute force majeure absent direct operational prevention"
```

---

## Industry-Specific Considerations

### Technology/SaaS

**Cloud Infrastructure Dependencies**:
```
"Force Majeure - Cloud Provider Failures:
Failures of third-party cloud infrastructure providers (AWS, Azure,
Google Cloud) qualify as force majeure events if:
(a) Outage affects multiple availability zones or regions
(b) Cloud provider publicly acknowledges outage as force majeure event
(c) Vendor implemented industry-standard multi-region architecture
(d) Outage duration exceeds [4] hours

Vendor's failure to implement reasonable redundancy and failover
capabilities shall disqualify cloud provider outages from force majeure."
```

**Cyber Attacks**:
```
"Cyber attacks qualify as force majeure if:
- Attack is nation-state or sophisticated criminal organization
- Vendor maintained SOC 2 Type II or ISO 27001 security standards
- Attack affects multiple industry participants
- Attack is unprecedented in scale per industry standards"
```

### International Transactions

**Geopolitical Events**:
```
"Force Majeure - International Transactions:
Events including:
(a) Trade embargoes or sanctions affecting either party's country
(b) Import/export license denials or revocations
(c) Currency controls preventing payment transfers
(d) War, invasion, or armed conflict in either party's jurisdiction
(e) Expropriation or nationalization of either party's assets
(f) Inability to obtain foreign exchange for payments"
```

**Choice of Law and Force Majeure**:
- **Common Law** (US, UK): Force majeure is purely contractual; no default doctrine
- **Civil Law** (France, Germany): May have statutory force majeure provisions
- **International Contracts**: Specify governing law and whether statutory provisions apply

### Hardware/Manufacturing

**Supply Chain Disruptions**:
```
"Supplier/Manufacturer Force Majeure:
Vendor may claim force majeure for supplier failures if:
(a) Supplier is affected by qualifying force majeure event
(b) No alternative suppliers available despite reasonable efforts
(c) Vendor provided Customer notice within 10 days
(d) Vendor qualifies alternative suppliers within 60 days

Vendor bears risk of:
- Single-source supplier dependencies
- Supplier financial failure or bankruptcy
- Supplier quality issues or delays not caused by force majeure events"
```

### Critical Infrastructure / Government

**Higher Standards**:
```
"Force Majeure - Critical Infrastructure:
Given the critical nature of Services for [government operations /
public safety / national security], force majeure relief is available
only for:
(a) Direct government orders prohibiting performance
(b) Physical destruction of facilities by natural disaster or terrorism
(c) War or armed conflict in the service delivery location

Economic conditions, labor disputes, supplier issues, and utility
failures do NOT constitute force majeure for critical infrastructure
services. Vendor shall maintain [99.99%] uptime regardless of such events."
```

---

## Negotiation Strategies

### Customer Negotiation Priorities

1. **Narrow Definition**: Limit force majeure to truly extraordinary events
   ```
   "Force Majeure Events are limited to: (a) acts of God, (b) war,
   (c) terrorism, (d) government orders directly prohibiting performance"
   ```

2. **Payment Suspension**: Don't pay for services not received
   ```
   "Customer's payment obligations are suspended during periods of
   vendor non-performance due to force majeure"
   ```

3. **Short Termination Period**: Exit quickly if vendor can't perform
   ```
   "Either party may terminate if force majeure exceeds 30 days"
   ```

4. **Mitigation Requirements**: Vendor must actively work to restore service
   ```
   "Vendor shall use all reasonable efforts, including activating backup
   facilities, engaging alternative suppliers, and implementing workarounds"
   ```

5. **Exclusion of Vendor's Normal Risks**: Vendor bears foreseeable risks
   ```
   "Force majeure excludes: supplier failures, vendor's infrastructure
   failures, labor disputes with vendor's employees, insufficient capacity"
   ```

### Vendor Negotiation Priorities

1. **Broad Definition**: Cover wide range of events
   ```
   "Events beyond Vendor's reasonable control including but not limited to..."
   ```

2. **Payments Continue**: Revenue stream continues even if can't perform
   ```
   "Payment obligations are not excused by force majeure"
   ```
   (Note: Usually fails; customers won't pay for services not received)

3. **Longer Cure Period**: Time to remediate before termination
   ```
   "Either party may terminate only if force majeure exceeds 180 days"
   ```

4. **Include Infrastructure Dependencies**: Not liable for AWS, supplier failures
   ```
   "Force majeure includes failures of critical third-party providers
   including cloud infrastructure, internet backbone, and key suppliers"
   ```

5. **Limited Mitigation Obligations**: "Reasonable efforts" not "all efforts"
   ```
   "Vendor shall use commercially reasonable efforts to mitigate,
   provided such efforts do not require extraordinary expense"
   ```

### Balanced Middle Ground

```
"FORCE MAJEURE - BALANCED TERMS

1. Definition: Events beyond reasonable control including acts of God,
   war, terrorism, government action, pandemic (per WHO PHEIC), utility
   failures, internet backbone failures. Excludes: economic hardship,
   party's own infrastructure failures (unless caused by qualifying event),
   labor disputes with party's own employees, foreseeable events.

2. Notice: Affected party provides notice within 5 business days
   including event description, expected impact, and mitigation steps.

3. Mitigation: Affected party uses commercially reasonable efforts to
   mitigate and resume performance. Vendor activates disaster recovery
   procedures within 24 hours.

4. Payment Suspension: Customer's payment obligations are suspended
   (not eliminated) during vendor non-performance due to force majeure.
   Upon resumption, Customer pays for services actually received.

5. Partial Performance: If force majeure affects only part of Services,
   unaffected services continue. Customer pays only for services received.

6. Termination: If force majeure continues >60 days, either party may
   terminate upon 30 days notice. Vendor refunds prepaid fees for
   services not rendered.

7. SLA Exclusion: Force majeure events excluded from SLA uptime
   calculations, provided Vendor complies with notice and mitigation
   requirements.

8. Liability: Force majeure excuses performance and eliminates breach
   liability, but does not excuse data protection, confidentiality, or
   indemnification obligations."
```

---

## Common Pitfalls

### Customer Pitfalls

1. **Overly Broad Force Majeure**
   - "Any event beyond vendor's control" swallows all vendor obligations
   - Fix: Enumerate specific events, exclude normal business risks

2. **Payments Continue Despite Non-Performance**
   - Vendor excused from performing but customer still pays
   - Fix: Suspend (or eliminate) payment obligations during force majeure

3. **No Termination Rights**
   - Stuck with non-performing vendor indefinitely
   - Fix: Termination right after 30-90 days of continued force majeure

4. **Third-Party Failures as Force Majeure**
   - Vendor excused for every supplier or cloud provider hiccup
   - Fix: Require vendor maintain redundancy; limit to major outages

5. **No Mitigation Requirements**
   - Vendor claims force majeure and does nothing
   - Fix: Require commercially reasonable mitigation efforts

### Vendor Pitfalls

1. **No Force Majeure Clause**
   - Stuck with common law impossibility (very narrow)
   - Fix: Include force majeure clause in all contracts

2. **Undefined Events**
   - "Acts of God" ambiguous (does pandemic count?)
   - Fix: Explicitly enumerate events including pandemic

3. **Failure to Give Notice**
   - Vendor loses force majeure defense by late notice
   - Fix: Ensure notice procedures in vendor playbook

4. **Claiming Force Majeure for Foreseeable Events**
   - Hurricane in Florida during hurricane season = foreseeable
   - Fix: Only claim genuinely unforeseeable extraordinary events

5. **No Customer Mitigation Obligation**
   - Customer can claim force majeure without trying alternatives
   - Fix: Require both parties use mitigation efforts

---

## Validation Questions

When reviewing force majeure provisions, verify:

### Definition and Scope

- [ ] What events qualify as force majeure? (specific list or general language)
- [ ] Are pandemics explicitly included?
- [ ] Are third-party failures (cloud, suppliers) included?
- [ ] Are labor disputes with own employees excluded?
- [ ] Are economic hardship and financial difficulties excluded?
- [ ] Is foreseeability a disqualifying factor?

### Notice Requirements

- [ ] How quickly must affected party provide notice? (3/5/10 days)
- [ ] What information must notice include?
- [ ] Are ongoing updates required?
- [ ] What is consequence of late or missing notice?

### Obligations Affected

- [ ] What obligations are excused? (all except payment is standard)
- [ ] Are payment obligations excused or suspended?
- [ ] Are partial outages addressed?
- [ ] Do data protection and confidentiality obligations continue?

### Mitigation

- [ ] Must affected party use mitigation efforts?
- [ ] What standard? (reasonable, commercially reasonable, all efforts)
- [ ] Who bears mitigation costs?
- [ ] What happens if party fails to mitigate?

### Duration and Termination

- [ ] How long can force majeure continue before termination right? (30/60/90 days)
- [ ] Can either party terminate or only non-affected party?
- [ ] What notice is required for termination?
- [ ] What refunds or payments due upon termination?
- [ ] Is contract term extended by force majeure duration?

### Integration with Other Provisions

- [ ] Are force majeure events excluded from SLA calculations?
- [ ] Does force majeure excuse liability?
- [ ] Are warranties suspended during force majeure?
- [ ] Are indemnification obligations affected?

---

## When to Consult Experts

Consult legal counsel when:

1. **International transactions**: Geopolitical events, currency controls, trade sanctions
2. **Critical services**: Mission-critical systems where force majeure could be devastating
3. **Post-COVID disputes**: Claiming or defending against pandemic force majeure
4. **Long-term contracts**: Multi-year agreements with significant exposure
5. **Force majeure claimed**: Vendor/customer claims force majeure; assessing validity
6. **Custom force majeure language**: Negotiating non-standard terms

Consult technical/business experts when:

1. **Infrastructure resilience**: Assessing whether vendor's architecture reasonably prevents force majeure exposure
2. **Disaster recovery**: Designing mitigation strategies for force majeure events
3. **Supply chain analysis**: Evaluating single-source supplier risks
4. **Business continuity**: Developing force majeure response procedures

---

## Cross-References

**Related Key Provisions** (tech_transactions):
- `termination_provisions.md` - Extended force majeure often triggers termination rights
- `liability_limitations.md` - Force majeure as excuse for liability
- `service_levels.md` - Force majeure exclusions from SLA calculations
- `warranties_representations.md` - Force majeure effect on warranty obligations

**Contract Intelligence Skills** (from 4,900+ real contracts):
- `force-majeure-taxonomy.md` - Force majeure clause patterns from real contracts
- `force-majeure-examples.md` - Real force majeure language extracted from contracts
- `force-majeure-negotiation.md` - Strategic negotiation guidance with S1-S13 patterns

**Cognitive Patterns** (apply to force majeure analysis):
- `S3` - Multi-domain synthesis (legal doctrine vs. business impact)
- `S7` - Multi-perspective analysis (supplier vs. customer positions)
- `S8` - Scenario-based planning (what events could trigger FM?)
- `S11` - Temporal integration (notice periods, cure periods)
- `BI3` - Context-aware risk (pandemic lessons, geopolitical risks)

---

## References and Validation

**CAUTION**: This Skills file is synthetically generated and has not been validated by legal experts. The content is based on:
- General contract law principles (impossibility, impracticability, frustration)
- Common commercial force majeure provisions
- Post-COVID-19 pandemic clause evolution
- Technology industry practices

**Confidence Level**: 0.6 (Synthetic - Not Expert-Validated)

**Known Limitations**:
- Force majeure is highly fact-specific and jurisdiction-dependent
- Post-COVID-19 case law still developing (pandemic foreseeability, remote work alternatives)
- International force majeure varies significantly by jurisdiction
- Industry-specific standards (critical infrastructure, government contracts) require specialized expertise

**Recommended Validation**:
Before relying on this information:
1. Consult legal counsel for material contracts or force majeure disputes
2. Review jurisdiction-specific force majeure case law
3. Assess technical feasibility of mitigation measures with experts
4. Consider insurance coverage for force majeure events (business interruption)

**For Expert Review**:
Kevin Keller should validate:
- [ ] Standard force majeure event definitions and exclusions
- [ ] Post-COVID-19 pandemic clause best practices
- [ ] Customer vs. vendor negotiation priorities
- [ ] Interaction with SLA, liability, and warranty provisions
- [ ] Third-party infrastructure failure treatment (cloud providers)
- [ ] Mitigation obligation standards and enforcement
- [ ] Termination thresholds and refund practices
