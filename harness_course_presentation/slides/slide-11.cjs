const pptxgen = require('pptxgenjs');

function createSlide(pres, theme) {
  const slide = pres.addSlide();
  slide.background = { color: theme.bg };

  slide.addText('PRACTICAL WORKFLOW PATTERN', {
    x: 0.6, y: 0.4, w: 6.5, h: 0.6,
    fontSize: 22, fontFace: 'Arial', color: theme.primary, bold: true, align: 'left', valign: 'middle'
  });

  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: 7.2, y: 0.45, w: 2.2, h: 0.38,
    fill: { color: theme.accent }, rectRadius: 0.15
  });
  slide.addText('11:05 AM - 11:15 AM', {
    x: 7.2, y: 0.45, w: 2.2, h: 0.38,
    fontSize: 11, fontFace: 'Arial', color: 'FFFFFF', bold: true, align: 'center', valign: 'middle'
  });

  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0.6, y: 1.05, w: 8.8, h: 0.02,
    fill: { color: 'cbd5e1' }
  });


  const steps = [
    { num: '1', title: 'Spec First', desc: 'Write clear specs & acceptance criteria.' },
    { num: '2', title: 'Constrained Exec', desc: 'Run in sandbox with minimal tool scopes.' },
    { num: '3', title: 'Deterministic Checks', desc: 'Trigger pre/post hooks & linter rules.' },
    { num: '4', title: 'Test Verification', desc: 'Run automated unit & integration tests.' },
    { num: '5', title: 'Human Review', desc: 'Final sanity check & PR merge approval.' }
  ];

  steps.forEach((s, idx) => {
    const xPos = 0.6 + (idx * 1.78);
    slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x: xPos, y: 1.5, w: 1.64, h: 3.2,
      fill: { color: 'FFFFFF' }, rectRadius: 0.1, line: { color: 'cbd5e1', width: 1 }
    });

    slide.addShape(pres.shapes.OVAL, {
      x: xPos + 0.52, y: 1.7, w: 0.6, h: 0.6,
      fill: { color: theme.accent }
    });
    slide.addText(s.num, {
      x: xPos + 0.52, y: 1.7, w: 0.6, h: 0.6,
      fontSize: 14, fontFace: 'Arial', color: 'FFFFFF', bold: true, align: 'center', valign: 'middle'
    });

    slide.addText(s.title, {
      x: xPos + 0.1, y: 2.45, w: 1.44, h: 0.6,
      fontSize: 12, fontFace: 'Arial', color: theme.primary, bold: true, align: 'center'
    });

    slide.addText(s.desc, {
      x: xPos + 0.1, y: 3.1, w: 1.44, h: 1.4,
      fontSize: 10, fontFace: 'Arial', color: '475569', align: 'center'
    });
  });


  slide.addShape(pres.shapes.OVAL, {
    x: 9.2, y: 5.1, w: 0.4, h: 0.4,
    fill: { color: theme.accent }
  });
  slide.addText('11', {
    x: 9.2, y: 5.1, w: 0.4, h: 0.4,
    fontSize: 11, fontFace: 'Arial', color: 'FFFFFF', bold: true, align: 'center', valign: 'middle'
  });

  return slide;
}

module.exports = { createSlide };
