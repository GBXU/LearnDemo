public class SomeTest {
    public static void change(String s) {
    	s = new String("s2");
    	System.out.println("in change():" + s);
    }
    public static void main(String[] args) {
    	String s1 = new String("s1");
    	change(s1);
    	System.out.println("finally:" + s1);
    	/*
    	 * �������ϣ�
    	 * 	Java�ж�����õĲ������õ��ã�����ֵ����
    	 * 	���������޸�һ�������������͵Ĳ���
    	 * 	�������Ըı�һ�����������״̬
    	 * 	��������ʵ����һ�������������һ���µĶ���
    	 */
    }
}
