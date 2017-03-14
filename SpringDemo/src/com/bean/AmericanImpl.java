package com.bean;

import org.junit.Test;
import org.springframework.context.ApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;

public class AmericanImpl implements Person {
	private ChineseImpl chinese;
	/*构造注入
	 * 1 需要xml里注明construct的依赖
	 * 2 又AmericanImpl有ChineseImpl的依赖，所以要在xml的属性中标明<ref bean="chinese"/>
	 * 3 xml中的依赖可以是： 接口的实现、类的实例、子类的实例
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

