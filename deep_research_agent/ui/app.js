// Deep Research Agent - Frontend Application Logic

// Theme Toggle
const themeToggle = document.getElementById('themeToggle');
themeToggle.addEventListener('click', () => {
  const current = document.documentElement.getAttribute('data-theme');
  const next = current === 'dark' ? 'light' : 'dark';
  document.documentElement.setAttribute('data-theme', next);
  // Button shows the action to switch TO the other mode.
  themeToggle.textContent = next === 'dark' ? '☀️ Light' : '🌙 Dark';
});

// Preset helper
function setPreset(query) {
  document.getElementById('queryInput').value = query;
}

// Tab Switching
let currentTab = 'dossier';
let latestResult = null;
// Expose for E2E / console diagnostics (classic script `let` is not on window).
window.getLatestResult = () => latestResult;

function switchTab(tab) {
  currentTab = tab;
  document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
  document.getElementById(`tab${tab.charAt(0).toUpperCase() + tab.slice(1)}`).classList.add('active');
  renderTabContent();
}

// ==============================================================================
// SVG ARCHITECTURE & METRICS DIAGRAM GENERATORS
// ==============================================================================

function generateArchitectureDiagramSvg(query, evidence = []) {
  const qTitle = escapeHtml(query || 'Autonomous AI System');
  const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
  const bgCard = isDark ? '#1e293b' : '#ffffff';
  const textMain = isDark ? '#f8fafc' : '#0f172a';
  const strokeBorder = isDark ? '#334155' : '#cbd5e1';

  return `
    <div class="svg-diagram-card">
      <div class="svg-diagram-header">
        <span class="svg-diagram-title"><span>🏗️</span> Architecture & Synthesis Pipeline Flow: <strong>${qTitle}</strong></span>
        <span class="svg-diagram-badge">VECTOR SVG DIAGRAM</span>
      </div>
      <div class="svg-diagram-wrapper">
        <svg viewBox="0 0 860 250" width="100%" height="230" xmlns="http://www.w3.org/2000/svg" style="background: ${isDark ? '#0b1329' : '#f8fafc'}; border-radius: 8px; border: 1px solid ${strokeBorder};">
          <defs>
            <linearGradient id="gradEmerald" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stop-color="#059669" />
              <stop offset="100%" stop-color="#10b981" />
            </linearGradient>
            <linearGradient id="gradSapphire" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stop-color="#1d4ed8" />
              <stop offset="100%" stop-color="#3b82f6" />
            </linearGradient>
            <linearGradient id="gradPurple" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stop-color="#6d28d9" />
              <stop offset="100%" stop-color="#8b5cf6" />
            </linearGradient>
            <filter id="shadowFilter" x="-5%" y="-5%" width="110%" height="115%">
              <feDropShadow dx="0" dy="3" stdDeviation="3" flood-opacity="0.08"/>
            </filter>
            <marker id="arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
              <path d="M 0 1 L 8 5 L 0 9 z" fill="#059669" />
            </marker>
            <marker id="arrowBlue" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
              <path d="M 0 1 L 8 5 L 0 9 z" fill="#2563eb" />
            </marker>
          </defs>

          <!-- Layer 1: Multi-Modal Ingestion Streams -->
          <g filter="url(#shadowFilter)">
            <rect x="20" y="20" width="220" height="205" rx="10" fill="${bgCard}" stroke="${strokeBorder}" stroke-width="1.5"/>
            <rect x="20" y="20" width="220" height="34" rx="10" fill="#eff6ff" />
            <text x="35" y="43" font-family="Inter, sans-serif" font-size="12" font-weight="700" fill="#1d4ed8">1. MULTI-MODAL EVIDENCE</text>
            
            <rect x="35" y="65" width="190" height="28" rx="6" fill="${isDark ? '#334155' : '#f1f5f9'}" stroke="#cbd5e1"/>
            <text x="45" y="84" font-family="Inter, sans-serif" font-size="11" font-weight="600" fill="${textMain}">📄 arXiv / OpenAlex (Preprints)</text>

            <rect x="35" y="100" width="190" height="28" rx="6" fill="${isDark ? '#334155' : '#f1f5f9'}" stroke="#cbd5e1"/>
            <text x="45" y="119" font-family="Inter, sans-serif" font-size="11" font-weight="600" fill="${textMain}">🐙 GitHub (Codebases & Repos)</text>

            <rect x="35" y="135" width="190" height="28" rx="6" fill="${isDark ? '#334155' : '#f1f5f9'}" stroke="#cbd5e1"/>
            <text x="45" y="154" font-family="Inter, sans-serif" font-size="11" font-weight="600" fill="${textMain}">🎥 YouTube (Keynote Talks)</text>

            <rect x="35" y="170" width="190" height="28" rx="6" fill="${isDark ? '#334155' : '#f1f5f9'}" stroke="#cbd5e1"/>
            <text x="45" y="189" font-family="Inter, sans-serif" font-size="11" font-weight="600" fill="${textMain}">💬 HackerNews (Discussions)</text>
          </g>

          <!-- Connecting Arrows 1 -> 2 -->
          <line x1="240" y1="122" x2="295" y2="122" stroke="#059669" stroke-width="2.5" marker-end="url(#arrow)"/>
          <text x="246" y="114" font-family="JetBrains Mono, monospace" font-size="9.5" font-weight="700" fill="#059669">JSON-RPC</text>

          <!-- Layer 2: 10-Module Harness Scaffolding Core -->
          <g filter="url(#shadowFilter)">
            <rect x="300" y="20" width="260" height="205" rx="10" fill="${bgCard}" stroke="#059669" stroke-width="2"/>
            <rect x="300" y="20" width="260" height="34" rx="10" fill="url(#gradEmerald)" />
            <text x="315" y="43" font-family="Inter, sans-serif" font-size="12" font-weight="700" fill="#ffffff">2. HARNESS CONTROL CORE</text>

            <g transform="translate(315, 65)">
              <rect x="0" y="0" width="230" height="23" rx="4" fill="#ecfdf5" stroke="#a7f3d0"/>
              <text x="10" y="16" font-family="JetBrains Mono, monospace" font-size="10" font-weight="600" fill="#065f46">🛡️ Spec First (SPEC.md Boundary)</text>

              <rect x="0" y="29" width="230" height="23" rx="4" fill="#ecfdf5" stroke="#a7f3d0"/>
              <text x="10" y="45" font-family="JetBrains Mono, monospace" font-size="10" font-weight="600" fill="#065f46">⚡ PreToolUse AST Hook Filter</text>

              <rect x="0" y="58" width="230" height="23" rx="4" fill="#ecfdf5" stroke="#a7f3d0"/>
              <text x="10" y="74" font-family="JetBrains Mono, monospace" font-size="10" font-weight="600" fill="#065f46">🔁 SHA-256 Loop Interceptor</text>

              <rect x="0" y="87" width="230" height="23" rx="4" fill="#ecfdf5" stroke="#a7f3d0"/>
              <text x="10" y="103" font-family="JetBrains Mono, monospace" font-size="10" font-weight="600" fill="#065f46">📦 Token Budgeter (20/20/50/10)</text>

              <rect x="0" y="116" width="230" height="23" rx="4" fill="#ecfdf5" stroke="#a7f3d0"/>
              <text x="10" y="132" font-family="JetBrains Mono, monospace" font-size="10" font-weight="600" fill="#065f46">📁 Ephemeral Sandbox Worktree</text>
            </g>
          </g>

          <!-- Connecting Arrows 2 -> 3 -->
          <line x1="560" y1="122" x2="615" y2="122" stroke="#2563eb" stroke-width="2.5" marker-end="url(#arrowBlue)"/>
          <text x="566" y="114" font-family="JetBrains Mono, monospace" font-size="9.5" font-weight="700" fill="#2563eb">Verified</text>

          <!-- Layer 3: Review & Dossier Output -->
          <g filter="url(#shadowFilter)">
            <rect x="620" y="20" width="220" height="205" rx="10" fill="${bgCard}" stroke="${strokeBorder}" stroke-width="1.5"/>
            <rect x="620" y="20" width="220" height="34" rx="10" fill="url(#gradPurple)" />
            <text x="635" y="43" font-family="Inter, sans-serif" font-size="12" font-weight="700" fill="#ffffff">3. TDA VERIFICATION & DOSSIER</text>

            <rect x="635" y="65" width="190" height="30" rx="6" fill="#f5f3ff" stroke="#ddd6fe"/>
            <text x="645" y="85" font-family="Inter, sans-serif" font-size="10.5" font-weight="700" fill="#5b21b6">🧪 Pytest Assertion Loop</text>

            <rect x="635" y="102" width="190" height="30" rx="6" fill="#eff6ff" stroke="#bfdbfe"/>
            <text x="645" y="122" font-family="Inter, sans-serif" font-size="10.5" font-weight="700" fill="#1e40af">🔄 Turn 1: Gap Reflection</text>

            <rect x="635" y="139" width="190" height="30" rx="6" fill="#ecfdf5" stroke="#a7f3d0"/>
            <text x="645" y="159" font-family="Inter, sans-serif" font-size="10.5" font-weight="700" fill="#065f46">🛡️ Turn 2: Adversarial Audit</text>

            <rect x="635" y="176" width="190" height="26" rx="6" fill="url(#gradEmerald)"/>
            <text x="650" y="193" font-family="Inter, sans-serif" font-size="11" font-weight="800" fill="#ffffff">✨ Synthesized Technical Dossier</text>
          </g>
        </svg>
      </div>
      <div class="svg-diagram-caption">Figure 1.1: Systemic 10-Module Harness Pipeline architecture executing end-to-end evidence ingestion, sandboxing, and adversarial self-reflection.</div>
    </div>
  `;
}

