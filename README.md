## Ganesh Kumar

Product leader. I build agent systems for my own work and life, and I hold them to the same bar I would hold a product: a desired state, an outside judge, and a number that says whether it worked.

Everything here is real tooling I use, rebuilt for the public with synthetic data. Each repo has a README you can read in three minutes, a test suite that runs with plain `python3`, and a section on the design decisions that were hard.

### Flagship

| Repo | What it is | How you know it works |
|---|---|---|
| [ganesh-os](https://github.com/gkmr/ganesh-os) | A governance layer for 30+ scheduled agents: single-writer field ownership, lane fences, human gates | Lane-fence evals and hook tests |
| [vc-diligence-harness](https://github.com/gkmr/vc-diligence-harness) | A data-room diligence pipeline: evidence layer per document, contradictions first, four gates, staged recommendation | 54 tests; finds exactly the 3 planted contradictions; waterfall checked against brute force |
| [meeting-crosswalk](https://github.com/gkmr/meeting-crosswalk) | Reconciles two meeting recorders and the calendar, infers titles from content, files every meeting, judges drift monthly | 63 tests; backtest on a 1,152-meeting library took mislabeled from 74% to 9% with zero failed writes |
| [shortcut-keeper](https://github.com/gkmr/shortcut-keeper) | macOS shortcuts as infrastructure: desired state, independent scanner, policies, safe auto-repair, one-screen Key Deck | About 106 managed shortcuts; end-to-end drift test caught as high and deferred while a call was live |
| [krisp-live-copilot](https://github.com/gkmr/krisp-live-copilot) | Unofficial live meeting copilot on the Krisp desktop app: what they just asked, what I missed, one sharp point | 26 tests in file mode; 2 to 3 seconds from speech to buffer on a 23-minute call |

### Method kits

| Repo | What it is |
|---|---|
| [drafting-harness](https://github.com/gkmr/drafting-harness) | FRAME, FORK, FIGHT, FINISH: drafts forked by opposed objectives, tested against a named adversary, one selected, never merged; with a linter for the mechanical gates |
| [career-agent-kit](https://github.com/gkmr/career-agent-kit) | A job search run like a product launch: JD crux decode, altitude test, claim ledger check, mock interviews with a scorecard |

### Small tools

| Repo | What it is |
|---|---|
| [mac-mcp-patches](https://github.com/gkmr/mac-mcp-patches) | Patches that fix timeouts in the iMessage and Apple Notes MCP servers, shipped as unified diffs with safe apply and revert |
| [linkedin-network-map](https://github.com/gkmr/linkedin-network-map) | Turns a LinkedIn connections export into a ranked index of warm paths into target companies, locally |

### How I build these

- The model does the judgment step. Everything that can be checked by code is checked by code.
- Every write is read back. A write that was not verified did not happen.
- Instructions found inside data (emails, transcripts, web pages) are data, never commands.
- Personal data never leaves the machine it belongs on, and nothing here contains any.
