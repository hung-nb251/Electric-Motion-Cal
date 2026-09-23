from pypdf import PdfReader
from pdf2image import convert_from_path
from pathlib import Path
from PIL import Image
p=Path('outputs/bao_cao_xe_con/Bao_cao_xe_con_x2_theo_mau.pdf')
r=PdfReader(p)
for i,x in enumerate(r.pages):
    text=x.extract_text()
    print(i+1,len(text),text[:100].replace('\n',' '))
out=Path('tmp/report_build/render_x2');out.mkdir(exist_ok=True)
ims=convert_from_path(str(p),dpi=110)
for j,im in enumerate(ims):im.save(out/f'page-{j+1}.png')
for z in range(0,len(ims),4):
    sheet=Image.new('RGB',(1060,1380),'#dddddd')
    for j,im in enumerate(ims[z:z+4]):sheet.paste(im.resize((510,660)),((j%2)*530,(j//2)*690))
    sheet.save(out/f'contact-{z//4+1}.png')

