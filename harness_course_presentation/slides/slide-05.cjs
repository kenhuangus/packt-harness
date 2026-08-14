const pptxgen = require('pptxgenjs');

function createSlide(pres, theme) {
 const slide = pres.addSlide();
 slide.background = { color: theme.bg };

 slide.addText('SPEC-DRIVEN DEVELOPMENT', {
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
 x: 0.6, y: 1.25, w: 4.2, h: 3.7,
 fill: { color: 'FFFFFF' }, rectRadius: 0.1, line: { color: 'cbd5e1', width: 1 }
 });
 slide.addText('📋 Executable Specifications', {
 x: 0.8, y: 1.45, w: 3.8, h: 0.3,
 fontSize: 13, fontFace: 'Arial', color: theme.accent, bold: true
 });
 slide.addText('• Convert ambiguous user requests into formal SPEC.md files.\n• Define strict functional boundaries, schemas, and non-goals.\n• Prevent agent hallucination by providing unambiguous targets.', {
 x: 0.8, y: 1.95, w: 3.8, h: 2.8,
 fontSize: 11, fontFace: 'Arial', color: theme.primary
 });

 slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
 x: 5.2, y: 1.25, w: 4.2, h: 3.7,
 fill: { color: 'FFFFFF' }, rectRadius: 0.1, line: { color: 'cbd5e1', width: 1 }
 });
 slide.addText('🎯 Guiding Claude Code Behavior', {
 x: 5.4, y: 1.45, w: 3.8, h: 0.3,
 fontSize: 13, fontFace: 'Arial', color: theme.accent, bold: true
 });
 slide.addText('• Embed acceptance criteria directly in prompt context.\n• Agents validate feature completeness against spec benchmarks.\n• Drastically reduces iterations & off-target refactoring.', {
 x: 5.4, y: 1.95, w: 3.8, h: 2.8,
 fontSize: 11, fontFace: 'Arial', color: theme.primary
 });


 slide.addShape(pres.shapes.OVAL, {
 x: 9.2, y: 5.1, w: 0.4, h: 0.4,
 fill: { color: theme.accent }
 });
 slide.addText('5', {
 x: 9.2, y: 5.1, w: 0.4, h: 0.4,
 fontSize: 11, fontFace: 'Arial', color: 'FFFFFF', bold: true, align: 'center', valign: 'middle'
 });

 return slide;
}

module.exports = { createSlide };
