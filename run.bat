@echo off
::keyword �����ؼ���
set keyword="������ѵ"
::city_id ����ID��160 Ϊ֣�ݣ��������вο� location.md �ļ�
set city_id=134
::num_pages ��ȡҳ��
set num_pages=3
::wait_range ÿ��������ʱ�䷶Χ����λ�룬�������ֱ�ʾ��С�����ֵ
set wait_range=6 12
::output_file ����ļ�·��
set output_file="nanchang.csv"
::browser_type ��������ͣ�֧�� chrome �� edge
set browser_type=edge

call conda activate scratch
python ./scratchDianPing.py --keyword %keyword% --city_id %city_id% --num_pages %num_pages% --wait_range %wait_range% --output %output_file% --browser %browser_type%