package com.bean;

public class ChineseImpl implements Person{
	private String name;
	private int age;
	public String getName() {
		return name;
	}
	public void setName(String name) {
		this.name = name;
	}
	public int getAge() {
		return age;
	}
	public void setAge(int age) {
		this.age = age;
	}
	@Override
	public void Speak() {
		// TODO Auto-generated method stub
		System.out.println("I'm Chinese,My name is "+name);
	}
}
