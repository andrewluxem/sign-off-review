# Profile: build-plan

**Use for:** specs, run sheets, build plans, and prompts written for coding agents.
**Signals:** numbered steps, commands, paths, a done-when.

## Seat 1: Decision (owner)

- **1.1** A done-when exists and can be checked: a command, a test or an observable state, not "it works".
- **1.2** Scope is stated, and non-goals say what the plan will not do.
- **1.3** A named person or role owns the outcome and makes the calls the plan leaves open.
- **1.4** The goal says why the work matters, so the executor can make sensible calls where the plan is silent.

## Seat 2: Logic

- **2.1** The steps run in an order that works: nothing uses an output before the step that creates it.
- **2.2** Dependencies (access, other teams, earlier steps, external services) are stated where they apply.
- **2.3** Nothing is missing between steps: setup, migration, verification and cleanup are all present.
- **2.4** Verification comes before anything irreversible: every destructive step follows a check that its input is good.

## Seat 3: Evidence

- **3.1** Every path, flag, config key, environment variable and version either cites the file and line it comes from or carries a discovery command (`--help`, `ls`, `grep`) to confirm it.
- **3.2** Commands are complete and can be pasted as written. Any placeholder comes with a rule for filling it in.
- **3.3** Claims about the current state (what is installed, what a service does, how large the data is) say how they were established.
- **3.4** The plan says where each secret or credential comes from, and writes none of them into the plan.

## Seat 4: Skeptic (operator)

- **4.1** For each risky step, the plan says what happens if it fails halfway, and what to do then.
- **4.2** Every destructive or state-changing step has a way back, and a backup is taken and verified before it runs.
- **4.3** Downtime, cost and resource use are stated where they matter: the window, the duration, the spend, disk, quotas.
- **4.4** Security is handled: permissions, exposure, secrets, and anything the plan opens up.
- **4.5** Decisions the plan depends on are on record with an ID (for example D3, D8) and cited where they apply, not left in someone's head.

## Seat 5: Outsider (fresh agent)

- **5.1** A fresh agent with no chat history and only this document could carry out every step. Any reference to an earlier conversation ("as agreed", "the layout we discussed") is a finding.
- **5.2** Every host, service, file and term is introduced before it is used.
- **5.3** Where a step needs judgment, the plan gives the rule to apply or says to stop and ask.
- **5.4** The plan says what to report back, and when to stop.

## Tie-out scope

Every version, count, size, port and duration, across the plan and any files passed in with it. A version or port stated two ways is a mismatch. A path spelled two ways is an Evidence finding.

## Outside view

For each duration, cost and size, ask what it is based on: a past run or a measurement. List estimates with no basis under Missing outside view.

## Premortem prompts

Internal (on the author's or executor's side):
- No named owner to make calls mid-run.
- The plan was written from memory, so a path, flag or version is wrong.
- The executor lacks the access the plan assumes.
- A decision the plan relies on exists only in chat.

External:
- A dependency upgrade or API change lands mid-run.
- The data is larger or messier than assumed.
- A service the plan relies on is down.

## False alarms (build-plan)

- A short plan for a small change.
- No rollback for read-only steps or steps that can safely run again.
- No architecture explanation, when the goal and the steps are clear.
- Command style (long or short flags), when both forms are verified.
- No test suite for a one-off script whose done-when already proves it worked.
