package com.servlet.bean;

import java.util.List;

public class ProjectBean {
	private int mProjectId;
	private String mStatus;
	private String mProjectname;
	private int mLeaderid;
	private String mLeadername;
	private String mDetails;
//	private List<String> needs;
//	private List<String> tabs;
//	private List<UserBean> member;
	private int applicationnum;

	public void setapplicationnum(int applicationnum) {
		this.applicationnum = applicationnum;
	}
	public void setapplicationnum() {
		this.applicationnum = 0;
	}
	public int getapplicationnum() {
		return applicationnum;
	}
//	public void setmember(List<UserBean> member ) {
//		this.member = member;
//	}
//	public List<UserBean> getmembers() {
//		return member;
//	}
//	public void settabs(List<String> tabs ) {
//		this.tabs = tabs;
//	}
//	public List<String> gettabs() {
//		return tabs;
//	}
//	public void setneeds(List<String> needs ) {
//		this.needs = needs;
//	}
//	public List<String> getneeds() {
//		return needs;
//	}
	public void setmDetails(String mDetails ) {
		this.mDetails = mDetails;
	}
	public String getmDetails() {
		return mDetails;
	}
	public void setmLeadername(String mLeadername ) {
		this.mLeadername = mLeadername;
	}
	public String getmLeadername() {
		return mLeadername;
	}
	public void setmLeaderid(int mLeaderid ) {
		this.mLeaderid = mLeaderid;
	}
	public int getmLeaderid() {
		return mLeaderid;
	}
	public void setmProjectId(int mProjectId ) {
		this.mProjectId = mProjectId;
	}
	public int getmProjectId() {
		return mProjectId;
	}
	public void setmStatus(int mStatus ) {
		if(mStatus==1){
			this.mStatus = "招募中";
		}else {
			this.mStatus="已结束";
		}
	}
	public String getmStatus() {
		return mStatus;
	}
	public void setmProjectname(String mProjectname ) {
		this.mProjectname = mProjectname;
	}
	public String getmProjectname() {
		return mProjectname;
	}
}
