package com.bean;

import org.junit.Test;
import org.springframework.context.ApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;

public class AmericanImpl implements Person {
	private ChineseImpl chinese;
	/*����ע��
	 * 1 ��Ҫxml��ע��construct������
	 * 2 ��AmericanImpl��ChineseImpl������������Ҫ��xml�������б���<ref bean="chinese"/>
	 * 3 xml�е����������ǣ� �ӿڵ�ʵ�֡����ʵ���������ʵ��
	 * */
	public AmericanImpl(ChineseImpl chinese) {
		super();
		this.chinese = chinese;
	}
	public ChineseImpl getChinese() {
		return chinese;
	}
	public void setChinese(ChineseImpl chinese) {
		this.chinese = chinese;
	}
	@Override
	public void Speak() {
		System.out.println("I was a chinese, my name is " + chinese.getName());
	}
}

