package com.servlet.bean;

public class UserBean {
	private int userId; 
	private String name;
	private String email;
	public void setUserId(int UserId) {
		this.userId = UserId;
	}
	public int getUserId() {
		return this.userId;
	}
	
	public void setName(String name) {
		this.name = name;
	}
	public String getName() {
		return this.name;
	}
	
	public void setEmail(String email) {
		this.email = email;
	}
	public String getEmail() {
		return this.email;
	}
}
