
# ✅ Cursor AI Priming Checklist for Superstack

> Ensure Cursor is fully primed to leverage your structured knowledge system for maximum AI effectiveness.

This checklist covers strategic setup steps to ensure you're getting the most from Cursor + Superstack. It includes context linking, prompt hygiene, and enhancement recommendations.

---

## 🧠 1. Context Integration

- [x] **Ensure context modules are co-located in the repo**
  - All files from `docs/ai-context/` are inside the active Cursor workspace.

- [x] **Use AI-context headers in source files**
  - Add `// AI-Context: path/to/module` at the top of files using relevant modules.
  - Example:
    ```ts
    // AI-Context: design/principles/visual-hierarchy
    // AI-Context: development/patterns/state-isolation
    ```

- [x] **Apply context selectively**
  - Use 2–4 relevant modules per file to avoid overloading Cursor.

- [x] **Maintain a central context index**
  - Create a summary guide (like this one) for easy navigation and updates.

---

## ⚙️ 2. Cursor Configuration & Usage

- [x] **Enable full project reference in Cursor settings**
  - Allows Cursor to embed and reason over your local files.

- [x] **Use workspace summary to pre-embed context**
  - Prompt Cursor: “Summarize the contents of `docs/ai-context/`.”

- [x] **Use in-code comment prompting**
  - Insert actionable TODOs or questions inline:
    ```ts
    // TODO: Refactor with visual hierarchy rules
    // Ask: "Does this follow spacing system guidelines?"
    ```

- [x] **Structure dev notes for reference**
  - Keep logs in `logs/sessions/*.md` — Cursor can read and reuse insights.

---

## 💬 3. Prompt Strategy

- [x] **Be explicit about what module to use**
  - “Use `spacing-systems.md` to assess this layout.”

- [x] **Frame prompts as action verbs**
  - Use verbs like `refactor`, `review`, `explain`, `adapt`.

- [x] **Reference patterns and reasoning principles**
  - “Explain this using the `cards` UI pattern and its reasoning principles.”

---

## 🛠️ 4. Dev CLI Support (optional enhancements)

- [ ] Create a `dev context add-cursor` command
  - Automatically inserts `// AI-Context:` headers based on selected modules.

- [ ] Export context summary for Cursor
  - Generate a `cursor-context.md` with all active module summaries.

---

## 🧪 5. Context Verification Prompts

Use these to test if Cursor is truly ingesting your context:

- [ ] “Summarize the key rules of `design/principles/spacing-systems.md`”
- [ ] “Refactor this layout using the `cards` pattern”
- [ ] “Does this follow `state-isolation` principles?”
- [ ] “Why is this approach an anti-pattern according to `modularity.md`?”

---

> Keep this file updated as your system evolves. Cursor works best when the context is both available and _activated_ through intentional use.