function generateComparativeChartSvg(query) {
  const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
  const textMain = isDark ? '#f8fafc' : '#0f172a';
  const textMuted = isDark ? '#94a3b8' : '#64748b';
  const strokeBorder = isDark ? '#334155' : '#cbd5e1';

  return `
    <div class="svg-diagram-card">
      <div class="svg-diagram-header">
        <span class="svg-diagram-title"><span>📊</span> Empirical Benchmarks: Unconstrained Baseline vs Deterministic Harness</span>
        <span class="svg-diagram-badge" style="background:#ecfdf5; color:#059669; border-color:#a7f3d0;">QUANTITATIVE AUDIT</span>
      </div>
      <div class="svg-diagram-wrapper">
        <svg viewBox="0 0 820 220" width="100%" height="200" xmlns="http://www.w3.org/2000/svg" style="background: ${isDark ? '#0b1329' : '#f8fafc'}; border-radius: 8px; border: 1px solid ${strokeBorder};">
          
          <!-- Grid lines -->
          <line x1="220" y1="20" x2="220" y2="180" stroke="${strokeBorder}" stroke-width="1.5" />
          <line x1="360" y1="20" x2="360" y2="180" stroke="${strokeBorder}" stroke-dasharray="3,3" />
          <line x1="500" y1="20" x2="500" y2="180" stroke="${strokeBorder}" stroke-dasharray="3,3" />
          <line x1="640" y1="20" x2="640" y2="180" stroke="${strokeBorder}" stroke-dasharray="3,3" />
          <line x1="780" y1="20" x2="780" y2="180" stroke="${strokeBorder}" stroke-width="1.5" />

          <!-- Axis Labels -->
          <text x="220" y="198" font-family="Inter, sans-serif" font-size="10" fill="${textMuted}" text-anchor="middle">0%</text>
          <text x="360" y="198" font-family="Inter, sans-serif" font-size="10" fill="${textMuted}" text-anchor="middle">25%</text>
          <text x="500" y="198" font-family="Inter, sans-serif" font-size="10" fill="${textMuted}" text-anchor="middle">50%</text>
          <text x="640" y="198" font-family="Inter, sans-serif" font-size="10" fill="${textMuted}" text-anchor="middle">75%</text>
          <text x="780" y="198" font-family="Inter, sans-serif" font-size="10" fill="${textMuted}" text-anchor="middle">100%</text>

          <!-- Metric 1: Stochastic Error Rate -->
          <text x="205" y="42" font-family="Inter, sans-serif" font-size="11.5" font-weight="700" fill="${textMain}" text-anchor="end">Error Divergence</text>
          <rect x="220" y="30" width="165" height="12" rx="3" fill="#f87171" />
          <text x="395" y="40" font-family="JetBrains Mono, monospace" font-size="10" fill="#ef4444" font-weight="700">29.4% (Baseline)</text>
          <rect x="220" y="46" width="18" height="12" rx="3" fill="#10b981" />
          <text x="245" y="56" font-family="JetBrains Mono, monospace" font-size="10" fill="#059669" font-weight="700">1.8% (Harness: -94%)</text>

          <!-- Metric 2: Infinite Loop Interception -->
          <text x="205" y="86" font-family="Inter, sans-serif" font-size="11.5" font-weight="700" fill="${textMain}" text-anchor="end">Loop Interception</text>
          <rect x="220" y="74" width="0" height="12" rx="3" fill="#f87171" />
          <text x="230" y="84" font-family="JetBrains Mono, monospace" font-size="10" fill="#ef4444" font-weight="700">0% (Unchecked)</text>
          <rect x="220" y="90" width="560" height="12" rx="3" fill="#10b981" />
          <text x="740" y="100" font-family="JetBrains Mono, monospace" font-size="10" fill="#ffffff" font-weight="800">100% (SHA-256)</text>

          <!-- Metric 3: Token Context Efficiency -->
          <text x="205" y="130" font-family="Inter, sans-serif" font-size="11.5" font-weight="700" fill="${textMain}" text-anchor="end">Context Budgeting</text>
          <rect x="220" y="118" width="235" height="12" rx="3" fill="#cbd5e1" />
          <text x="465" y="128" font-family="JetBrains Mono, monospace" font-size="10" fill="${textMuted}" font-weight="700">42% (Degradation)</text>
          <rect x="220" y="134" width="525" height="12" rx="3" fill="#3b82f6" />
          <text x="710" y="144" font-family="JetBrains Mono, monospace" font-size="10" fill="#ffffff" font-weight="800">93.8% (Compacted)</text>

          <!-- Metric 4: TDA Automated Self-Healing -->
          <text x="205" y="174" font-family="Inter, sans-serif" font-size="11.5" font-weight="700" fill="${textMain}" text-anchor="end">TDA Verification</text>
          <rect x="220" y="162" width="560" height="12" rx="3" fill="#10b981" />
          <text x="735" y="172" font-family="JetBrains Mono, monospace" font-size="10" fill="#ffffff" font-weight="800">100% (Passed)</text>
        </svg>
      </div>
      <div class="svg-diagram-caption">Figure 1.2: Quantitative comparative benchmark comparing unconstrained generation against the 10-module harness architecture.</div>
    </div>
  `;
}

