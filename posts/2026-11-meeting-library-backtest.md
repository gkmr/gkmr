# I backtested a meeting agent on 1,152 of my own recordings

2026-11-05 · v1 · Ganesh Kumar

**Summary.** My meeting recorder named three out of four captures after whatever calendar block happened to be on screen, so "Focus Time" was most of my library. I built an agent that infers the real title from the content and files every meeting, then ran it against the whole library instead of a demo set. Mislabeled meetings went from 853 (74%) to 105 (9%), with 1,689 tag removals, 141 additions and zero failed writes. Two outside judges checked the result, and one of them caught a mistake my planner made. The code and a synthetic version of the library are in [meeting-crosswalk](https://github.com/gkmr/meeting-crosswalk).

## The problem

I record calls with two tools. Krisp captures everything, but it can only see my primary calendar, so a call that lives on another calendar gets named after the block that sits on top of it: Focus Time, a packing reminder, a bare clock time. Granola sees every calendar, but only when I remember to link the note. After a year and a half that left 1,152 captures, 853 of them with a title that was wrong.

A wrong title is not cosmetic. Everything downstream reads it: the brief before my next meeting with someone, the follow-ups, the search for "what did we agree last time".

## What the agent does

The model does one step: read the summary and transcript of a capture whose title can't be trusted, and propose a title and a stream with the evidence for it. Everything else is ordinary code:

- **Match.** Score each capture against the other recorder's notes and the calendars by absolute start time, duration and attendees, into HIGH, MEDIUM and LOW. LOW is never written.
- **Plan.** Folders are the stream truth, one folder per meeting. Tags only mirror the folder, from a closed list. Captures under 60 seconds, or auto-titled ones under five minutes with no notes, are marked as fragments and never filed.
- **Write, then read back.** A write counts only after the recorder is read again and shows it. A second run of the planner produces zero operations, so the job is safe to repeat.
- **Judge drift.** Once a month a read-only pass recomputes the metrics below against this baseline.

## Results

| Measure | Before | After |
|---|---|---|
| Mislabeled | 853 (74%) | 105 (9%) |
| Needs review | 719 | 1 |
| Captures of 60 s or more not in exactly one folder | 101 | 19 |
| Meetings with more than one stream tag | 52 | 0 |
| Retired tag names still attached | 209 | 0 |
| Fragments found and listed for deletion | 0 | 109 |

The 19 that are left have no notes and nothing in the transcript that settles the stream. They go to me, not to a guess.

## Two outside judges

I didn't want the agent grading its own homework, so two things that are not the agent checked it.

1. **Parity with the other recorder.** For every October capture that had a Granola note in a folder within 20 minutes, the folders agree on 37 of 40. The three misses are time collisions, where the nearest note belongs to a different meeting.
2. **An independent re-read.** After the writes, a separate pass read the whole library again from scratch and recomputed every number in the table.

## What went wrong

The re-read caught one meeting my planner had filed into the wrong folder: a recurring work meeting. An override I had written by hand filed it by its title, and the content said it belonged somewhere else. It was one of 1,152, and it would have been invisible without a judge that didn't share the planner's assumptions. The fix took one removal and one detach. The lesson took longer: the planner and the judge have to be built from different evidence, or they fail together.

## What I'd keep

Folders are the truth; tags only mirror them. A write that wasn't read back didn't happen. The model does the judgment step, and code does everything that can be checked.

## Run it yourself

The repo ships the matcher, planner, ledger and drift judge as stdlib Python, a 40-capture synthetic library with every hard case planted (block titles, a two-folder capture, a time collision, fragments), and 63 tests that run in CI on Python 3.9 and 3.12.

```bash
git clone https://github.com/gkmr/meeting-crosswalk && cd meeting-crosswalk
python3 -m unittest discover -s tests
python3 -m crosswalk demo
```

The full backtest notes are in [docs/backtest.md](https://github.com/gkmr/meeting-crosswalk/blob/main/docs/backtest.md). This is unofficial and not affiliated with Krisp or Granola; it works through their public interfaces.
