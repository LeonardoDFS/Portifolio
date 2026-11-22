import fs from 'node:fs/promises';
import { Workbook, SpreadsheetFile } from 'file:///C:/Users/Leonardo/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/@oai/artifact-tool/dist/artifact_tool.mjs';

const data = JSON.parse(await fs.readFile('tmp/gastos_data.json', 'utf8'));
const wb = Workbook.create();
const dash = wb.worksheets.add('Análise');
const source = wb.worksheets.add('Lançamentos');
const months = ['Sem mês', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro'];
const cats = ['Alimentação', 'Casa e contas', 'Transporte', 'Saúde e pets', 'Casa e compras', 'Outros / revisar'];
const end = data.length + 4;
const font = 'Arial';
const money = '"R$" #,##0.00';

source.showGridLines = false;
source.getRange('A1').values = [['Lançamentos originais e classificação']];
source.getRange('A2').values = [['Fonte: Gastos_Melhorado.xlsx; valores copiados das sete abas, sem alterar o arquivo original.']];
source.getRange('A4:F4').values = [['Mês', 'Meio', 'Descrição original', 'Valor (R$)', 'Categoria', 'Origem (aba e células)']];
source.getRange(`A5:F${end}`).values = data.map(x => [x.mes, x.tipo, x.descricao, x.valor, x.categoria, `${x.origem} ${x.celula}`]);
source.getRange(`D5:D${end}`).setNumberFormat(money);
source.getRange('A1:F2').format.font = { name: font, size: 11, color: '#1F2937' };
source.getRange('A1').format.font = { name: font, size: 15, bold: true, color: '#17324D' };
source.getRange('A4:F4').format = { fill: '#17324D', font: { name: font, size: 10, bold: true, color: '#FFFFFF' } };
source.getRange(`A5:F${end}`).format.font = { name: font, size: 10, color: '#263238' };
source.getRange('A:A').format.columnWidth = 17;
source.getRange('B:B').format.columnWidth = 14;
source.getRange('C:C').format.columnWidth = 29;
source.getRange('D:D').format.columnWidth = 16;
source.getRange('E:E').format.columnWidth = 22;
source.getRange('F:F').format.columnWidth = 38;
source.freezePanes.freezeRows(4);

dash.showGridLines = false;
dash.tabColor = '#17324D';
dash.getRange('A2').values = [['Análise dos gastos']];
dash.getRange('A3').values = [['Sete abas analisadas; a primeira não informa o mês. Valores em reais.']];
dash.getRange('A5:F5').values = [['Mês', 'Débito', 'Cartão', 'Gasto total', 'Entradas', 'Cartão (%)']];
dash.getRange('A6:A12').values = months.map(x => [x]);
for (let row = 6; row <= 12; row++) {
  dash.getRange(`B${row}`).formulas = [[`=SUMIFS(Lançamentos!$D$5:$D$${end},Lançamentos!$A$5:$A$${end},$A${row},Lançamentos!$B$5:$B$${end},"Débito")`]];
  dash.getRange(`C${row}`).formulas = [[`=SUMIFS(Lançamentos!$D$5:$D$${end},Lançamentos!$A$5:$A$${end},$A${row},Lançamentos!$B$5:$B$${end},"Cartão")`]];
  dash.getRange(`D${row}`).formulas = [[`=SUM(B${row}:C${row})`]];
  dash.getRange(`E${row}`).formulas = [[`=IF(COUNTIFS(Lançamentos!$A$5:$A$${end},$A${row},Lançamentos!$B$5:$B$${end},"Entrada")=0,"",SUMIFS(Lançamentos!$D$5:$D$${end},Lançamentos!$A$5:$A$${end},$A${row},Lançamentos!$B$5:$B$${end},"Entrada"))`]];
  dash.getRange(`F${row}`).formulas = [[`=C${row}/D${row}`]];
}
dash.getRange('A13').values = [['Total']];
for (const col of ['B','C','D','E']) dash.getRange(`${col}13`).formulas = [[`=SUM(${col}6:${col}12)`]];
dash.getRange('F13').formulas = [['=C13/D13']];

dash.getRange('A16:I16').values = [['Categoria', ...months, 'Total']];
dash.getRange('A17:A22').values = cats.map(x => [x]);
for (let row = 17; row <= 22; row++) {
  for (let col = 2; col <= 8; col++) {
    const letter = String.fromCharCode(64 + col);
    dash.getRange(`${letter}${row}`).formulas = [[`=SUMIFS(Lançamentos!$D$5:$D$${end},Lançamentos!$A$5:$A$${end},${letter}$16,Lançamentos!$E$5:$E$${end},$A${row})`]];
  }
  dash.getRange(`I${row}`).formulas = [[`=SUM(B${row}:H${row})`]];
}
dash.getRange('A23').values = [['Total']];
for (let col = 2; col <= 9; col++) {
  const letter = String.fromCharCode(64 + col);
  dash.getRange(`${letter}23`).formulas = [[`=SUM(${letter}17:${letter}22)`]];
}

dash.getRange('A26').values = [['Leitura dos dados']];
dash.getRange('A27').values = [['“Sem mês” é a aba inicial, sem período identificado.']];
dash.getRange('A28').values = [['Entradas vazias indicam ausência de registro; não permitem calcular déficit ou sobra mensal.']];
dash.getRange('A29').values = [['“Outros / revisar” reúne descrições ambíguas; altere a categoria na aba Lançamentos se souber o destino.']];
dash.getRange('A30').values = [['Alimentação inclui rótulos como Vale, Amigão, Rosani, Molinis e Mercado.']];
dash.getRange('A31').values = [['As abas não informam o ano. Os gastos podem ser compras ou parcelas lançadas no mês indicado.']];

dash.getRange('A2:I31').format.font = { name: font, size: 10, color: '#263238' };
dash.getRange('A2').format.font = { name: font, size: 15, bold: true, color: '#17324D' };
dash.getRange('A5:F5').format = { fill: '#17324D', font: { name: font, size: 10, bold: true, color: '#FFFFFF' } };
dash.getRange('A16:I16').format = { fill: '#17324D', font: { name: font, size: 10, bold: true, color: '#FFFFFF' } };
dash.getRange('A13:F13').format = { fill: '#E7EEF5', font: { name: font, size: 10, bold: true, color: '#17324D' } };
dash.getRange('A23:I23').format = { fill: '#E7EEF5', font: { name: font, size: 10, bold: true, color: '#17324D' } };
dash.getRange('A26').format.font = { name: font, size: 11, bold: true, color: '#17324D' };
dash.getRange('B6:E13').setNumberFormat(money);
dash.getRange('B17:I23').setNumberFormat(money);
dash.getRange('F6:F13').setNumberFormat('0.0%');
dash.getRange('A:A').format.columnWidth = 25;
dash.getRange('B:H').format.columnWidth = 17;
dash.getRange('I:I').format.columnWidth = 19;
dash.getRange('J:J').format.columnWidth = 3;
dash.getRange('K:U').format.columnWidth = 13;

const trend = dash.charts.add('bar', dash.getRange('A5:C12'));
trend.title = 'Gasto mensal por meio (R$)';
trend.titleTextStyle.typeface = font;
trend.titleTextStyle.fontSize = 12;
trend.legend = { position: 'top', textStyle: { typeface: font } };
trend.yAxis = { numberFormatCode: '"R$" #,##0', numberFormatSourceLinked: false, textStyle: { typeface: font } };
trend.setPosition('K5', 'U18');
trend.series.items[0].fill = '#55A7A0';
trend.series.items[1].fill = '#315D88';

const byCategory = dash.charts.add('bar', [dash.getRange('A16:A22'), dash.getRange('I16:I22')]);
byCategory.title = 'Gasto por categoria (R$)';
byCategory.titleTextStyle.typeface = font;
byCategory.titleTextStyle.fontSize = 12;
byCategory.hasLegend = false;
byCategory.yAxis = { numberFormatCode: '"R$" #,##0', numberFormatSourceLinked: false, textStyle: { typeface: font } };
byCategory.setPosition('K20', 'U33');
byCategory.series.items[0].fill = '#315D88';

wb.recalculate();
const check = await wb.inspect({ kind: 'region', sheetId: dash.sheetId, range: 'A5:I23', maxChars: 5500, tableMaxRows: 25, tableMaxCols: 9 });
console.log(check.ndjson);
const errors = await wb.inspect({ kind: 'match', searchTerm: '#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!', options: { useRegex: true, maxResults: 20 }, maxChars: 1000 });
console.log('ERRORS', errors.ndjson);
const preview = await wb.render({ sheetName: 'Análise', range: 'A1:U34', scale: 1.3, format: 'png' });
await fs.writeFile('tmp/gastos_preview.png', new Uint8Array(await preview.arrayBuffer()));
const outputPath = 'outputs/gastos/Analise_Gastos_Mensais.xlsx';
await fs.mkdir('outputs/gastos', { recursive: true });
const blob = await SpreadsheetFile.exportXlsx(wb);
await blob.save(outputPath);
console.log('SAVED', outputPath, 'CHARTS', dash.charts.items.length, 'ROWS', data.length);
