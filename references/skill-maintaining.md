# Maintaining the skill

Read this before changing, pulling or pushing the skill. It syncs across machines through its own
GitHub repository (`github.com/bai-ting-chen/bc-image-roaster`).

## What may go in (RULES GOV_01, GOV_02)
- **Methods that hold for any image:** prompt rules, failure → fix rows, edit-type templates,
  model facts with their check date. Test each with "would it hold on a different image?"
- **Never project data:** no test images, project names or paths, client or site names. A lesson
  goes in stripped of where it came from ("a sculpture moved to where the removed desk stood").
- **State each rule once, in [RULES.md](../RULES.md);** references carry the how-to and a pointer
  such as "(RULES CHK_02)".
- **New failure seen and fixed** → one row in the table in [prompting.md](prompting.md).
- Code goes into `scripts/` only once it runs on images it was not written for.

## Writing patterns
| Pattern | Files |
|---|---|
| Sequential workflow (numbered steps, a check after each) | SKILL.md, check.md |
| Iterative refinement (criteria, check, fix, stop rule) | check.md |
| Domain intelligence (rules applied before acting, sources and dates) | prompting.md, models.md |
| Context-aware selection (a template per case) | edit-types.md |

## Before editing
1. `git fetch origin`, then `git pull --ff-only origin main`. Never force-push over commits you
   have not seen.
2. Identity, once per clone: `git config user.name bai-ting-chen`,
   `git config user.email baitingchen.arch@gmail.com`.
3. If `MIGRATE.md` exists, apply the sections from other machines (`From:` line), run their
   checks, then remove those sections.

## MIGRATE.md
Write a section in the same commit when a change can break another clone (moved or renamed files,
new setup): `# MIGRATE: <topic>`, `From: <hostname>`, `## What changed`, `## Steps`,
`## Check after pull`. Not a change log.

## Commit and push
Messages say what changed and why. Push only the skill; project folders never get a remote.
