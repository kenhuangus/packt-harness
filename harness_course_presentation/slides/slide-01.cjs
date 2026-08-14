const pptxgen = require('pptxgenjs');

function createSlide(pres, theme) {
 const slide = pres.addSlide();
 slide.background = { color: '0f172a' }; // Dark sleek cover background

 // Top Category Pill
 slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
 x: 0.8, y: 0.8, w: 2.8, h: 0.35,
 fill: { color: '0d9488' }, rectRadius: 0.15
 });
 slide.addText('HANDS-ON WORKSHOP', {
 x: 0.8, y: 0.8, w: 2.8, h: 0.35,
 fontSize: 11, fontFace: 'Arial', color: 'FFFFFF', bold: true, align: 'center', valign: 'middle'
 });

 // Main Title
 slide.addText('Harness Engineering for AI Coding Agents', {
 x: 0.8, y: 1.5, w: 8.4, h: 1.4,
 fontSize: 34, fontFace: 'Arial', color: 'FFFFFF', bold: true, align: 'left', valign: 'top'
 });

 // Subtitle
 slide.addText('Building Reliable, Deterministic, and Production-Grade Agentic Workflows', {
 x: 0.8, y: 2.9, w: 8.4, h: 0.8,
 fontSize: 18, fontFace: 'Arial', color: '94a3b8', align: 'left', valign: 'top'
 });

 // Decorative Accent Bar
 slide.addShape(pres.shapes.RECTANGLE, {
 x: 0.8, y: 3.8, w: 8.4, h: 0.04,
 fill: { color: '0d9488' }
 });

 // Workshop Details Card
 slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
 x: 0.8, y: 4.1, w: 8.4, h: 1.0,
 fill: { color: '1e293b' }, rectRadius: 0.1, line: { color: '334155', width: 1 }
 });
 slide.addText('🎯 Focus: Claude Code, AGY, MCP & Safety Guardrails | 💡 Format: Theory & Code Labs', {
 x: 1.0, y: 4.2, w: 8.0, h: 0.8,
 fontSize: 13, fontFace: 'Arial', color: 'cbd5e1', align: 'left', valign: 'middle'
 });

 return slide;
}

module.exports = { createSlide };
