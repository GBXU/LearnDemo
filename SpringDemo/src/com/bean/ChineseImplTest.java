package com.bean;

import static org.junit.Assert.*;

import org.junit.Test;
import org.springframework.context.ApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;

public class ChineseImplTest {
	/*
	 * ≤‚ ‘ …Ë÷µ◊¢»Î
	 */
	@Test
	public void test()throws Exception{
		@SuppressWarnings("resource")
		ApplicationContext context = new ClassPathXmlApplicationContext("applicationContext.xml");
		Person person = (Person)context.getBean("chinese");
		person.Speak();
	}

}
