package com.spring;
import java.util.Date;
import java.util.Locale;

import org.springframework.context.ApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;

public class LanguageChange {
	/*
	 * XML中声明MessageSource的Bean实例message
	 * properties = 基础名 message 后缀诸如_en_US等特定的Locale
	 */
	public static void main(String[] args){
		//实例化ApplicationContext
		@SuppressWarnings("resource")
		ApplicationContext ctx = new ClassPathXmlApplicationContext("applicationContext.xml");
		
		String [] a = {"读者"};
		//使用getMessage方法获得本地化信息。
		//返回计算机环境默认的Locale
		String hello = ctx.getMessage("hello", a, Locale.getDefault());
		Object[] b = { new Date() };
		String now = ctx.getMessage("now", b, Locale.getDefault());
		//将两条本地化信息打印出来
		System.out.println(hello);		
		System.out.println(now);
		
		//认为设置成英文环境
		hello = ctx.getMessage("hello", a, Locale.US);
		now = ctx.getMessage("now", b, Locale.US);
		//将两条英文信息打印出来
		System.out.println(hello);		
		System.out.println(now);
		
		//认为设置成中文环境
		hello = ctx.getMessage("hello", a, Locale.CHINA);
		now = ctx.getMessage("now", b, Locale.CHINA);
		//将两条中文信息打印出来
		System.out.println(hello);		
		System.out.println(now);

	}

}
