## House rules

### Governance

**GOV_01 — Recording Reusable Knowledge**  
Rule: Keep image-independent methods, prompt rules, failure fixes and model facts; a single edit's results stay in its work folder. One-time operations go to the user in chat, never into the skill.  
Read: [skill-maintaining.md](references/skill-maintaining.md)

**GOV_02 — Working With Skill And Project Files**  
Rule: Publish only generic method and code; no project images, names or paths. The skill is self-contained: it runs with an empty CLAUDE.md and memory; skill rules live only here.  
Read: [skill-maintaining.md](references/skill-maintaining.md)

**GOV_03 — Synchronizing This Skill**  
Rule: Pull before editing, use the per-clone identity, apply MIGRATE.md if present, and write MIGRATE.md for any change that can break another clone.  
Read: [skill-maintaining.md](references/skill-maintaining.md)

**GOV_04 — Extending Code Or Documents**  
Rule: One module per job, one place per fact; a reference that documents one script shares its name. Add a safeguard only for a failure a test has shown.  
Read: [skill-maintaining.md](references/skill-maintaining.md)

### Editing

**EDT_01 — Before Writing A Prompt**  
Rule: Read the input at full size into a scene inventory; name every target, look-alike and at-risk item.  
Read: [image-reading.md](references/image-reading.md)

**EDT_02 — The Request Is Unclear**  
Rule: Take the user's words at their full scope. Ask back only when the request and the image disagree (count, which object) or a word has two readings (evening: dusk or night); otherwise decide and say what was decided.  
Read: [prompting.md](references/prompting.md)

**EDT_03 — Running A Prompt**  
Rule: Show the prompt as it will be sent, with one plain-English line on why, before the first run; warn when the image holds small text.  
Read: [prompting.md](references/prompting.md)

**EDT_04 — A Follow-Up Edit**  
Rule: Start every run from the original image and merge the new change into one prompt; offer one chained step only after the retry cap, still checked against the original.  
Read: [check.md](references/check.md)

### Models

**MOD_01 — Choosing A Model**  
Rule: Run `fal-ai/nano-banana-2` at 2K; escalate to `fal-ai/nano-banana-pro` once, after the retry cap.  
Read: [models.md](references/models.md)

### Checking

**CHK_01 — Judging A Try**  
Rule: Judge the change and the preservation separately, from full-size crops against the inventory; the drift number only says where to look.  
Read: [check.md](references/check.md)

**CHK_02 — A Try Fails**  
Rule: Name the failure, change one thing in the prompt, retry; stop after 3 tries and escalate (MOD_01) or ask the user.  
Read: [check.md](references/check.md)

**CHK_03 — Delivering**  
Rule: Deliver the final image, the compare sheet of the input and every try, and one line per failed try; then delete prepared copies and crops.  
Read: [check.md](references/check.md)
