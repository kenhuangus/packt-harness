const pptxgen = require('pptxgenjs');

const pres = new pptxgen();
pres.layout = 'LAYOUT_16x9';

const theme = {
  primary: '0f172a',
  secondary: '1e293b',
  accent: '0d9488',
  light: 'cbd5e1',
  bg: 'f8fafc'
};

for (let i = 1; i <= 12; i++) {
  const num = String(i).padStart(2, '0');
  const slideModule = require('./slide-' + num + '.cjs');
  slideModule.createSlide(pres, theme);
}

pres.writeFile({ fileName: './output/harness_engineering_course.pptx' })
  .then(fileName => {
    console.log('Presentation compiled successfully: ' + fileName);
  })
  .catch(err => {
    console.error('Compilation error:', err);
  });
