# Venture Time Tracker

A single-file, offline time tracker for people running several ventures at once. Track hours and billable value per venture and per activity, run multiple timers in parallel, and see the breakdown in charts. No accounts, no server, no build step — just one HTML file.

## Features

- **Multiple concurrent timers** — start several at once for parallel or background work. Each timer has its own live clock, a **Pause/Resume**, a **Stop & save**, and its own note field. Running timers survive a page reload, and the browser tab title shows how many are ticking.
- **Manual entry** — backfill sessions you forgot to time, with date, hours, billable flag, rate and note.
- **Ventures & activities** — add, edit and delete your own ventures (with colours) and the activities under each (e.g. Marketing, Sales, a specific client). Cross-venture activity-type tags for rollups.
- **Move an activity between ventures** — reorganised as you went? Move a whole activity into another venture, or into a brand-new one you name on the spot. Its entire history, its running timers and its billable value move with it. If the destination already has an activity by that name, you can merge the two into one.
- **Analytics** — hours by venture, hours by activity type, hours over time, billable value (£) by venture and by activity, plus top activities and KPI cards. Filter by date range, then tick and untick individual ventures and activities — everything starts selected, so you narrow by deselecting what you don't want to see.
- **Your data stays yours** — everything is stored locally in your browser (IndexedDB). Optionally connect a `time-data.json` file on your computer so every save is written to disk; keep that file in a git repo and each commit is a versioned backup.
- **Export** — one-click JSON backup and CSV export (handy for invoicing billable hours).

## Getting started

1. Download or clone this repo.
2. Open `index.html` in a modern browser (Chrome or Edge recommended — the direct file-save feature uses the File System Access API).
3. Head to **Ventures & Activities** to set up your own ventures, then start tracking.

The app opens with a few generic example ventures so you can see how it works. Delete or rename them and add your own.

## Saving your data to disk (optional)

By default your data is saved in the browser. To also keep a file on disk:

1. Open the **Data & Backup** tab.
2. Click **Connect / create data file** and save it as `time-data.json`.
3. Every change now writes to that file automatically.

`time-data.json` is listed in `.gitignore` so your real data is never committed if you fork or extend this project.

## Tech

Plain HTML, CSS and JavaScript in one file. Charts via [Chart.js](https://www.chartjs.org/) loaded from a CDN. No framework, no bundler.

## Licence

MIT — see [LICENSE](LICENSE).
