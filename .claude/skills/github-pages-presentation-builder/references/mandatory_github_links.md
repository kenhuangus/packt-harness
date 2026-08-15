# Mandatory GitHub Linking for Technical Artifacts

## 1. Principle of Actionable Technical Presentations
A technical slide deck should never display disconnected code snippets or abstract file names without direct, clickable links to the live repository. Every technical slide must empower attendees and reviewers to inspect the executable implementation and automated tests immediately.

## 2. Invariant Rules for Code Slides

Every Code Slide must include:
1. **Clickable Header File Tag**:
   ```html
   <a href="https://github.com/<org>/<repo>/blob/main/<file_path>" target="_blank" rel="noopener noreferrer" class="code-file-tag">
     📄 <file_path> ↗
   </a>
   ```
2. **Execution & Control Invariant Card**:
   ```html
   <div class="invariant-card">
     <div class="invariant-title">🛡️ Execution &amp; Control Invariant</div>
     <div style="margin-bottom:0.35rem; color:var(--ink); font-size:0.86rem;">
       Verified directly against runnable tests in GitHub:
     </div>
     <div style="display:flex; flex-direction:column; gap:0.25rem; font-size:0.84rem;">
       <div>📄 <strong>Source File:</strong> <a href="https://github.com/<org>/<repo>/blob/main/<file_path>" target="_blank" rel="noopener noreferrer"><code><file_path></code> ↗</a></div>
       <div>🧪 <strong>Test Suite:</strong> <a href="https://github.com/<org>/<repo>/tree/main/<module_path>/tests" target="_blank" rel="noopener noreferrer"><code><module_path>/tests/</code> ↗</a></div>
     </div>
   </div>
   ```

## 3. Invariant Rules for Agent Skill Slides

Every Skill Slide must include:
1. **Direct Directory Link**: Clickable link to `.claude/skills/<skill_name>/`.
2. **Direct Manifest Link**: Clickable link to `.claude/skills/<skill_name>/SKILL.md`.
3. **Progressive Disclosure Links**: Clickable links to `scripts/`, `references/`, and `assets/`.
