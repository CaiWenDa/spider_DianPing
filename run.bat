::keyword �����ؼ���
set keyword="������ѵ"
::city_id ����ID��160 Ϊ֣�ݣ��������вο� location.md �ļ�
set city_id=160
::num_pages ��ȡҳ��
set num_pages=1
::wait_range ÿ��������ʱ�䷶Χ����λ�룬�������ֱ�ʾ��С�����ֵ
set wait_range=3 6
::output_file ����ļ�·��
set output_file="dianping.csv"
python ./scratchDianPing.py --keyword %keyword% --city_id %city_id% --num_pages %num_pages% --wait_range %wait_range% --output_file %output_file%