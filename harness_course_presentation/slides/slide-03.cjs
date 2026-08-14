const pptxgen = require('pptxgenjs');

function createSlide(pres, theme) {
 const slide = pres.addSlide();
 slide.background = { color: theme.bg };

 // Header Title
 slide.addText('WHY HARNESS ENGINEERING', {
 x: 0.6, y: 0.4, w: 6.5, h: 0.6,
 fontSize: 22, fontFace: 'Arial', color: theme.primary, bold: true, align: 'left', valign: 'middle'
 });

 // Timeline Badge
 slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
 x: 7.2, y: 0.45, w: 2.2, h: 0.38,
 fill: { color: theme.accent }, rectRadius: 0.15
 });
 slide.addText('', {
 x: 7.2, y: 0.45, w: 2.2, h: 0.38,
 fontSize: 11, fontFace: 'Arial', color: 'FFFFFF', bold: true, align: 'center', valign: 'middle'
 });

 // Divider Line
 slide.addShape(pres.shapes.RECTANGLE, {
 x: 0.6, y: 1.05, w: 8.8, h: 0.02,
 fill: { color: 'cbd5e1' }
 });


 // Top Card: Core Formula
 slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
 x: 0.6, y: 1.25, w: 8.8, h: 1.1,
 fill: { color: '1e293b' }, rectRadius: 0.1
 });
 slide.addText('THE CORE FORMULA: AGENT = MODEL + HARNESS', {
 x: 0.8, y: 1.35, w: 8.4, h: 0.3,
 fontSize: 12, fontFace: 'Arial', color: '0d9488', bold: true
 });
 slide.addText('Reliability does not depend on model intelligence alone. The harness provides deterministic boundaries, persistent memory, tool sandboxing, and automated evaluation.', {
 x: 0.8, y: 1.65, w: 8.4, h: 0.6,
 fontSize: 12, fontFace: 'Arial', color: 'FFFFFF'
 });

 // Card Left: The 98% Harness Rule
 slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
 x: 0.6, y: 2.5, w: 4.2, h: 2.4,
 fill: { color: 'FFFFFF' }, rectRadius: 0.1, line: { color: 'cbd5e1', width: 1 }
 });
 slide.addText('💡 The 98% Harness Rule', {
 x: 0.8, y: 2.65, w: 3.8, h: 0.3,
 fontSize: 13, fontFace: 'Arial', color: theme.primary, bold: true
 });
 slide.addText('• Models are probabilistic inference engines.\n• 98% of production reliability comes from the surrounding system scaffolding.\n• Shift focus from Prompt Engineering to System Harnessing.', {
 x: 0.8, y: 3.05, w: 3.8, h: 1.7,
 fontSize: 11, fontFace: 'Arial', color: '334155'
 });

 // Card Right: Common Failure Modes
 slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
 x: 5.2, y: 2.5, w: 4.2, h: 2.4,
 fill: { color: 'FFFFFF' }, rectRadius: 0.1, line: { color: 'cbd5e1', width: 1 }
 });
 slide.addText('⚠️ Common Agent Failure Modes', {
 x: 5.4, y: 2.65, w: 3.8, h: 0.3,
 fontSize: 13, fontFace: 'Arial', color: 'b91c1c', bold: true
 });
 slide.addText('• Context Drift & Amnesia (losing scope).\n• Infinite Loop Runaways (repeating broken edits).\n• Hallucinated Tool Calls & API parameters.\n• Unsanitized filesystem/shell mutations.', {
 x: 5.4, y: 3.05, w: 3.8, h: 1.7,
 fontSize: 11, fontFace: 'Arial', color: '334155'
 });


 // Page Number Badge
 slide.addShape(pres.shapes.OVAL, {
 x: 9.2, y: 5.1, w: 0.4, h: 0.4,
 fill: { color: theme.accent }
 });
 slide.addText('3', {
 x: 9.2, y: 5.1, w: 0.4, h: 0.4,
 fontSize: 11, fontFace: 'Arial', color: 'FFFFFF', bold: true, align: 'center', valign: 'middle'
 });

 return slide;
}

module.exports = { createSlide };
