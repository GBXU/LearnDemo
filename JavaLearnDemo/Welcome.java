import java.io.*;
import java.math.BigDecimal;
import java.math.BigInteger;
import java.util.*;

/**
* <p>Title: Welcome</p>
* <p>Description: NULL</p>
* <p>Company: SCU</p> 
* @author xgb99
* @date 2016年7月10日下午2:39:58
*/
public class Welcome {
	public static void main(String[] args) throws Exception {
//		chapter2Variables();
//		chapter3CurrTime();
//		chapter4string();
//		chapter5	loop...
//		chapter6	overload...
//		chapter7Array();
//		chapter8MultiArray();
//		chapter9Class();
//		chapter10Object();
//		chapter11 封装 继承 多态 动态绑定 向上转换 向下转换（显式）public protected default private final
//		chapter12Error();
//		chapter12IO();
//		chapter13 抽象类 接口
//		chapter14 JAVAFX
//		chapter15 事件驱动 动画
//		chapter16 UI 多媒体
//		chapter17 二进制 IO
		
	}
	public static void chapter12IO() throws Exception{
		File source = new File("source.txt");
		if (!source.exists()) {
			System.out.println("source file don't exists");
			System.exit(1);
		}
		File target = new File("target.txt");
		if (target.exists()) {
			System.out.println("target file already exists");
			System.exit(1);
		}
		
		try (
			Scanner input = new Scanner(source);
			PrintWriter output = new PrintWriter(target);
		) {
			output.println("Java learning");
			while(input.hasNext()) {
				String str = input.nextLine();
				output.println(str);
			}
		}
	}
	public static void chapter12Error() {
		try{
			Scanner input = new Scanner(System.in);
			int negative = input.nextInt();
			if (negative <= 0) {
				chapter12Test(negative);
				System.exit(1);
			}
			else{
				System.out.println(negative + " is negative");
			}
		}
		catch(negativeEx ex){
			//错误被catch，这部分执行
			//ex.printStackTrace();
			System.out.print("\n" + ex.getMessage());
			//System.out.print("\n" + ex.toString());
		}
		finally {
			System.out.print("\n" + "end0");//无论怎样，这部分都执行
		}
		System.out.print("\n" + "end1");//错误被catch或者没有错，这部分执行
	}
	public static void chapter12Test(int num )throws negativeEx {
		negativeEx ex = new negativeEx(num);
		throw ex;
	}	
	public static void chapter10Object() {
		//基本数据类型 和 包装类类型 可以自动转换
		Integer int0 = new Integer(1);
		Double	double0 = new Double(1.0);
		Boolean bool0 = new Boolean(true);
		Character char0 = new Character('a');
		Float float0 = new Float(1.0);
		Byte byte0 = new Byte("11");
		Short short0 = new Short("123");
		Long long0 = new Long("12345");
		//
		BigInteger a = new BigInteger("1234665989");
		BigDecimal b = new BigDecimal(1.2);
		//替换
		String str0 = new String("hello");
		String str1 = str0.replace('o', 'A');
		String str2 = str1.replaceFirst("l", "L");
		System.out.println(str2);
		// \\d意思是单个数字位，{3}是三个数字位
		if("440-02-4534".matches("\\d{3}-\\d{2}-\\d{4}")) {
			System.out.println("\\d{3} matched");			
		}
		if("JAVA00sdad12".matches("JAVA.*")) {
			System.out.println("JAVA.* matched");					
		}
		// [$+#]意思是能够匹配$或+或#，replaceAll因此全部符合的都换了
		System.out.println("a+b$#c".replaceAll("[$+#]", "NNN"));
		//把字符串按照Regex切割
		String[] tokens = "Java,C?C#,C++".split("[,?]");
		System.out.println(tokens[1]);
		//转化
		char[] dst = "SCJava".toCharArray();
		"CS3720".getChars(0, 2, dst, 0);
		String dstDst = new String(dst);
		System.out.println(dstDst);
		//格式
		String number = String.valueOf(5.44);
		System.out.println(String.format("%7.2f%d%-4s%d", 45.54,123,"ABC",1));
		
		//StringBuffer StringBuilder 能string对象进行更改
	}
	public static void chapter9Class() {
		SimpleCircle tmp = new SimpleCircle(1.0);
		//只能有一个public class，此处即Welcome
		System.out.println(tmp.getArea());
		SimpleCircle.classFunc();
		tmp = null;// 引用变量tmp的对象会被虚拟机收回
	}
	public static void chapter8MultiArray() {
		char[][] str = {
				{'a','b','c'},
				{'a','b'},
				{'a'}
				};
		System.out.println(str[0]);
		char[][] str1 = new char[3][];
		str1[0] = new char[3];
		str1[1] = new char[2];
		str1[2] = new char[1];
	}
	public static void chapter7Array() {
		Double[] arrayTmp0 = {1.2,1.1,1.3};
		ArrayList<Double> arrayObject = new ArrayList<>(Arrays.asList(arrayTmp0));
		arrayObject.add(1.4);
		java.util.Collections.sort(arrayObject);//max min  sort shuffle
		System.out.println(arrayObject);
		Double[] arrayTmp1 = new Double[4];
		arrayObject.toArray(arrayTmp1);
		//
		int[] arr0 = new int[5];
		for(int i = 0;i<5;i++){
			arr0[i] = i;
		}
		int[] arr1 = new int[5];
		System.arraycopy(arr0, 0 , arr1, 0, 5);
		System.out.println(arr1[0]);
		char[] arr2 = {'h','e','l','l','o'};
		System.out.println(arr2);
		java.util.Arrays.sort(arr2);
		System.out.println(arr2);
		//paralleSort(arr2,0,2);binarySearch(arr2,'e');
		//equals(arr1,arr2);fill(arr2,'A')
		
		//function(int[] arr);
	}
	public static void chapter4string() {
		String s1 = "hello";
		System.out.println(s1.charAt(s1.length()-1));
		System.out.println(s1.concat("worl")+'d');
		System.out.println(s1.toUpperCase());
		
		System.out.print("请输入“hello”:");
		Scanner input = new Scanner(System.in);
		String s2 = input.nextLine();
		input.close();
		//== String只能判断是否指向同一个对象 例如“hello”
		if(s2.equals(s1) || s2.equalsIgnoreCase(s1)){
			System.out.println("忽略大小写，字符串一样");
		}
		if (s2.compareTo(s1)>0 || s2.compareToIgnoreCase(s1)>0) {
			System.out.println("字典顺序,s2更前");
		}
		if("Welcome to Java".endsWith("va")){
			System.out.println("以va结尾");//startWith
		}
		if("Welcome to Java".contains("com")){
			System.out.println("含有com");
		}
		//lastIndexOf
		System.out.println("welcome".indexOf('c'));
		//字符串到数的转化
		System.out.println(Double.parseDouble("123.1"));
	}
	public static void chapter3CurrTime() {
		long totalMilliseconds = System.currentTimeMillis();
		long totalSeconds = totalMilliseconds / 1000;
		long currentSecond = totalSeconds % 60;
		long totalMinutes = totalSeconds / 60;
		long currentMinute = totalMinutes % 60;
		long totalHours = totalMinutes / 60;
		long currentHour = totalHours % 24;//GMT 
		System.out.println("Beijing Time:" + (currentHour+8) + ":"
				+ currentMinute + ":"
				+ currentSecond);
	}
	public static void chapter2Variables(){
		/**
		 * classes are always UpperUpper
		 * methods,variables are always lower case or lowerUpper
		 * constant variables are UPPER
		 */
		double radius,area;
		final int VALUE = 2016;//常量
		System.out.print(VALUE + " input:");
		Scanner input = new Scanner(System.in);
		radius = input.nextDouble();
		input.close();
		area = radius * radius * Math.PI;//Math.random()
		System.out.println("the area of " + radius 
				+ " is " + area);		
	}
}
class negativeEx extends Exception{
	private int num;
	public negativeEx(int num) {
		super("illegalArgument is " + num);
		this.num = num;
	}
}
class SimpleCircle {
	static int circleNum = 0;//类共享的
	SimpleCircle() {
		radius = 1;
	}
	SimpleCircle(double newRadius) {
		radius = newRadius;
	}
	//因为是public方法 包外的类里才能调用
	public double getArea() {
		return radius * radius * Math.PI;
	}
	//静态函数才能直接用类来调用
	public static void classFunc(){
		System.out.println("SimpleCircle.classFunct");
	}
	private double radius;//类变量顺序不一定要在调用前
}