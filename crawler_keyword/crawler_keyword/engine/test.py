# -*- coding: utf-8 -*
from sentence_splitter import SentenceSplitter, split_text_into_sentences
import re
splitter = SentenceSplitter(language='en')
def list_contains(List1, List2): 
  
    set1 = set(List1) 
    set2 = set(List2) 
    if set1.intersection(set2): 
        return True 
    else: 
        return False

txt = "Phiên giao dịch ngày 19/5, các chỉ số biến động mạnh khi áp lực bán tăng cao về cuối phiên. Nhiều cổ phiếu vốn hoá lớn như BID, VCB, MSN, VHM, VRE… đều thu hẹp nhịp tăng của phiên sáng.Đối với khối ngoại, nhóm này tiếp tục bán ròng gần 77 tỷ đồng, giảm 30,7% so với phiên trước. Nhà đầu tư nước ngoại mua vào 44,2 triệu cổ phiếu, trị giá 2.073 tỷ đồng; trong khi bán ra 45 triệu đơn vị với giá trị tương ứng hơn 2.150 tỷ đồng. Trên HoSE, dòng vốn ngoại tiếp tục bán ròng khoảng 96 tỷ đồng, tăng 7% so với phiên trước. Xét về lượng mua vào và bán ra thì giá trị đều gấp đôi với phiên trước, đạt 2.011 tỷ đồng và 2.107 tỷ đồng. Nguyên nhân đến từ việc giao dịch thoả thuận 14 triệu cổ phiếu VIC với mức giá 96.500 đồng/cp.VRE bị bán ròng 5 phiên liên tiếp VRE với tổng giá trị hơn 290 tỷ đồng. Nhóm cổ phiếu ngành thép là HPG và NKG bị rút vốn 31,4 tỷ đồng và 14,7 tỷ đồng.Ngược lại, CCQ E1VFVN30 được mua vào mạnh nhất với 26,1 tỷ đồng. CTG được mua trở lại 24 tỷ đồng; VPB và VCB được mua ròng phiên thứ 8. CCQ VFMVN Diamond được mua ròng phiên thứ 5 với giá trị đạt 20 tỷ đồng.Tại HNX, nhà đầu tư nước ngoài chấm dứt chuỗi bán ròng kể từ 17/2 khi mua vào gần 600 triệu đồng. 2 cổ phiếu được mua ròng trên 1 tỷ là VCS, NTP.Ở chiều ngược lại, PVS, TIG bị bán ròng trở lại với 1,6 tỷ đồng và 940 triệu đồng. BVS bị bán ròng 23 phiên liên tiếp với tổng giá trị hơn 13 tỷ đồng.Trên UPCoM, nhóm này mua ròng trở lại hơn 18,5 tỷ đồng. VTP, VEA được mua ròng mạnh nhất với 1 tỷ đồng và 770 tỷ đồng. Trong khi đó, ACV bị bán ròng 12 phiên với tổng giá trị 127 tỷ đồng."
x = txt.replace(',',' ')
#print(x)

#x = txt.split(".")
#for i in x:
#    print(i)
y = splitter.split(text=x)
print(y)
items = ['VCB', 'BID', 'VIC']

#for i in y:

#    print(type(i))
#    for item in items:
#        if item in i:
#            print('thuộc items')
#        else:
#            print('ko items')
#    res = [ele for ele in items if(ele in i)]
#    if res == []:
#        print("thuộc item")
#    else:
#        print("ko thu")

doclist = [i for i in y]
docstr = ' ' . join(doclist)
# print(docstr)
