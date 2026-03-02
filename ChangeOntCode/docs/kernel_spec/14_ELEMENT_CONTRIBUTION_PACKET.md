# docs/kernel_spec/14_ELEMENT_CONTRIBUTION_PACKET.md

# Element Contribution Packet

## Status
- **Binding**: elements emit typed structural contribution packets
- **Recommended starting point**: packet family below
- **Open design space**: exact encoding details and packet serialization conventions

---

## 1. Principle

Elements should not all be forced into one flat scalar action-score interface.

Elements are different mechanism families:
- some are continuation-oriented,
- some are regime-oriented,
- some are cadence-oriented,
- some are mainly structural diagnostics.

The kernel therefore uses a **typed structural contribution packet**.

---

## 2. Packet rule

**Binding**

Every element must emit a contribution packet that fits a common packet family.

The packet may omit optional fields, but the contract must be shared.

---

## 3. Minimum mandatory fields

**Binding**

Every contribution packet must include:

- `element_id`
- `scope_ref`
- `contribution_kind`
- `confidence`
- `diagnostics`

---

## 4. Optional canonical fields

**Recommended starting point**

A contribution packet may also include:

- `branch_vote_surface`
- `regime_contribution`
- `cadence_contribution`
- `weight_hint`
- `bus_updates`

---

## 5. Field meanings

### `element_id`
Which element emitted the packet.

### `scope_ref`
Which part of the current path-space fragment the packet refers to.

### `contribution_kind`
The main kind of contribution.

**Recommended starting point**
Use a controlled set such as:
- `continuation`
- `regime`
- `cadence`
- `constraint`
- `structural_diagnostic`

### `confidence`
How sharply the element takes its own structural judgment.

### `diagnostics`
Supporting structural evidence or measurements.

### `branch_vote_surface`
Optional local branch preference contribution.

### `regime_contribution`
Optional regime interpretation contribution.

### `cadence_contribution`
Optional reevaluation cadence contribution.

### `weight_hint`
Optional local salience suggestion.

### `bus_updates`
Optional structured signal updates for the bus.

---

## 6. Branch vote rule

**Binding**

Not all elements must emit branch votes.

Elements that mainly perform regime/cadence/diagnostic work may omit `branch_vote_surface`.

This is not a contract violation.

---

## 7. Misalignment examples

Code is misaligned with this spec if:
- elements are forced to emit only flat action scores,
- packet types are inconsistent and ad hoc,
- regime/cadence-oriented elements have no way to express their contribution,
- or branch votes are required even when an element has no genuine continuation role.