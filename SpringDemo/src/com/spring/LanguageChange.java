package com.spring;
import java.util.Date;
import java.util.Locale;

import org.springframework.context.ApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;

public class LanguageChange {
	/*
	 * XML������MessageSource��Beanʵ��message
	 * properties = ������ message ��׺����_en_US���ض���Locale
	 */
	public static void main(String[] args){
		//ʵ����ApplicationContext
		@SuppressWarnings("resource")
		ApplicationContext ctx = new ClassPathXmlApplicationContext("applicationContext.xml");
		
		String [] a = {"����"};
		//ʹ��getMessage������ñ��ػ���Ϣ��
		//���ؼ��������Ĭ�ϵ�Locale
		String hello = ctx.getMessage("hello", a, Locale.getDefault());
		Object[] b = { new Date() };
		String now = ctx.getMessage("now", b, Locale.getDefault());
		//���������ػ���Ϣ��ӡ����
		System.out.println(hello);		
		System.out.println(now);
		
		//��Ϊ���ó�Ӣ�Ļ���
		hello = ctx.getMessage("hello", a, Locale.US);
		now = ctx.getMessage("now", b, Locale.US);
		//������Ӣ����Ϣ��ӡ����
		System.out.println(hello);		
		System.out.println(now);
		
		//��Ϊ���ó����Ļ���
		hello = ctx.getMessage("hello", a, Locale.CHINA);
		now = ctx.getMessage("now", b, Locale.CHINA);
		//������������Ϣ��ӡ����
		System.out.println(hello);		
		System.out.println(now);

	}

}
