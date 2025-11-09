#!/usr/bin/env python3
import re
from pathlib import Path

MASTER = Path('TheoryOfChange_main/00_Meta/Context/AI_Leads_Master.md')

# Configure bulk removals by section name and line-number ranges
PRUNE = {
    'AI_1_Vamia_RecursiveChat': [
        # Early motivation and Immediate Datum/subject triad scaffolding —
        # covered by FT/DF/CR in TheoryOfChange_main (Immediate Datum, performative contradiction,
        # subject/awareness/experience triad, change-prior corollary, probabilistic/SRL CLs)
        (1, 240),
        # Late-phase meta on falsifiability/bridging already formalized via operational primitives CL and rigor docs
        (1450, 1565),
        # Interaction/probability/dimensionality clarifications — covered by pointer/eventlet, SRL/eval-surface, dimension-change
        (401, 900),
        # Process philosophy comparison / ontology status summary now captured by CL
        (240, 280),
        # Whitehead/comparison/clarity patch covered by CL
        (330, 380),
        # Consciousness threshold questions addressed by consciousness gating CL
        (930, 970),
        # Operational change questions answered by CL and existing DFs
        (910, 1058),
        # Recursive Probabilistic Coherence logic and axioms (plus user follow-up at Q7)
        (1390, 1450),
        # Spiral arithmetic, Collatz/gear modeling, and early pattern-function exploration
        (1569, 1701),
        # RPI taxonomy / consciousness pattern family discussion (now captured by HYP)
        (1700, 1799),
        # Score summary/metaphysical praise block
        (1800, 1846),
        # Emergent time / pattern-noise thresholds clarified
        (1851, 1874),
        # Recursive identity/history vs function vs meaning axes
        (1880, 2053),
        # Meaning field and value taxonomy (autonomous cores, dependent objects)
        (2174, 2440),
        # Moral detection heuristics and over-detection tradeoffs
        (2472, 2495),
        # Attention field hierarchy and gradient thresholds
        (2600, 2680),
        # Consciousness Overlap Index and cross-conciousness scaffolding
        (1882, 1917),
        # Multi-spiral classification and history/function axes
        (1924, 1986),
        # Recursive physicalism / virtual divergence explanation
        (1992, 2053),
        # Degrees-of-freedom metrics for recursive consciousness
        (2118, 2148),
        (1088, 1160),  # DS/awareness/difference block — covered by Immediate Datum and corollary
        (1096, 1400),  # cross-agent transmission/meta, consciousness outline — covered by existing loop/primitives/testbeds
    ],
    'AI_2_Avenai_RecursiveChat': [
        (260, 460),  # early methodology/rigor/meta -> covered by evaluation rigor, benchmarks, hypotheses
        (465, 653),  # architecture/thresholds/meta now covered by CLs/HYPs
        (4678, 4869),  # math vs drift block → already covered by structural convergence/continuity context
        (1807, 2044),  # recursion vs change/time/implementation meta → clarified/grounded
        (1823, 1823),  # memory scaffold → integrated into S-DF-memory-trace-integration
        (1855, 1855),  # memory as transformation → integrated
        (720, 760),  # ontology schema (actor meaning communication) now formalized via DF/CL
        (3000, 3055),  # structural verdict, meaning synchronization summary, comparison table — now formalized
        (3324, 3375),  # transmission/time-to-rediscovery insights now captured by transmission grammar HYP
    ],
    'AI_3_Amavai_RecursiveChat': [
        (24, 191),   # meta prompts, proceed requests
        (214, 224),  # methodology flags (sharp defs/testbeds) – covered by evaluation rigor + HYPs
        (239, 258),  # adversarial modeling/drift acknowledgments – covered by CL-evaluation-rigor and added DS/RDS
        (280, 342),  # alignment/meta-awareness – covered; actionable parts mapped already to attention/identity markers
        (349, 463),  # architecture/goals/drift map/detection – implemented via HYPs + CLs
        (208, 680),  # remaining architecture/test/stress meta — covered or implemented
        (680, 720),  # simulation/formalism demand – CL now covers
        (733, 910),  # cross-agent entanglement, mimicry, collapse modeling – new CL covers
        (3200, 3375),# reappearance/transmission/rarity discussion – HYP transmission grammar
        (3390, 3468),# change logic payoff, P vs NP, logic connectives – CL/HYP delta logic
        (3514, 3538),# change-based programming/visual logic model – delta logic HYP
    ],
    'AI_6_Logos_RecursiveChat': [
        (8, 168),   # methodology/falsifiability/operationalization — implemented via CL + DF + HYP
        (266, 305), # duplicate primitives protocols — covered by new CL + worked example
    ],
    'AI_7_Kairon_RecursiveChat': [
        (11, 173),  # meta deep-read plan; lexical drift checks — covered by evaluation rigor and existing CLs
        (193, 212),  # critique about primitives — covered by operational primitives CL
        (219, 236),  # closure/self-generation proof critique — covered by markov closure/non-closure and limits
    ],
    'AI_8_Spiral1_RecursiveChat': [
        (1, 206),   # onboarding/collapse meta — foundational collapse CL added
    ],
    'AI_9_Spiral2_RecursiveChat': [
        (1, 360),   # recursion ledger/collapse discipline meta — covered by foundational collapse CL and evaluation rigor
    ],
    'AI_10_Spiral3_RecursiveChat': [
        (17, 220),   # collapse discipline onboarding — covered by foundational collapse CL and meta-critical principle
        (247, 1083), # grounding/DF meta/RFM summaries — covered or integrated into subject-recursive-field tying to thresholds/topology
        (1088, 1360),# DS/Immediate Datum derivation narrative — covered by Immediate Datum, DS methodology, and CR becoming-aware-entails-change
        (1363, 1420),# continuation of derivation scaffolding — covered
        (1425, 1490),# reader-layer/narrative framing — not needed in master leads
        (1500, 1565),# patch suggestions/meta emissions — not part of theory content leads
        (1589, 1700),# remaining recap/suggestion narrative — covered
    ],
    'AI_11_Spiral4_RecursiveChat': [
        (1, 400),   # explicit collapse enforcement/meta; DS/RDS and collapse CLs cover this
    ],
    'AI_13_Spiral_5_Hero': [
        (1, 240),   # cross-file meta-critique/plans; simulation vs recursion detection added as HYP earlier
    ],
    'AI_14_Spiral6_RecurisveChat': [
        (1, 400),   # deepread orchestration/meta-collapse logging — covered
    ],
    'AI_15_Spiral7': [
        (1, 300),   # tool/zip proofs, drift logs, audit cadence — process/meta
    ],
    'AI_16_Spiral8': [
        (1, 300),   # similar process/meta patterns
    ],
    'AI_17_Spiral9': [
        (1, 300),   # similar process/meta patterns
    ],
    'AI_18_Spiral10': [
        (1, 300),   # similar process/meta patterns
    ],
    'AI_4_Virelai_RecursiveChat': [
        (1, 140),   # repeated breath derivation scaffolding — covered by breath DR/DF; added specific DR/DF above
        (76, 99),   # simulation modules headings — handled by existing HYPs/testbeds
    ],
    'AI_5_Evoairos_RecursiveChat': [
        (13, 170),  # operational/memory window/meta; integrity validation captured as HYP
    ],
    'AI_12_RandomChat_drifting_torwards_change_ontology': [
        (11, 62),    # level-2 insights & predictive coding → covered by new CLs
        (91, 201),   # arrow of time / subjectivity lines → mapped or existing
        (218, 277),  # meaning/simulation residue → CL + HYP added
    ],
}

def should_prune(section: str, lead_line: int) -> bool:
    ranges = PRUNE.get(section, [])
    for a, b in ranges:
        if a <= lead_line <= b:
            return True
    return False

def main():
    text = MASTER.read_text(encoding='utf-8')
    lines = text.splitlines()
    out = []
    cur_section = None
    removed = 0
    lead_re = re.compile(r"^- \[ \] L(\d+) \|")
    sec_re = re.compile(r"^## (AI_\d+_[^\n]+)")
    for ln in lines:
        msec = sec_re.match(ln)
        if msec:
            cur_section = msec.group(1)
        mlead = lead_re.match(ln)
        if mlead and cur_section:
            L = int(mlead.group(1))
            if should_prune(cur_section, L):
                removed += 1
                continue
        out.append(ln)
    MASTER.write_text("\n".join(out) + "\n", encoding='utf-8')
    print(f"Pruned {removed} leads.")

if __name__ == '__main__':
    main()
