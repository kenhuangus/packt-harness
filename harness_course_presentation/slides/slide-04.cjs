const pptxgen = require('pptxgenjs');

function createSlide(pres, theme) {
  const slide = pres.addSlide();
  slide.background = { color: theme.bg };

  // Header Title
  slide.addText('CORE HARNESS STACK & PILLARS', {
    x: 0.6, y: 0.4, w: 6.5, h: 0.6,
    fontSize: 22, fontFace: 'Arial', color: theme.primary, bold: true, align: 'left', valign: 'middle'
  });

  // Timeline Badge
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: 7.2, y: 0.45, w: 2.2, h: 0.38,
    fill: { color: theme.accent }, rectRadius: 0.15
  });
  slide.addText('09:15 AM - 09:30 AM', {
    x: 7.2, y: 0.45, w: 2.2, h: 0.38,
    fontSize: 11, fontFace: 'Arial', color: 'FFFFFF', bold: true, align: 'center', valign: 'middle'
  });

  // Divider Line
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0.6, y: 1.05, w: 8.8, h: 0.02,
    fill: { color: 'cbd5e1' }
  });


  const pillars = [
    { title: '1. Instructions & Conventions', desc: 'CLAUDE.md, AGENTS.md, & style guides specifying repo rules.' },
    { title: '2. Tools & Permissions', desc: 'Scoped API calls, terminal sandboxing, & filesystem boundaries.' },
    { title: '3. Hooks & Policy Checks', desc: 'Deterministic pre/post action filters blocking invalid mutations.' },
    { title: '4. Tests & Verification', desc: 'Automated test runners giving instant feedback on agent outputs.' },
    { title: '5. Logging & Observability', desc: 'Structured event tracing for debugging, metrics, & auditing.' }
  ];

  pillars.forEach((p, idx) => {
    const yPos = 1.25 + (idx * 0.72);
    slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x: 0.6, y: yPos, w: 8.8, h: 0.62,
      fill: { color: 'FFFFFF' }, rectRadius: 0.08, line: { color: 'cbd5e1', width: 1 }
    });
    slide.addText(p.title, {
      x: 0.8, y: yPos + 0.1, w: 3.2, h: 0.4,
      fontSize: 12, fontFace: 'Arial', color: theme.accent, bold: true
    });
    slide.addText(p.desc, {
      x: 4.0, y: yPos + 0.1, w: 5.2, h: 0.4,
      fontSize: 11, fontFace: 'Arial', color: theme.primary
    });
  });


  // Page Number Badge
  slide.addShape(pres.shapes.OVAL, {
    x: 9.2, y: 5.1, w: 0.4, h: 0.4,
    fill: { color: theme.accent }
  });
  slide.addText('4', {
    x: 9.2, y: 5.1, w: 0.4, h: 0.4,
    fontSize: 11, fontFace: 'Arial', color: 'FFFFFF', bold: true, align: 'center', valign: 'middle'
  });

  return slide;
}

module.exports = { createSlide };