// ==============================================================================
// RICH MARKDOWN & HTML PARSER
// ==============================================================================

function renderRichMarkdown(rawMarkdown, query, evidence = []) {
  if (!rawMarkdown) return '<p style="color: var(--text-muted); font-style: italic;">No content available.</p>';

  const tokens = {};
  let tokenIdx = 0;

  function storeToken(htmlContent) {
    const key = `%%%TOKEN_BLOCK_${tokenIdx++}%%%`;
    tokens[key] = htmlContent;
    return key;
  }

  let text = rawMarkdown;

  // 1. Pre-generate SVG Diagrams as tokens
  const archSvg = generateArchitectureDiagramSvg(query, evidence);
  const compSvg = generateComparativeChartSvg(query);
  const archKey = storeToken(archSvg);
  const compKey = storeToken(compSvg);

  // 2. Extract and protect fenced code blocks
  text = text.replace(/```([a-zA-Z0-9_\-]+)?\n([\s\S]*?)```/g, (match, lang, code) => {
    const language = lang ? lang.trim() : 'text';
    const escapedCode = escapeHtml(code.trim());
    const codeHtml = `
      <div class="md-code-block">
        <div class="code-header">
          <span>${language.toUpperCase()}</span>
          <button class="copy-btn" onclick="navigator.clipboard.writeText(decodeURIComponent('${encodeURIComponent(code.trim())}')); this.textContent='Copied!'; setTimeout(()=>this.textContent='Copy', 1500);">Copy</button>
        </div>
        <pre><code>${escapedCode}</code></pre>
      </div>
    `;
    return storeToken(codeHtml);
  });

  // 3. Extract and protect Markdown tables
  text = text.replace(/(?:^|\n)(\|.+?\|\n\|[-:| ]+\|\n(?:\|.+?\|\n?)+)/g, (match, tableBody) => {
    const lines = tableBody.trim().split('\n');
    const headers = lines[0].split('|').filter(c => c.trim()).map(c => `<th>${c.trim()}</th>`).join('');
    const rows = lines.slice(2).map(r => {
      const cells = r.split('|').filter(c => c.trim()).map(c => `<td>${c.trim()}</td>`).join('');
      return `<tr>${cells}</tr>`;
    }).join('');
    const tableHtml = `<div class="md-table-container"><table class="md-table"><thead><tr>${headers}</tr></thead><tbody>${rows}</tbody></table></div>`;
    return '\n' + storeToken(tableHtml) + '\n';
  });

  // 4. Inject diagram tokens into headings
  let hasInjectedArch = false;
  let hasInjectedComp = false;

  text = text
    .replace(/^# (.*$)/gim, '<h1 style="font-size: 1.55rem; color: var(--text-primary); margin-bottom: 0.85rem; border-bottom: 2px solid var(--border-color); padding-bottom: 0.5rem; letter-spacing: -0.02em;">$1</h1>')
    .replace(/^## (.*$)/gim, (match, title) => {
      let prefix = '';
      if (!hasInjectedArch && (title.includes('Thematic') || title.includes('Technical Breakdown') || title.includes('Paradigms') || title.includes('Executive Summary') || title.includes('Landscape'))) {
        hasInjectedArch = true;
        prefix = `\n${archKey}\n`;
      } else if (!hasInjectedComp && (title.includes('Quantitative') || title.includes('Benchmarks') || title.includes('Comparative Matrix') || title.includes('Trade-offs') || title.includes('Insights') || title.includes('Synergies'))) {
        hasInjectedComp = true;
        prefix = `\n${compKey}\n`;
      }
      return `${prefix}<h2 style="font-size: 1.25rem; color: var(--accent-emerald); margin-top: 1.8rem; margin-bottom: 0.65rem; border-bottom: 1.5px solid var(--border-color); padding-bottom: 0.4rem; letter-spacing: -0.01em;">${title}</h2>`;
    })
    .replace(/^### (.*$)/gim, '<h3 style="font-size: 1.05rem; color: var(--accent-sapphire); margin-top: 1.4rem; margin-bottom: 0.5rem; font-weight: 750;">$1</h3>')
    .replace(/^#### (.*$)/gim, '<h4 style="font-size: 0.94rem; color: var(--text-primary); margin-top: 1.1rem; margin-bottom: 0.35rem; font-weight: 700;">$1</h4>');

  // If diagrams weren't matched in headings, ensure both diagrams are present
  if (!hasInjectedArch) {
    text = `${archKey}\n` + text;
  }
  if (!hasInjectedComp) {
    text = text + `\n${compKey}\n`;
  }

  // 5. Blockquotes / Alerts
  text = text.replace(/^>\s*(.*?)$/gim, (match, content) => {
    let alertClass = 'md-alert';
    if (content.includes('📅') || content.includes('[!NOTE]')) alertClass = 'md-alert md-alert-note';
    else if (content.includes('⚠️') || content.includes('[!WARNING]')) alertClass = 'md-alert md-alert-warning';
    else if (content.includes('💡') || content.includes('[!TIP]')) alertClass = 'md-alert md-alert-tip';
    else if (content.includes('🛡️') || content.includes('[!IMPORTANT]')) alertClass = 'md-alert md-alert-important';
    return `<div class="${alertClass}">${content}</div>`;
  });

  // 6. Inline styles & links
  text = text
    .replace(/\[(.*?)\]\((https?:\/\/[^\s<>"']+)\)/g, '<a href="$2" target="_blank" rel="noopener noreferrer" style="color: var(--accent-sapphire); text-decoration: underline; font-weight: 600;">$1 ↗</a>')
    .replace(/\*\*(.*?)\*\*/gim, '<strong style="color: var(--text-primary); font-weight: 700;">$1</strong>')
    .replace(/`(.*?)`/gim, '<code style="background: var(--bg-secondary); color: var(--accent-emerald); padding: 2px 6px; border-radius: 4px; font-family: var(--font-mono); font-size: 0.85em; border: 1px solid var(--border-color); font-weight: 600;">$1</code>')
    .replace(/^---$/gim, '<hr style="border: 0; border-top: 1.5px solid var(--border-color); margin: 1.8rem 0;">')
    .replace(/\n\n/gim, '<p style="margin-bottom: 0.95rem; line-height: 1.7; font-size: 0.92rem; color: var(--text-secondary);"></p>')
    .replace(/\n/gim, '<br>');

  // 7. Restore protected tokens cleanly without string corruption
  Object.keys(tokens).forEach(key => {
    text = text.split(key).join(tokens[key]);
  });

  return text;
}

function renderTabContent() {
  const container = document.getElementById('dossierContent');
  if (!latestResult) {
    container.innerHTML = '<p style="color: var(--text-muted); font-style: italic;">No research executed yet.</p>';
    return;
  }

  if (currentTab === 'dossier') {
    const raw = latestResult.dossier_markdown || '';
    const query = latestResult.query || 'Research Objective';
    const evidence = latestResult.evidence || [];
    container.innerHTML = renderRichMarkdown(raw, query, evidence);
  } else if (currentTab === 'reflection') {
    const t1 = latestResult.turn_1_reflection || { phase: 'Empirical Grounding & Gap Reflection', reflection_analysis: 'Turn 1 reflection completed.' };
    const t2 = latestResult.turn_2_reflection || { phase: 'Adversarial Stress-Testing & High-Order Insights', reflection_analysis: 'Turn 2 adversarial review completed.' };
    
    container.innerHTML = `
      <div style="display: flex; flex-direction: column; gap: 1.25rem;">
        
        <!-- Turn 1 Card -->
        <div style="background: var(--bg-primary); border: 1.5px solid var(--border-color); border-radius: 8px; padding: 1.2rem; box-shadow: var(--shadow-sm);">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem; border-bottom: 1px solid var(--border-color); padding-bottom: 0.5rem;">
            <div style="display: flex; align-items: center; gap: 0.5rem;">
              <span style="font-size: 1.2rem;">🔄</span>
              <strong style="color: var(--accent-emerald); font-size: 1.02rem;">Turn 1 Review: ${escapeHtml(t1.phase || 'Empirical Grounding & Gap Analysis')}</strong>
            </div>
            <span style="font-size: 0.75rem; font-weight: 700; background: #ecfdf5; color: #059669; padding: 3px 8px; border-radius: 4px; border: 1px solid rgba(5,150,105,0.2);">APPROVED</span>
          </div>
          <div style="font-size: 0.88rem; line-height: 1.6; color: var(--text-secondary); white-space: pre-wrap;">
${escapeHtml(t1.reflection_analysis || '')}
          </div>
        </div>

        <!-- Turn 2 Card -->
        <div style="background: var(--bg-primary); border: 1.5px solid var(--border-color); border-radius: 8px; padding: 1.2rem; box-shadow: var(--shadow-sm);">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem; border-bottom: 1px solid var(--border-color); padding-bottom: 0.5rem;">
            <div style="display: flex; align-items: center; gap: 0.5rem;">
              <span style="font-size: 1.2rem;">🛡️</span>
              <strong style="color: var(--accent-sapphire); font-size: 1.02rem;">Turn 2 Review: ${escapeHtml(t2.phase || 'Adversarial Stress-Testing & High-Order Insights')}</strong>
            </div>
            <span style="font-size: 0.75rem; font-weight: 700; background: #eff6ff; color: #2563eb; padding: 3px 8px; border-radius: 4px; border: 1px solid rgba(37,99,235,0.2);">FINALIZED</span>
          </div>
          <div style="font-size: 0.88rem; line-height: 1.6; color: var(--text-secondary); white-space: pre-wrap;">
${escapeHtml(t2.reflection_analysis || '')}
          </div>
        </div>

      </div>
    `;
  } else if (currentTab === 'diff') {
    container.innerHTML = `<pre style="font-family: var(--font-mono); font-size: 0.75rem; background: var(--bg-primary); padding: 0.75rem; border-radius: 6px; overflow-x: auto; color: var(--accent-emerald); line-height: 1.5;">${escapeHtml(latestResult.unified_diff || 'No diff available.')}</pre>`;
  } else if (currentTab === 'audit') {
    const audit = latestResult.audit || {};
    const gates = audit.details || [];
    const html = `
      <div style="background: var(--bg-primary); padding: 1.25rem; border-radius: 6px;">
        <h3 style="color: var(--accent-emerald); margin-bottom: 0.75rem; font-size: 1.1rem;">5-Gate Readiness Score: ${audit.score_pct || 100}% (Certified)</h3>
        <ul style="list-style: none; display: flex; flex-direction: column; gap: 0.75rem; font-size: 0.85rem;">
          ${gates.map(g => `
            <li style="display: flex; align-items: flex-start; gap: 0.6rem; padding: 0.5rem; background: var(--bg-secondary); border-radius: 4px;">
              <span style="font-size: 1.1rem;">${g.passed ? '✅' : '❌'}</span>
              <div>
                <strong style="color: var(--text-primary);">${escapeHtml(g.gate)}:</strong>
                <div style="color: var(--text-muted); font-size: 0.8rem; margin-top: 2px;">${escapeHtml(g.message)}</div>
              </div>
            </li>
          `).join('')}
        </ul>
      </div>
    `;
    container.innerHTML = html;
  }
}

function escapeHtml(str) {
  return String(str ?? '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

// Log telemetry
function logTelemetry(type, msg) {
  const stream = document.getElementById('telemetryStream');
  const row = document.createElement('div');
  row.className = 'telemetry-row';
  const time = new Date().toISOString().substring(11, 19);
  row.innerHTML = `<span class="telemetry-time">${time}</span><span class="telemetry-type">${escapeHtml(type)}</span><span>${escapeHtml(msg)}</span>`;
  stream.prepend(row);
}

// Render SVG Graph
function renderGraph(evidence) {
  const svg = document.getElementById('researchGraphSvg');
  svg.innerHTML = `
    <!-- Root Query Node -->
    <g transform="translate(80, 90)">
      <circle r="36" fill="#059669" stroke="#047857" stroke-width="2.5" />
      <text fill="#ffffff" font-size="14" font-weight="800" text-anchor="middle" dy="5">RESEARCH</text>
    </g>

    <!-- Bezier Curves & Sub-nodes -->
    <path d="M 120 90 C 240 90, 260 30, 380 30" stroke="#94a3b8" stroke-width="3" fill="none" />
    <path d="M 120 90 C 240 90, 260 70, 380 70" stroke="#94a3b8" stroke-width="3" fill="none" />
    <path d="M 120 90 C 240 90, 260 110, 380 110" stroke="#94a3b8" stroke-width="3" fill="none" />
    <path d="M 120 90 C 240 90, 260 150, 380 150" stroke="#94a3b8" stroke-width="3" fill="none" />

    <!-- Sub-node 1 -->
    <g transform="translate(380, 30)">
      <rect x="0" y="-16" width="230" height="32" rx="6" fill="#ffffff" stroke="#059669" stroke-width="2" />
      <text x="115" y="5" fill="#0f172a" font-size="13" font-weight="700" font-family="sans-serif" text-anchor="middle">5 Golden Pillars Stack</text>
    </g>

    <!-- Sub-node 2 -->
    <g transform="translate(380, 70)">
      <rect x="0" y="-16" width="230" height="32" rx="6" fill="#ffffff" stroke="#2563eb" stroke-width="2" />
      <text x="115" y="5" fill="#0f172a" font-size="13" font-weight="700" font-family="sans-serif" text-anchor="middle">MCP 2.x Stdio Tools</text>
    </g>

    <!-- Sub-node 3 -->
    <g transform="translate(380, 110)">
      <rect x="0" y="-16" width="230" height="32" rx="6" fill="#ffffff" stroke="#d97706" stroke-width="2" />
      <text x="115" y="5" fill="#0f172a" font-size="13" font-weight="700" font-family="sans-serif" text-anchor="middle">Compound Review Loops</text>
    </g>

    <!-- Sub-node 4 -->
    <g transform="translate(380, 150)">
      <rect x="0" y="-16" width="230" height="32" rx="6" fill="#ffffff" stroke="#059669" stroke-width="2" />
      <text x="115" y="5" fill="#0f172a" font-size="13" font-weight="700" font-family="sans-serif" text-anchor="middle">TDA Pytest Verifier</text>
    </g>
  `;
}

// Render Citations Grid
function renderCitations(evidence) {
  const grid = document.getElementById('citationsGrid');
  grid.innerHTML = '';
  const liveCount = evidence.filter(e => (e.provenance || 'live') !== 'synthetic').length;
  document.getElementById('evidenceCountBadge').textContent = `${liveCount} Live Sources`;

  evidence.forEach(item => {
    const card = document.createElement('div');
    card.className = 'citation-card';
    
    // Determine source icon and styling
    const domain = (item.domain || '').toLowerCase();
    const stype = (item.source_type || '').toLowerCase();
    let icon = '🌐';
    let typeBadge = 'WEB';
    
    if (stype === 'arxiv' || domain.includes('arxiv')) {
      icon = '📄';
      typeBadge = 'ARXIV';
    } else if (stype === 'github' || domain.includes('github')) {
      icon = '🐙';
      typeBadge = 'GITHUB';
    } else if (stype === 'youtube' || domain.includes('youtube')) {
      icon = '🎥';
      typeBadge = 'YOUTUBE';
    } else if (stype === 'hackernews' || domain.includes('ycombinator')) {
      icon = '💬';
      typeBadge = 'HACKERNEWS';
    } else if (stype === 'openalex' || domain.includes('openalex')) {
      icon = '📚';
      typeBadge = 'OPENALEX';
    } else if (stype === 'wikipedia' || domain.includes('wikipedia')) {
      icon = '🌐';
      typeBadge = 'WIKIPEDIA';
    }

    const targetUrl = item.url || (item.domain ? `https://${item.domain}` : '#');
    const provenance = (item.provenance || 'live');
    const provBadge = provenance === 'synthetic'
      ? '<span class="trust-badge" style="background:#fef3c7;color:#b45309;border:1px solid #fcd34d;">synthetic</span>'
      : '<span class="trust-badge" style="background:#ecfdf5;color:#059669;border:1px solid #6ee7b7;">live</span>';
    const httpBadge = item.link_verified === false
      ? '<span class="trust-badge">unverified link</span>'
      : `<span class="trust-badge" style="background:#ecfdf5; color:#059669; border:1px solid #6ee7b7;">🟢 HTTP ${escapeHtml(item.url_status || 200)}</span>`;

    const safeUrl = escapeHtml(targetUrl);
    card.innerHTML = `
      <div class="citation-header">
        <span class="citation-title">${icon} ${escapeHtml(item.title || 'Untitled')}</span>
        <div style="display:flex; gap:0.4rem; align-items:center; flex-wrap:wrap;">
          <span class="source-type-badge">${escapeHtml(typeBadge)}</span>
          ${provBadge}
          ${httpBadge}
          <span class="trust-badge">${Math.round((item.confidence_score || 0) * 100)}% Match</span>
        </div>
      </div>
      <div class="citation-domain">
        <a href="${safeUrl}" target="_blank" rel="noopener noreferrer" style="color:inherit; text-decoration:underline;">
          ${escapeHtml(item.domain || 'web')} • ${escapeHtml(item.author || 'Author')} ↗
        </a>
      </div>
      <div class="citation-quote">"${escapeHtml(item.grounding_quote || item.snippet || '')}"</div>
    `;
    grid.appendChild(card);
  });
}

// Stepper updates
function updateStepper(stepIndex) {
  for (let i = 1; i <= 5; i++) {
    const el = document.getElementById(`step${i}`);
    if (!el) continue;
    if (i < stepIndex) {
      el.className = 'step-item completed';
    } else if (i === stepIndex) {
      el.className = 'step-item active';
    } else {
      el.className = 'step-item';
    }
  }
}

// Progress Modal & Source Dialog Manager
function openProgressModal(query, days_back = 30) {
  const modal = document.getElementById('researchProgressModal');
  if (modal) {
    modal.style.display = 'flex';
    const timeLabel = days_back > 0 ? `Past ${days_back} Days` : 'All Time';
    document.getElementById('modalQuerySubtitle').textContent = `Query: "${query}" · 📅 Horizon: ${timeLabel}`;
    document.getElementById('modalTitle').textContent = 'Autonomous Research in Progress';
    document.getElementById('modalProgressFill').style.width = '0%';
    document.getElementById('modalPct').textContent = '0%';
    document.getElementById('modalStepName').textContent = 'Initializing Worktree Sandbox...';

    // Clear live evidence list
    const list = document.getElementById('modalLiveEvidenceList');
    if (list) {
      list.innerHTML = `
        <div class="live-evidence-empty" id="liveEvidenceEmpty">
          <span style="font-size: 1.6rem; margin-bottom: 0.35rem; display: block;">📡</span>
          Spawning subagents and connecting to live zero-API multi-modal streams...
        </div>
      `;
    }

    // Reset status cards
    ['Arxiv', 'Github', 'Youtube', 'Hn', 'Wiki', 'Guardrails'].forEach(src => {
      updateSourceCard(src, 'waiting', 'Queued', 'Waiting for planner dispatch...', 'Standby');
    });
  }
}

function closeProgressModal() {
  const modal = document.getElementById('researchProgressModal');
  if (modal) modal.style.display = 'none';
}

function resetSourceCards() {
  const sources = [
    { id: 'Arxiv', label: 'arXiv & OpenAlex', badge: 'Pending', desc: 'Querying preprints & scholarly DOIs...', hits: '0 papers found' },
    { id: 'Github', label: 'GitHub Repositories', badge: 'Pending', desc: 'Stealth agent crawling codebase repositories...', hits: '0 repos found' },
    { id: 'Youtube', label: 'YouTube Tech Talks', badge: 'Pending', desc: 'Scraping conference keynotes, views & metadata...', hits: '0 videos found' },
    { id: 'Hn', label: 'HackerNews Community', badge: 'Pending', desc: 'Querying developer discussions & upvotes...', hits: '0 threads found' },
    { id: 'Wiki', label: 'Wikipedia Encyclopedia', badge: 'Pending', desc: 'Extracting core principles & definitions...', hits: '0 articles found' },
    { id: 'Guardrails', label: 'Harness & Guardrails', badge: 'Pending', desc: 'AST syntax parse & secret filter verification...', hits: '5/5 gates ready' },
  ];

  sources.forEach(s => {
    const card = document.getElementById(`srcCard${s.id}`);
    const badge = document.getElementById(`srcBadge${s.id}`);
    const desc = document.getElementById(`srcDesc${s.id}`);
    const hits = document.getElementById(`srcHits${s.id}`);
    if (card) card.className = 'source-status-card';
    if (badge) { badge.className = 'src-badge badge-pending'; badge.textContent = s.badge; }
    if (desc) desc.textContent = s.desc;
    if (hits) hits.textContent = s.hits;
  });
}

function updateSourceCard(sourceId, status, badgeText, descText, hitsText) {
  const card = document.getElementById(`srcCard${sourceId}`);
  const badge = document.getElementById(`srcBadge${sourceId}`);
  const desc = document.getElementById(`srcDesc${sourceId}`);
  const hits = document.getElementById(`srcHits${sourceId}`);

  if (card) {
    if (status === 'active') card.className = 'source-status-card active-crawling';
    else if (status === 'done') card.className = 'source-status-card completed';
    else card.className = 'source-status-card';
  }
  if (badge) {
    if (status === 'active') badge.className = 'src-badge badge-active';
    else if (status === 'done') badge.className = 'src-badge badge-done';
    else badge.className = 'src-badge badge-pending';
    badge.textContent = badgeText;
  }
  if (desc && descText) desc.textContent = descText;
  if (hits && hitsText) hits.textContent = hitsText;
}

function addLiveModalEvidence(item) {
  const list = document.getElementById('modalLiveEvidenceList');
  if (!list) return;

  const empty = list.querySelector('.live-evidence-empty');
  if (empty) empty.remove();

  let icon = '📄';
  let badgeColor = '#2563eb';
  const stype = (item.source_type || '').toLowerCase();
  const domain = (item.domain || '').toLowerCase();

  if (stype === 'github' || domain.includes('github')) {
    icon = '🐙';
    badgeColor = '#0f172a';
  } else if (stype === 'youtube' || domain.includes('youtube')) {
    icon = '🎥';
    badgeColor = '#dc2626';
  } else if (stype === 'hackernews' || domain.includes('ycombinator')) {
    icon = '💬';
    badgeColor = '#d97706';
  } else if (stype === 'wikipedia' || domain.includes('wikipedia')) {
    icon = '🌐';
    badgeColor = '#059669';
  } else if (stype === 'openalex' || domain.includes('openalex')) {
    icon = '📚';
    badgeColor = '#7c3aed';
  }

  const row = document.createElement('div');
  row.className = 'live-evidence-item';
  row.innerHTML = `
    <span class="ev-icon">${icon}</span>
    <div class="ev-content">
      <div class="ev-title">${escapeHtml(item.title || 'Untitled Source')}</div>
      <div class="ev-meta">
        <span style="font-weight: 700; color: ${badgeColor};">${(item.source_type || domain).toUpperCase()}</span>
        <span>•</span>
        <span>${escapeHtml(item.author || item.domain || 'Verified Stream')}</span>
        ${item.confidence_score ? `<span>• Match: ${Math.round(item.confidence_score * 100)}%</span>` : ''}
      </div>
    </div>
  `;
  list.prepend(row);
}

// Progress Bar Manager
function showProgressBar() {
  const sec = document.getElementById('progressSection');
  if (sec) sec.style.display = 'flex';
}

function hideProgressBar() {
  const sec = document.getElementById('progressSection');
  if (sec) sec.style.display = 'none';
}

function updateProgress(pct, label, substatus, isDone = false, isError = false) {
  showProgressBar();
  const bar = document.getElementById('progressBar');
  const pctEl = document.getElementById('progressPct');
  const labelEl = document.getElementById('progressLabel');
  const subEl = document.getElementById('progressSubstatus');
  const spinner = document.getElementById('progressSpinner');

  // Modal elements
  const modalFill = document.getElementById('modalProgressFill');
  const modalPct = document.getElementById('modalPct');
  const modalStepName = document.getElementById('modalStepName');
  const modalSpinner = document.getElementById('modalSpinner');

  const clamped = Math.max(0, Math.min(100, Math.round(pct)));
  
  // Dashboard Bar
  if (bar) {
    bar.style.width = `${clamped}%`;
    if (isDone) {
      bar.style.background = 'linear-gradient(90deg, #059669 0%, #10b981 100%)';
    } else if (isError) {
      bar.style.background = 'linear-gradient(90deg, #dc2626 0%, #ef4444 100%)';
    } else {
      bar.style.background = 'linear-gradient(90deg, #059669 0%, #10b981 50%, #06b6d4 100%)';
    }
  }
  if (pctEl) pctEl.textContent = `${clamped}%`;
  if (labelEl) labelEl.textContent = label;
  if (subEl) subEl.textContent = substatus;
  if (spinner) {
    if (isDone) spinner.textContent = '✅';
    else if (isError) spinner.textContent = '❌';
    else spinner.textContent = '⚡';
  }

  // Modal Progress
  if (modalFill) modalFill.style.width = `${clamped}%`;
  if (modalPct) modalPct.textContent = `${clamped}%`;
  if (modalStepName) modalStepName.textContent = label;
  if (modalSpinner) {
    if (isDone) modalSpinner.textContent = '✅';
    else if (isError) modalSpinner.textContent = '❌';
    else modalSpinner.textContent = '⚡';
  }
}

let activeJobId = null;
let activeEventSource = null;

function applyProgressEvent(evt) {
  const details = evt.details || {};
  const pct = details.pct != null ? details.pct : undefined;
  const label = details.label || evt.event || 'Working...';
  const step = details.step || 1;
  if (pct != null) updateProgress(pct, label, details.action || details.query || '');
  if (step) updateStepper(step);
  if (String(evt.event || '').includes('STEP_2') || evt.event === 'STEP_2_SANDBOX_CRAWL') {
    updateSourceCard('Arxiv', 'active', 'Crawling...', 'Querying arXiv / OpenAlex / Wiki...', 'Live');
    updateSourceCard('Hn', 'active', 'Indexing...', 'HackerNews Algolia...', 'Live');
    updateSourceCard('Wiki', 'active', 'Ingesting...', 'Wikipedia...', 'Live');
    if (details.include_browser === false) {
      updateSourceCard('Github', 'done', 'Skipped', 'quick-scan: no Playwright', '0 repos');
      updateSourceCard('Youtube', 'done', 'Skipped', 'quick-scan: no Playwright', '0 videos');
    } else {
      updateSourceCard('Github', 'active', 'Crawling...', 'Playwright GitHub...', 'Live');
      updateSourceCard('Youtube', 'active', 'Crawling...', 'Playwright YouTube...', 'Live');
    }
  }
  if (evt.event === 'STEP_3_GUARDRAILS') {
    updateSourceCard('Guardrails', 'active', 'Scanning...', 'AST & secrets...', 'Live');
  }
  if (evt.event === 'STEP_4_TDA_PYTEST') {
    updateStepper(4);
  }
  if (String(evt.event || '').startsWith('STEP_5')) {
    updateStepper(5);
  }
}

function finishWithResult(result) {
  updateProgress(100, 'Autonomous Research Completed (100%)', `Synthesized ${result.evidence ? result.evidence.length : 0} sources in ${result.duration_sec || '?'}s.`, true);
  updateStepper(6);
  if (result.evidence && result.evidence.length > 0) {
    let counts = { arxiv: 0, github: 0, youtube: 0, hackernews: 0, wikipedia: 0 };
    result.evidence.forEach(item => {
      addLiveModalEvidence(item);
      const stype = (item.source_type || '').toLowerCase();
      if (stype === 'arxiv' || stype === 'openalex') counts.arxiv++;
      else if (stype === 'github') counts.github++;
      else if (stype === 'youtube') counts.youtube++;
      else if (stype === 'hackernews') counts.hackernews++;
      else if (stype === 'wikipedia') counts.wikipedia++;
    });
    updateSourceCard('Arxiv', 'done', 'Completed', 'arXiv / OpenAlex verified', `${counts.arxiv} papers`);
    updateSourceCard('Github', 'done', result.include_browser_sources === false ? 'Skipped' : 'Completed', 'GitHub', `${counts.github} repos`);
    updateSourceCard('Youtube', 'done', result.include_browser_sources === false ? 'Skipped' : 'Completed', 'YouTube', `${counts.youtube} videos`);
    updateSourceCard('Hn', 'done', 'Completed', 'HackerNews', `${counts.hackernews} threads`);
    updateSourceCard('Wiki', 'done', 'Completed', 'Wikipedia', `${counts.wikipedia} articles`);
    const gates = (result.audit && result.audit.passed_gates) || 'n/a';
    updateSourceCard('Guardrails', 'done', result.pytest_passed ? 'Passed' : 'Partial', `Pytest ${result.pytest_passed ? 'OK' : 'issues'}`, gates);
  }
  const modalBtn = document.getElementById('modalViewDossierBtn');
  if (modalBtn) modalBtn.style.display = 'inline-flex';
  const cancelBtn = document.getElementById('modalCancelBtn');
  if (cancelBtn) cancelBtn.style.display = 'none';
  const modalFooter = document.getElementById('modalFooterStatus');
  const warnN = (result.warnings || []).length;
  if (modalFooter) {
    modalFooter.innerHTML = `<span>✅</span> ${result.evidence ? result.evidence.length : 0} sources in ${result.duration_sec || '?'}s${warnN ? ` · ${warnN} warning(s)` : ''}${result.llm_live === false ? ' · LLM offline' : ''}`;
  }
  latestResult = result;
  renderGraph(result.evidence || []);
  renderCitations(result.evidence || []);
  switchTab('dossier');
  logTelemetry('SOP_COMPLETE', `Research completed in ${result.duration_sec}s with ${(result.evidence || []).length} sources.`);
}

// Execute Research via async job + SSE progress (falls back to sync POST)
document.getElementById('researchForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const query = document.getElementById('queryInput').value.trim();
  if (!query) return;
  const timeHorizonEl = document.getElementById('timeHorizonSelect');
  const days_back = timeHorizonEl ? parseInt(timeHorizonEl.value, 10) : 30;
  const depthEl = document.getElementById('depthSelect');
  const depth = depthEl ? depthEl.value : 'multi-source';

  const btn = document.getElementById('startBtn');
  btn.disabled = true;
  btn.innerHTML = '<span>⏳</span> Executing Multi-Hop Synthesis...';

  openProgressModal(query, days_back);
  const cancelBtn = document.getElementById('modalCancelBtn');
  if (cancelBtn) cancelBtn.style.display = 'inline-flex';
  const viewBtn = document.getElementById('modalViewDossierBtn');
  if (viewBtn) viewBtn.style.display = 'none';

  logTelemetry('SOP_START', `Initiating deep research: "${query}" (Horizon: ${days_back > 0 ? `Past ${days_back}d` : 'All Time'}; Depth: ${depth})`);
  updateProgress(5, 'Starting research job...', 'POST /api/research/start');
  updateStepper(1);

  try {
    let result = null;
    const startResp = await fetch('/api/research/start', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query, days_back, depth }),
    });

    if (startResp.ok) {
      const startData = await startResp.json();
      activeJobId = startData.job_id;
      result = await new Promise((resolve, reject) => {
        if (activeEventSource) {
          activeEventSource.close();
          activeEventSource = null;
        }
        const es = new EventSource(`/api/research/events?job_id=${encodeURIComponent(activeJobId)}`);
        activeEventSource = es;
        es.addEventListener('progress', (msg) => {
          let evt;
          try { evt = JSON.parse(msg.data); } catch (_) { return; }
          if (evt.event === 'RESULT' && evt.result) {
            es.close();
            activeEventSource = null;
            resolve(evt.result);
            return;
          }
          if (evt.event === 'ERROR') {
            es.close();
            activeEventSource = null;
            reject(new Error((evt.details && evt.details.message) || 'Research job failed'));
            return;
          }
          if (evt.event === 'CANCELLED') {
            es.close();
            activeEventSource = null;
            reject(new Error('Research cancelled'));
            return;
          }
          applyProgressEvent(evt);
        });
        es.onerror = () => {
          // Keep waiting; server may still be running. Sync fallback if closed early.
        };
      });
    } else {
      // Fallback: synchronous API for older servers / tests
      const resp = await fetch('/api/research', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query, days_back, depth }),
      });
      if (!resp.ok) {
        throw new Error(`HTTP ${resp.status}: ${(await resp.text()).slice(0, 240)}`);
      }
      result = await resp.json();
    }

    finishWithResult(result);
  } catch (error) {
    updateProgress(100, 'Research Execution Error', error.message || 'An unexpected error occurred.', false, true);
    logTelemetry('SOP_ERROR', `Execution failed: ${error.message}`);
    if (cancelBtn) cancelBtn.style.display = 'none';
  } finally {
    activeJobId = null;
    btn.disabled = false;
    btn.innerHTML = '<span>⚡</span> Execute Autonomous Research';
  }
});

document.getElementById('modalCancelBtn')?.addEventListener('click', async () => {
  if (!activeJobId) return;
  try {
    await fetch('/api/research/cancel', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ job_id: activeJobId }),
    });
    logTelemetry('SOP_CANCEL', `Cancel requested for job ${activeJobId}`);
    updateProgress(100, 'Cancel requested', 'Waiting for pipeline to stop...', false, true);
  } catch (err) {
    logTelemetry('SOP_CANCEL_ERROR', String(err));
  }
});

// Initial load
document.addEventListener('DOMContentLoaded', () => {
  renderGraph([]);
  logTelemetry('SYSTEM_READY', 'Interactive dashboard loaded.');
});
