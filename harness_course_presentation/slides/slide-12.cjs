const pptxgen = require('pptxgenjs');

function createSlide(pres, theme) {
 const slide = pres.addSlide();
 slide.background = { color: theme.bg };

 slide.addText('CLOSING PRINCIPLES & FINAL Q&A', {
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


 // 4 Core Principles Cards
 const principles = [
 { title: '🎯 Predictability Over Randomness', desc: 'Standardize environments, memory files, and context structures.' },
 { title: '🔍 Reduce Ambiguity', desc: 'Eliminate vague prompts by enforcing executable specs & acceptance criteria.' },
 { title: '⚡ Automate Checks', desc: 'Replace human vigilance with deterministic hooks, linters, and test suites.' },
 { title: '🛡️ Optimize for Trust', desc: 'Prioritize system safety, auditability, and correctness over raw speed.' }
 ];

 principles.forEach((p, idx) => {
 const xPos = (idx % 2 === 0) ? 0.6 : 5.2;
 const yPos = (idx < 2) ? 1.25 : 2.75;

 slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
 x: xPos, y: yPos, w: 4.2, h: 1.35,
 fill: { color: 'FFFFFF' }, rectRadius: 0.1, line: { color: 'cbd5e1', width: 1 }
 });
 slide.addText(p.title, {
 x: xPos + 0.2, y: yPos + 0.15, w: 3.8, h: 0.35,
 fontSize: 12, fontFace: 'Arial', color: theme.accent, bold: true
 });
 slide.addText(p.desc, {
 x: xPos + 0.2, y: yPos + 0.5, w: 3.8, h: 0.7,
 fontSize: 11, fontFace: 'Arial', color: theme.primary
 });
 });

 // Bottom Q&A Card
 slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
 x: 0.6, y: 4.25, w: 8.8, h: 0.7,
 fill: { color: '1e293b' }, rectRadius: 0.1
 });
 slide.addText('💬 Thank You! Open Q&A & Discussion', {
 x: 0.8, y: 4.25, w: 8.4, h: 0.7,
 fontSize: 14, fontFace: 'Arial', color: 'FFFFFF', bold: true, align: 'center', valign: 'middle'
 });


 slide.addShape(pres.shapes.OVAL, {
 x: 9.2, y: 5.1, w: 0.4, h: 0.4,
 fill: { color: theme.accent }
 });
 slide.addText('12', {
 x: 9.2, y: 5.1, w: 0.4, h: 0.4,
 fontSize: 11, fontFace: 'Arial', color: 'FFFFFF', bold: true, align: 'center', valign: 'middle'
 });

 return slide;
}

module.exports = { createSlide };
