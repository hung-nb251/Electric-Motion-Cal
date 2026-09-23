import {Workbook} from '@oai/artifact-tool';
const w=Workbook.create();console.log(w.help('chart.series',{include:'index,examples,notes',search:'formula|scatter|xValues|categoryFormula',maxChars:6500}).ndjson);
