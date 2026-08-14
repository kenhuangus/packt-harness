const pptxgen = require('pptxgenjs');

function createSlide(pres, theme) {
 const slide = pres.addSlide();
 slide.background = { color: theme.bg };

 slide.addText('BREAK & OPEN Q&A', {
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


 slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
 x: 0.6, y: 1.25, w: 8.8, h: 3.7,
 fill: { color: '1e293b' }, rectRadius: 0.15
 });
 slide.addText('☕ MID-MORNING BREAK & OPEN Q&A', {
 x: 0.8, y: 1.55, w: 8.4, h: 0.5,
 fontSize: 20, fontFace: 'Arial', color: '0d9488', bold: true, align: 'center'
 });
 slide.addText('Reflect on Session 1 Takeaways & Prepare for Session 2', {
 x: 0.8, y: 2.15, w: 8.4, h: 0.4,
 fontSize: 13, fontFace: 'Arial', color: '94a3b8', align: 'center'
 });

 slide.addShape(pres.shapes.RECTANGLE, {
 x: 1.8, y: 2.7, w: 6.4, h: 0.02,
 fill: { color: '0d9488' }
 });

 slide.addText('Key Discussion Points:\n1. What failure modes have you encountered in production AI agents?\n2. How are you handling file & command permissions in your org?\n3. Questions on Spec-Driven Development & Guardrail Hooks.', {
 x: 1.2, y: 2.9, w: 7.6, h: 1.8,
 fontSize: 12, fontFace: 'Arial', color: 'FFFFFF', align: 'left'
 });


 slide.addShape(pres.shapes.OVAL, {
 x: 9.2, y: 5.1, w: 0.4, h: 0.4,
 fill: { color: theme.accent }
 });
 slide.addText('7', {
 x: 9.2, y: 5.1, w: 0.4, h: 0.4,
 fontSize: 11, fontFace: 'Arial', color: 'FFFFFF', bold: true, align: 'center', valign: 'middle'
 });

 return slide;
}

module.exports = { createSlide };
