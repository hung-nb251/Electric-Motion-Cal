import fs from 'node:fs/promises';
import {FileBlob,SpreadsheetFile} from '@oai/artifact-tool';
const wb=await SpreadsheetFile.importXlsx(await FileBlob.load('Tính toán thông số động cơ.xlsx'));
const im=await wb.render({sheetName:'Tính toán chi tiết động cơ a=1',range:'A3:F24',scale:1.4});
await fs.writeFile('tmp/report_build/source_layout.png',new Uint8Array(await im.arrayBuffer()));
