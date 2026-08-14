const pptxgen = require('pptxgenjs');

function createSlide(pres, theme) {
 const slide = pres.addSlide();
 slide.background = { color: theme.bg };

 slide.addText('SKILLS, PLUGINS & MCP TOOLS', {
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


 const extComponents = [
 { title: '📦 Reusable Skills', desc: 'Standard SKILL.md format providing explicit instructions, metadata, and workflows for repeatable domain tasks.' },
 { title: '🔌 Modular Plugins', desc: 'Bundling skills, agents, hooks, and MCP servers into self-contained packages, declared in .claude-plugin/plugin.json, for easy distribution across teams.' },
 { title: '🌐 Model Context Protocol (MCP)', desc: 'Open standard protocol connecting AI agents safely to enterprise databases, internal APIs, and local services.' }
 ];

 extComponents.forEach((c, idx) => {
 const yPos = 1.25 + (idx * 1.22);
 slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
 x: 0.6, y: yPos, w: 8.8, h: 1.05,
 fill: { color: 'FFFFFF' }, rectRadius: 0.1, line: { color: 'cbd5e1', width: 1 }
 });
 slide.addText(c.title, {
 x: 0.8, y: yPos + 0.15, w: 8.4, h: 0.3,
 fontSize: 13, fontFace: 'Arial', color: theme.accent, bold: true
 });
 slide.addText(c.desc, {
 x: 0.8, y: yPos + 0.45, w: 8.4, h: 0.5,
 fontSize: 11, fontFace: 'Arial', color: theme.primary
 });
 });


 slide.addShape(pres.shapes.OVAL, {
 x: 9.2, y: 5.1, w: 0.4, h: 0.4,
 fill: { color: theme.accent }
 });
 slide.addText('9', {
 x: 9.2, y: 5.1, w: 0.4, h: 0.4,
 fontSize: 11, fontFace: 'Arial', color: 'FFFFFF', bold: true, align: 'center', valign: 'middle'
 });

 return slide;
}

module.exports = { createSlide };
