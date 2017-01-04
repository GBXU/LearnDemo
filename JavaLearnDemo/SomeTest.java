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
    	 * 查阅资料：
    	 * 	Java中对象采用的不是引用调用，而是值传递
    	 * 	方法不能修改一个基本数据类型的参数
    	 * 	方法可以改变一个对象参数的状态
    	 * 	方法不能实现让一个对象参数引用一个新的对象
    	 */
    }
}
