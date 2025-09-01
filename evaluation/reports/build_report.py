from future import annotations  
import argparse  
import json  
from pathlib import Path  
from typing import Dict, List

from evaluation.reports.tables import summarize_episode_rows, rows_to_markdown  
from experiments.logging.plots import plot_flips_and_events, plot_episode_aggregates

def _load_jsonl(path: Path) -> List[Dict]:  
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]

def build_report(run_dir: Path, out_md: Path) -> None:  
    """  
    Assemble a simple Markdown report from a run directory structure:  
    run_dir/  
    steps_episode_*.jsonl  
    episodes_summary.jsonl  
    config_resolved.yaml (optional)  
    agent_spec.json (optional)

    ```
    Produces:
    out_md (markdown)
    figures under run_dir/figures/
    """
    run_dir = run_dir.resolve()
    out_md = out_md.resolve()
    figures_dir = run_dir / "figures"
    figures_dir.mkdir(exist_ok=True, parents=True)

    # Episode-level summary
    ep_summary_path = run_dir / "episodes_summary.jsonl"
    if not ep_summary_path.exists():
        raise FileNotFoundError(f"Missing {ep_summary_path}")

    rows = _load_jsonl(ep_summary_path)
    agg = summarize_episode_rows(rows)
    tbl = rows_to_markdown(rows)

    # One step-log plot (first episode) and aggregates plot
    step_logs = sorted(run_dir.glob("steps_episode_*.jsonl"))
    step_fig = None
    if step_logs:
        step_fig = figures_dir / "episode0_flips_events.png"
        try:
            plot_flips_and_events(step_logs[0], step_fig, title="Episode 0 — flips & events")
        except Exception as e:
            step_fig = None  # keep report generation robust

    agg_fig = figures_dir / "episodes_summary.png"
    try:
        plot_episode_aggregates(ep_summary_path, agg_fig, title="Per-episode metrics")
    except Exception:
        agg_fig = None

    # Optional artifacts
    cfg_text = ""
    cfg_path = run_dir / "config_resolved.yaml"
    if cfg_path.exists():
        cfg_text = cfg_path.read_text()

    agent_text = ""
    agent_path = run_dir / "agent_spec.json"
    if agent_path.exists():
        agent_text = agent_path.read_text()

    # Build Markdown
    md = []
    md.append("# CO-core: Renewal Toy — Report")
    md.append("")
    md.append(f"_Run directory_: `{run_dir}`")
    md.append("")
    md.append("## Episodes (table)")
    md.append("")
    md.append(tbl)
    md.append("")
    md.append("## Aggregates")
    md.append("")
    md.append(f"- flips/ep: **{agg['flips_mean']:.2f} ± {agg['flips_iqr']:.2f}**")
    md.append(f"- FDR_windowed: **{agg['fdr_mean']:.3f} ± {agg['fdr_iqr']:.3f}**")
    md.append(f"- slope_window: **{agg['slope_mean']:.4f} ± {agg['slope_iqr']:.4f}**")
    md.append(f"- AUReg_window: **{agg['au_mean']:.4f} ± {agg['au_iqr']:.4f}**")
    md.append(f"- episodes: **{agg['n_episodes']}**")
    md.append("")
    if step_fig and step_fig.exists():
        md.append("## Episode 0 — flips & events")
        md.append(f"![episode0]({step_fig.relative_to(run_dir).as_posix()})")
        md.append("")
    if agg_fig and agg_fig.exists():
        md.append("## Per-episode metrics")
        md.append(f"![episodes]({agg_fig.relative_to(run_dir).as_posix()})")
        md.append("")

    if cfg_text:
        md.append("## Config (resolved)")
        md.append("")
        md.append("```\n" + cfg_text.strip() + "\n```")
        md.append("")

    if agent_text:
        md.append("## Agent Spec")
        md.append("")
        md.append("```\n" + agent_text.strip() + "\n```")
        md.append("")

    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_md.write_text("\n".join(md), encoding="utf-8")
    

    if name == "main":  
        ap = argparse.ArgumentParser()  
        ap.add_argument("--run_dir", type=str, required=True, help="Path to outputs/<run_name>")  
        ap.add_argument("--out", type=str, default="report.md", help="Markdown output file path")  
        args = ap.parse_args()  
        build_report(Path(args.run_dir), Path(args.out))