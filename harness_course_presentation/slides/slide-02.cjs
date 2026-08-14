const pptxgen = require('pptxgenjs');

function createSlide(pres, theme) {
 const slide = pres.addSlide();
 slide.background = { color: theme.bg };

 // Header Title
 slide.addText('WORKSHOP AGENDA & TIMETABLE', {
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


 // Left Column (Morning Sessions Part 1)
 slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
 x: 0.6, y: 1.25, w: 4.2, h: 3.7,
 fill: { color: 'FFFFFF' }, rectRadius: 0.1, line: { color: 'cbd5e1', width: 1 }
 });
 slide.addText('SESSION 1: FOUNDATIONS & GUARDRAILS', {
 x: 0.8, y: 1.35, w: 3.8, h: 0.3,
 fontSize: 12, fontFace: 'Arial', color: theme.accent, bold: true
 });
 
 const itemsLeft = [
 ' | Why Harness Engineering',
 ' | Core Harness Stack & Architecture',
 ' | Spec-Driven Development',
 ' | Guardrails & Deterministic Hooks',
 ' | Break - Open Q&A'
 ];
 itemsLeft.forEach((item, idx) => {
 slide.addText(item, {
 x: 0.8, y: 1.75 + (idx * 0.6), w: 3.8, h: 0.5,
 fontSize: 11, fontFace: 'Arial', color: theme.primary, bold: (idx === 4)
 });
 });

 // Right Column (Morning Sessions Part 2)
 slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
 x: 5.2, y: 1.25, w: 4.2, h: 3.7,
 fill: { color: 'FFFFFF' }, rectRadius: 0.1, line: { color: 'cbd5e1', width: 1 }
 });
 slide.addText('SESSION 2: ADVANCED WORKFLOWS & TEAMS', {
 x: 5.4, y: 1.35, w: 3.8, h: 0.3,
 fontSize: 12, fontFace: 'Arial', color: theme.accent, bold: true
 });

 const itemsRight = [
 ' | Tests as Reliability Layer',
 ' | Skills, Plugins, and MCP Tools',
 ' | Compound Engineering & Agent Teams',
 ' | Practical Workflow Pattern',
 ' | Closing Principles and Q&A'
 ];
 itemsRight.forEach((item, idx) => {
 slide.addText(item, {
 x: 5.4, y: 1.75 + (idx * 0.6), w: 3.8, h: 0.5,
 fontSize: 11, fontFace: 'Arial', color: theme.primary, bold: (idx === 4)
 });
 });


 // Page Number Badge
 slide.addShape(pres.shapes.OVAL, {
 x: 9.2, y: 5.1, w: 0.4, h: 0.4,
 fill: { color: theme.accent }
 });
 slide.addText('2', {
 x: 9.2, y: 5.1, w: 0.4, h: 0.4,
 fontSize: 11, fontFace: 'Arial', color: 'FFFFFF', bold: true, align: 'center', valign: 'middle'
 });

 return slide;
}

module.exports = { createSlide };
