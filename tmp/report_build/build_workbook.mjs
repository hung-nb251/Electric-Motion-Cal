import fs from 'node:fs/promises';
import path from 'node:path';
import {Workbook,SpreadsheetFile} from '@oai/artifact-tool';
const out=path.resolve('outputs/bao_cao_xe_con'), tmp=path.resolve('tmp/report_build');
const wb=Workbook.create();const s=wb.worksheets.add('Ket_qua');const inp=wb.worksheets.add('Dau_vao');
const inputs=[
 ['Tải nâng Q',12222,'kg','Đề bài'],['Khối lượng nâng hạ m_h',222,'kg','Đề bài'],['Khối lượng bổ sung m_x',0,'kg','Chưa có dữ liệu; 0 là mốc tối thiểu, phải cập nhật'],
 ['Tốc độ tối đa',.12,'m/s','Đề bài'],['Gia tốc giới hạn',.5,'m/s²','Đề bài'],['Jerk giới hạn',2,'m/s³','Đề bài'],['Chiều cao nâng',12,'m','Đề bài; không phải hành trình ngang'],
 ['Đường kính bánh D',.25,'m','SOW_HungNB.docx'],['Tỷ số truyền i',100,'','Đề xuất'],['Hiệu suất cơ khí',.96,'','SOW; kiểm tra catalog'],['Hệ số dự trữ k',1.2,'','SOW'],['Gia tốc trọng trường',9.81,'m/s²','Hằng số quy ước'],
 ['Hệ số cản chạy f_r',.01,'','Giả thiết cản lăn; xem báo cáo mục 2'],['Hệ số bám μ_b',.2,'','Giả thiết, phải kiểm tra ray thực'],['Tỷ lệ tải bánh chủ động',.5,'','Hai bánh chịu 50% tải, giả thiết'],['Quán tính phần quay J_rot',.015,'kg·m²','Ngân sách quán tính quy về motor; phải xác minh'],
 ['Công suất motor đề xuất',2.2,'kW','Đề xuất sơ bộ'],['Tốc độ danh định motor',960,'vòng/phút','Giả định để chọn 6 cực'],['Thời gian tăng/giảm tốc Ta',2,'s','Đề xuất quỹ đạo thường'],['Thời gian jerk tj',.25,'s','Đề xuất quỹ đạo thường'],['Hành trình ngang minh họa L',9,'m','Excel khóa trước; không phải chiều cao nâng'],['Thời gian nghỉ mỗi đầu',30,'s','Giả thiết chu kỳ'],['Số bánh chịu tải',4,'','Giả thiết phân bố đều'],['Hệ số phân bố tải bánh',1.25,'','Giả thiết thiết kế sơ bộ']
];
inp.getRange('A1:D1').merge();inp.getRange('A1').values=[['Thông số xe con cầu trục']];
inp.getRange('A2:D2').merge();inp.getRange('A2').values=[['Ô vàng có thể sửa. Phương án có điều kiện; đọc ghi chú trước khi thay đầu vào.']];
inp.getRange('A4:D4').values=[['Đại lượng','Giá trị','Đơn vị','Nguồn hoặc giả thiết']];inp.getRange('A5:D28').values=inputs;
inp.getRange('A30:D30').merge();inp.getRange('A30').values=[['Nguồn tham khảo và giới hạn mô hình']];
const notes=[
 'SYSTEM ARCHITECTURE – CRANE TROLLEY DRIVE SYSTEM.txt: tham khảo cấu trúc, không sao chép định mức.',
 'Tính toán thông số động cơ.xlsx: tab a=1; lực cản 0,2 chỉ để đối chiếu ở Ket_qua.',
 'SOW_HungNB.docx: D=0,25 m, η=0,96, k=1,2; không thiết kế nâng hạ.',
 'SEW Project Planning for Drives, mục 7.4 và 8: https://download.sew-eurodrive.com/download/pdf/10522913.pdf',
 'Cản lăn và hệ số bám là hai đại lượng khác nhau. Kiểm tra tải lệch, ray dốc và dây cấp điện trước khi chốt.',
 'M_RMS áp dụng quỹ đạo đối xứng với lực tại bánh còn cùng chiều chuyển động khi giảm tốc; không thay kiểm tra nhiệt catalog.',
 'Không điền khối lượng toàn xe vào m_x nếu đã chứa m_h; tránh tính trùng 222 kg.'
];
for(let j=0;j<notes.length;j++){inp.getRange(`A${31+j}:D${31+j}`).merge();inp.getRange(`A${31+j}`).values=[[notes[j]]];}
const rows=[
 [5,'Khối lượng có tải','=Dau_vao!B5+Dau_vao!B6+Dau_vao!B7','kg','Q + m_h + m_x'],
 [6,'Khối lượng không tải','=Dau_vao!B6+Dau_vao!B7','kg','m_h + m_x'],
 [7,'Bán kính bánh','=Dau_vao!B12/2','m','D / 2'],
 [8,'Tốc độ bánh','=60*Dau_vao!B8/(2*PI()*B7)','vòng/phút','Theo tốc độ ngang'],
 [9,'Tốc độ motor làm việc','=B8*Dau_vao!B13','vòng/phút','n_b × i'],
 [10,'Tốc độ góc motor','=Dau_vao!B8*Dau_vao!B13/B7','rad/s','v × i / r'],
 [11,'Lực cản lăn có tải','=Dau_vao!B17*B5*Dau_vao!B16','N','f_r × m × g'],
 [12,'Lực kéo bao trên','=B11+B5*Dau_vao!B9','N','F_c + m × a_lim'],
 [13,'Lực bám giả định','=Dau_vao!B18*Dau_vao!B19*B5*Dau_vao!B16','N','μ_b × tỷ lệ tải × m × g'],
 [14,'Hệ số dự trữ bám','=B13/B12','','Phải ≥ 1 với phân bố tải thực'],
 [15,'Mô-men bánh thiết kế','=Dau_vao!B15*B12*B7','N·m','k × F_k × r'],
 [16,'Tải bánh thiết kế','=Dau_vao!B28*B5*Dau_vao!B16/Dau_vao!B27','N','Giả thiết phân bố đều'],
 [17,'Quán tính tịnh tiến quy đổi','=B5*(B7/Dau_vao!B13)^2','kg·m²','Không cộng trùng vào mô-men có m × a'],
 [18,'Mô-men chạy đều C','=B11*B7/(Dau_vao!B14*Dau_vao!B13)','N·m','F_c × r / (η × i)'],
 [19,'Hệ số gia tốc có tải B','=B5*B7/(Dau_vao!B14*Dau_vao!B13)+Dau_vao!B20*Dau_vao!B13/B7','N·m/(m/s²)','Gồm quán tính phần quay'],
 [20,'Mô-men bao trên','=B18+B19*Dau_vao!B9','N·m','C + B × a_lim'],
 [21,'Mô-men yêu cầu có dự trữ','=Dau_vao!B15*B20','N·m','k × M_bao'],
 [22,'Công suất cơ bao trên','=B21*B10/1000','kW','Đã tính η trong mô-men'],
 [23,'Mô-men motor danh định','=Dau_vao!B21*1000/(Dau_vao!B22*2*PI()/60)','N·m','Motor đề xuất / tốc độ danh định'],
 [24,'Dự trữ mô-men motor','=B23/B21','','Phải ≥ 1; còn kiểm tra catalog'],
 [25,'Gia tốc S-curve thường','=Dau_vao!B8/(Dau_vao!B23-Dau_vao!B24)','m/s²','v / (Ta − tj)'],
 [26,'Jerk S-curve thường','=B25/Dau_vao!B24','m/s³','a_p / tj'],
 [27,'Mô-men đỉnh chạy thường','=B18+B19*B25','N·m','Chưa nhân hệ số dự trữ'],
 [28,'Quãng đường mỗi đoạn tăng/giảm','=Dau_vao!B8*Dau_vao!B23/2','m','v × Ta / 2'],
 [29,'Thời gian chạy đều','=Dau_vao!B25/Dau_vao!B8-Dau_vao!B23','s','Chỉ áp dụng nếu L đủ dài'],
 [30,'Thời gian một lượt','=B29+2*Dau_vao!B23','s','Ta + chạy đều + Ta'],
 [31,'Thời gian chu kỳ','=2*B30+2*Dau_vao!B26','s','Có tải đi, không tải về'],
 [32,'Hệ số chạy CDF','=2*B30/B31','','Tỷ lệ thời gian, không tự xác định S3/S4'],
 [33,'Mô-men đều không tải C0','=Dau_vao!B17*B6*Dau_vao!B16*B7/(Dau_vao!B14*Dau_vao!B13)','N·m','f_r × m0 × g × r / (η × i)'],
 [34,'Hệ số gia tốc không tải B0','=B6*B7/(Dau_vao!B14*Dau_vao!B13)+Dau_vao!B20*Dau_vao!B13/B7','N·m/(m/s²)','Không bỏ quán tính rotor khi không tải'],
 [35,'Tích phân a² trong một lượt','=2*B25^2*(Dau_vao!B23-4*Dau_vao!B24/3)','m²/s³','Hai đoạn tăng và giảm tốc'],
 [36,'Mô-men RMS chu kỳ','=SQRT(((B18^2+B33^2)*B30+(B19^2+B34^2)*B35)/B31)','N·m','Có điều kiện như ghi chú đầu vào'],
 [37,'Động năng có tải','=0.5*B5*Dau_vao!B8^2+0.5*Dau_vao!B20*B10^2','J','Tịnh tiến + quay'],
 [38,'Động năng không tải','=0.5*B6*Dau_vao!B8^2+0.5*Dau_vao!B20*B10^2','J','Tịnh tiến + quay'],
 [39,'Năng lượng thiết kế một dừng','=Dau_vao!B15*B37','J','Chưa chọn điện trở khi thiếu dữ liệu chopper'],
 [40,'Năng lượng dừng / chu kỳ','= (B37+B38)/B31','W','Bỏ qua cản, không dùng riêng để chọn điện trở'],
 [41,'Tăng tốc nhanh nhất từ nghỉ','=IF(Dau_vao!B8<Dau_vao!B9^2/Dau_vao!B10,2*SQRT(Dau_vao!B8/Dau_vao!B10),Dau_vao!B8/Dau_vao!B9+Dau_vao!B9/Dau_vao!B10)','s','Quỹ đạo tam giác hoặc hình thang gia tốc'],
 [42,'Đối chiếu lực theo f = 0,2','=B5*(0.2*Dau_vao!B16+Dau_vao!B9)','N','Mô hình mẫu; không dùng để chốt bánh–ray'],
 [43,'Đối chiếu công suất theo mẫu','=Dau_vao!B15*B42*Dau_vao!B8/(Dau_vao!B14*1000)','kW','Chưa gồm quán tính phần quay'],
 [44,'Dự trữ bám theo mẫu','=B13/B42','','< 1: không đạt mô hình bám giả định']
];
s.getRange('A1:D1').merge();s.getRange('A1').values=[['Tính chọn truyền động xe con 12 222 kg']];
s.getRange('A2:D2').merge();s.getRange('A2').values=[['Phương án 2,2 kW có điều kiện. Kết quả cập nhật theo tab Dau_vao.']];
s.getRange('A4:D4').values=[['Đại lượng','Kết quả','Đơn vị','Cách tính / điều kiện']];
for(const [row,label,formula,unit,note] of rows){s.getRange(`A${row}:D${row}`).values=[[label,null,unit,note]];s.getRange(`B${row}`).formulas=[[formula]];}
s.getRange('A46:D46').merge();s.getRange('A46').values=[['Kiểm tra điều kiện mô hình và đầu vào']];
const checks=[
 ['Đầu vào đầy đủ','=IF(COUNTBLANK(Dau_vao!B5:B28)>0,"THIẾU DỮ LIỆU","Đã điền")'],
 ['Quỹ đạo hợp lệ','=IF(AND(Dau_vao!B23>=2*Dau_vao!B24,Dau_vao!B24>0,B29>=0,B25<=Dau_vao!B9,B26<=Dau_vao!B10),"Đạt theo giả thiết","CẦN TÍNH LẠI")'],
 ['Công thức RMS còn áp dụng','=IF(B25<Dau_vao!B17*Dau_vao!B16,"Áp dụng","CẦN MÔ HÌNH TRUYỀN NGƯỢC")'],
 ['Mô-men motor và lực bám','=IF(AND(B24>=1,B14>=1),"Đạt theo giả thiết","CẦN CHỌN LẠI")'],
 ['Điều kiện trước chế tạo','="Cần khối lượng khung, catalog, phân bố bánh và kiểm chứng dừng thực"']
];
for(let j=0;j<checks.length;j++){let rr=47+j;s.getRange(`A${rr}`).values=[[checks[j][0]]];s.getRange(`B${rr}:D${rr}`).merge();s.getRange(`B${rr}`).formulas=[[checks[j][1]]];}
for(const sh of [s,inp]){sh.showGridLines=false;let last=sh===s?51:37;sh.getRange(`A1:D${last}`).format.font={name:'Arial',size:11};sh.getRange(`A1:D${last}`).format.verticalAlignment='center';sh.getRange(`A1:D${last}`).format.wrapText=true;sh.getRange(`A1:D${last}`).format.rowHeight=34;sh.getRange('A:A').format.columnWidth=39;sh.getRange('B:B').format.columnWidth=18;sh.getRange('C:C').format.columnWidth=19;sh.getRange('D:D').format.columnWidth=63;sh.getRange('A1:D1').format.font={name:'Arial',size:16,bold:true};sh.getRange('A1:D1').format.rowHeight=38;sh.getRange('A4:D4').format={fill:'#24445C',font:{name:'Arial',size:11,color:'#FFFFFF',bold:true}};sh.getRange('B5:B44').setNumberFormat('#,##0.0000');sh.freezePanes.freezeRows(4);}
inp.getRange('B5:B28').format.fill='#FFF2CC';inp.getRange('A30:D30').format.fill='#DCE6F1';inp.getRange('A31:D37').format.rowHeight=46;
s.getRange('B32').setNumberFormat('0.00%');s.getRange('A46:D46').format.fill='#DCE6F1';s.getRange('A47:D51').format.rowHeight=39;
for(const rr of [21,22,23,24,36])s.getRange(`A${rr}:D${rr}`).format.fill='#EAF0F5';
for(let rr=5;rr<=28;rr++)inp.getRange(`B${rr}`).dataValidation={rule:{type:'decimal',operator:'greaterThanOrEqual',formula1:[7,20,26].includes(rr)?0:0.000001}};
for(const rr of [14,18,19])inp.getRange(`B${rr}`).dataValidation={rule:{type:'decimal',operator:'between',formula1:0.000001,formula2:1}};
for(const rr of [5,6,7,11,13,22,27])inp.getRange(`B${rr}`).setNumberFormat('#,##0');
for(const rr of [5,6])s.getRange(`B${rr}`).setNumberFormat('#,##0');
for(const rr of [11,12,13,15,16,37,38,39,42])s.getRange(`B${rr}`).setNumberFormat('#,##0.00');
s.getRange('B47:D50').conditionalFormats.add('containsText',{text:'CẦN',format:{fill:'#FCE4D6',font:{color:'#9C0006',bold:true}}});
s.getRange('B47:D50').conditionalFormats.add('containsText',{text:'THIẾU',format:{fill:'#FCE4D6',font:{color:'#9C0006',bold:true}}});
wb.recalculate();
const initial=s.getRange('B22').values[0][0];inp.getRange('B7').values=[[1000]];wb.recalculate();const changed=s.getRange('B22').values[0][0];if(!(changed>initial))throw Error('Mass sensitivity did not recalculate');inp.getRange('B7').values=[[0]];wb.recalculate();
if(Math.abs(s.getRange('B36').values[0][0]-.989297081243038)>1e-6)throw Error('RMS independent check failed');
inp.getRange('B23').values=[[.3]];wb.recalculate();if(s.getRange('B48').values[0][0]!=='CẦN TÍNH LẠI')throw Error('Invalid profile not detected');inp.getRange('B23').values=[[2]];
inp.getRange('B7').clear({applyTo:'contents'});wb.recalculate();if(s.getRange('B47').values[0][0]!=='THIẾU DỮ LIỆU')throw Error('Missing input not detected');inp.getRange('B7').values=[[0]];wb.recalculate();
console.log((await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!',options:{useRegex:true,maxResults:20},summary:'Formula errors'})).ndjson);
console.log(JSON.stringify({basePower:initial,extra1000Power:changed,rms:s.getRange('B36').values}));
for(const [sheet,range,name] of [['Ket_qua','A1:D26','calc_top'],['Ket_qua','A27:D51','calc_bottom'],['Dau_vao','A1:D20','input_top'],['Dau_vao','A21:D37','input_bottom']]){const blob=await wb.render({sheetName:sheet,range,scale:1.5,format:'png'});await fs.writeFile(path.join(tmp,name+'.png'),new Uint8Array(await blob.arrayBuffer()));}
const file=await SpreadsheetFile.exportXlsx(wb);await file.save(path.join(out,'Tinh_toan_xe_con_12222kg.xlsx'));
