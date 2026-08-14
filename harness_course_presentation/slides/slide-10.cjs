const pptxgen = require('pptxgenjs');

function createSlide(pres, theme) {
 const slide = pres.addSlide();
 slide.background = { color: theme.bg };

 slide.addText('COMPOUND ENGINEERING & AGENT TEAMS', {
 x: 0.6, y: 0.4, w: 6.5, h: 0.6,
 fontSize: 22, fontFace: 'Arial', color: theme.primary, bold: true, align: 'left', valign: 'middle'
 });

 slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
 x: 7.2, y: 0.45, w: 2.2, h: 0.38,
 fill: { color: theme.accent }, rectRadius: 0.15
 });
 slide.addText('', {
 x: 7.2, y: 0.45, w: 2.2, h: 0.38,
 fontSize: 11, fontFace: 'Arial', color: 'FFFFFF', bold: true, align: 'center', valign: 'middle'
 });

 slide.addShape(pres.shapes.RECTANGLE, {
 x: 0.6, y: 1.05, w: 8.8, h: 0.02,
 fill: { color: 'cbd5e1' }
 });


 // Top 3 Role Cards
 const roles = [
 { title: '🧠 Planner', desc: 'Architect agent that analyzes requirements and drafts step-by-step execution plans.' },
 { title: '⚙️ Implementer', desc: 'Focused coder agent executing task under strict directory & tool boundaries.' },
 { title: '🔍 Reviewer', desc: 'Independent auditor agent evaluating code diffs, lints, and test coverage.' }
 ];

 roles.forEach((r, idx) => {
 const xPos = 0.6 + (idx * 2.98);
 slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
 x: xPos, y: 1.25, w: 2.84, h: 2.2,
 fill: { color: 'FFFFFF' }, rectRadius: 0.1, line: { color: 'cbd5e1', width: 1 }
 });
 slide.addText(r.title, {
 x: xPos + 0.15, y: 1.4, w: 2.54, h: 0.3,
 fontSize: 13, fontFace: 'Arial', color: theme.accent, bold: true
 });
 slide.addText(r.desc, {
 x: xPos + 0.15, y: 1.8, w: 2.54, h: 1.5,
 fontSize: 11, fontFace: 'Arial', color: theme.primary
 });
 });

 // Bottom Card: Self Improvement Loop
 slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
 x: 0.6, y: 3.65, w: 8.8, h: 1.3,
 fill: { color: '1e293b' }, rectRadius: 0.1
 });
 slide.addText('🔄 RECURSIVE SELF-IMPROVEMENT LOOP', {
 x: 0.8, y: 3.75, w: 8.4, h: 0.3,
 fontSize: 12, fontFace: 'Arial', color: '0d9488', bold: true
 });
 slide.addText('Capture execution traces, failure modes, and user edits automatically to update prompt rules, expand test benchmarks, and continuously refine agent behavior.', {
 x: 0.8, y: 4.05, w: 8.4, h: 0.8,
 fontSize: 11, fontFace: 'Arial', color: 'FFFFFF'
 });


 slide.addShape(pres.shapes.OVAL, {
 x: 9.2, y: 5.1, w: 0.4, h: 0.4,
 fill: { color: theme.accent }
 });
 slide.addText('10', {
 x: 9.2, y: 5.1, w: 0.4, h: 0.4,
 fontSize: 11, fontFace: 'Arial', color: 'FFFFFF', bold: true, align: 'center', valign: 'middle'
 });

 return slide;
}

module.exports = { createSlide };
