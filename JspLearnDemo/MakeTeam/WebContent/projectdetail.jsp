<%@page import="com.servlet.bean.ProjectBean"%>
<%@page import="com.servlet.bean.UserBean"%>
<%@page import="com.servlet.util.Dbutil"%>
<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<%@ page import="java.io.*,java.util.*,java.sql.*"%>
<%
	UserBean user = (UserBean)session.getAttribute("user");
	if(user==null || request.getParameter("projectid")== null){
		getServletContext().getRequestDispatcher("/allprojects.jsp").forward(request, response);
	}
	int projectid = Integer.parseInt(request.getParameter("projectid"));
%>
<%
	ProjectBean pro=new ProjectBean();
	UserBean leader = new UserBean();
	List<String> needs=new ArrayList<String>();
	List<String> tabs=new ArrayList<String>();
	List<UserBean> members=new ArrayList<UserBean>();
	boolean isin = false;
	boolean isapplied = false;
try {  
            Connection con=(Connection) Dbutil.getConnection();  
            Statement stmt=(Statement) con.createStatement();//句柄
            String proSql="SELECT projectid,projectname,status,leaderid,details FROM project where projectid='"+projectid+"'";
	        ResultSet proRs=stmt.executeQuery(proSql);  
	        if(proRs.next()) {
	    		pro.setmProjectId(proRs.getInt(1));
	    		pro.setmProjectname(proRs.getString(2));
	    		pro.setmStatus(proRs.getInt(3));
	    		pro.setmLeaderid(proRs.getInt(4));
	    		pro.setmDetails(proRs.getString(5));
	        }

            Statement leaderstmt=(Statement) con.createStatement();//句柄
            String leaderSql="SELECT name,userid,email FROM user where userid='"+pro.getmLeaderid()+"'";
	        ResultSet leaderRs=stmt.executeQuery(leaderSql);  
	        if(leaderRs.next()) {
	        	leader.setName(leaderRs.getString(1));
	        	leader.setUserId(leaderRs.getInt(2));
	        	leader.setEmail(leaderRs.getString(3));
	        }
	        
        	Statement needsstmt=(Statement) con.createStatement();//句柄
            String needsSql="SELECT ability FROM projectneed where projectid='"+projectid+"'";
	        ResultSet needsRs=needsstmt.executeQuery(needsSql);  
	        while(needsRs.next()) {
	        	needs.add(needsRs.getString(1));
	        }
			
        	Statement tabsstmt=(Statement) con.createStatement();//句柄
            String tabsSql="SELECT tab FROM projecttab where projectid='"+projectid+"'";
	        ResultSet tabsRs=tabsstmt.executeQuery(tabsSql);  
	        while(tabsRs.next()) {
	        	tabs.add(tabsRs.getString(1));
	        }

        	Statement membersstmt=(Statement) con.createStatement();//句柄
            String membersSql="select name,userid from user where userid in (SELECT userid FROM member where projectid='"+projectid+"')";
	        ResultSet membersRs=membersstmt.executeQuery(membersSql); 
	        while(membersRs.next()) {
	        	UserBean tmpuser=new UserBean();
	        	tmpuser.setName(membersRs.getString(1));
	        	tmpuser.setUserId(membersRs.getInt(2));
	        	members.add(tmpuser);
	        }
	        
        	Statement isinstmt=(Statement) con.createStatement();//句柄
            String isinSql="SELECT userid FROM member where projectid='"+projectid+"' and userid='"+user.getUserId()+"' ";
	        ResultSet isinRs=isinstmt.executeQuery(isinSql); 
	        while(isinRs.next()) {
				isin = true;
	        }
	        
        	Statement isappliedstmt=(Statement) con.createStatement();//句柄
            String isappliedSql="SELECT userid FROM application where projectid='"+projectid+"' and userid='"+user.getUserId()+"' ";
	        ResultSet isappliedRs=isappliedstmt.executeQuery(isappliedSql); 
	        while(isappliedRs.next()) {
	        	isapplied = true;
	        }
        }  
        catch(Exception ex) {  
            ex.printStackTrace();  
        }  
        finally {  
        	Dbutil.Close();  
        }
%>
<!DOCTYPE html>
<head>
	<title>projectdetail</title>
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<meta charset="utf-8">
	<meta name="title" content="Bootstrap的使用">
	<meta name="description" content="Bootstrap网页设计">
	<meta name="keywords" content="bootstrap">
	<link href="http://cdn.staticfile.org/twitter-bootstrap/3.0.1/css/bootstrap.min.css" rel="stylesheet">
	<link href="v3/layoutit.css" rel="stylesheet">
	<!--[if lt IE 9]>
		<script src="http://apps.bdimg.com/libs/html5shiv/3.7/html5shiv.min.js"></script>
		<![endif]-->

	<script type="text/javascript" src="http://cdn.staticfile.org/jquery/2.0.0/jquery.min.js"></script>
	<script type="text/javascript" src="http://cdn.staticfile.org/jqueryui/1.10.2/jquery-ui.min.js"></script>
	<script type="text/javascript" src="http://cdn.staticfile.org/jqueryui-touch-punch/0.2.2/jquery.ui.touch-punch.min.js"></script>
	<script type="text/javascript" src="v3/jquery.htmlClean.js"></script>

	<script type="text/javascript" src="http://cdn.staticfile.org/twitter-bootstrap/3.0.1/js/bootstrap.min.js"></script>
	<script type="text/javascript" src="v3/scripts.min.js"></script>
</head>
<body>

		<div class="container">
			<div class="row clearfix">
				<div class="col-md-12 column">
					<ul class="nav nav-pills">
					<li>
						 <a href="allprojects.jsp"></span>Home</a>
					</li>
					<li>
						<a href="profile.jsp"></span><%= user.getName() %></a>
					</li>
						
						<form class="navbar-form navbar-right" role="search">
							<div class="form-group">
								<input type="text" class="form-control" />
							</div> <button type="submit" class="btn btn-default">搜索</button>
						</form>
					</ul>
		<div class="container">
			<div class="row clearfix">
				<div class="col-md-12 column">
					<div class="page-header">
						<h1>
							<%=pro.getmProjectname() %>
							<a href="information.jsp?userid=<%=leader.getUserId()%>">
							<small><%=leader.getName() %></small>
							</a>
						</h1>
					</div>
					<%if(pro.getmStatus().compareTo("已结束")==0){ %>
					<div class="alert alert-dismissable alert-success">
						 <button type="button" class="close" data-dismiss="alert" aria-hidden="true">×</button>
						<h4>
							提醒：
						</h4> 该项目已完结
					</div> 
					<%}else if(user.getUserId()==leader.getUserId()){ %>
						<form role="form" action="Stop" method="post">
							<input type="hidden" value=<%=pro.getmProjectId() %> name="projectid" >
							<button type="submit" class="btn btn-primary btn-default navbar-right">停止招募</button>
						</form>
					<%}else if(isin){ %>
						<button type="button" class="btn btn-primary btn-default navbar-right">已加入</button>
					<%}else if(isapplied){ %>
						<button type="button" class="btn btn-primary btn-default navbar-right">已申请</button>
					<%}else{%>
						<form role="form" action="Apply" method="post">
							<input type="hidden" value=<%=pro.getmProjectId() %> name="projectid" >
							<button type="submit"  class="btn btn-primary btn-default navbar-right">申请加入</button>
						</form>
					<%}%>
					<dl>
						<dt>
							Description:
						</dt>
						<dd>
							<% for(String tab:tabs){ %>
							<span class="label label-default">
								<%=tab%>
							</span>
							<%} %>
							</br></br>
							<%=pro.getmDetails() %>
						</dd>
						</br>
						<dt>
							Members:
						</dt>
						<dd>		
							<% for(UserBean member:members){ %>
							<a href="information.jsp?userid=<%=member.getUserId()%>">
							<%=member.getName()%>
							</a>
							<%} %>
						</dd>
						</br>
						<dt>
							e-mail:
						</dt>
						<dd>
							<a href="mailto:
							<%=leader.getEmail() %>
							?subject=来自项目组队网站"><%=leader.getEmail()%></a>
						</dd>
						</br>
						<dt>
							寻找队友:
						</dt>
						<dd>
							<% for(String need:needs){ %>
							<span class="label label-default">
								<%=need%>
							</span>
							<%} %>
						</dd>
						
					</dl>
					<blockquote>
						<p>
							齐心协力是一个团队成长的关键。
						</p> <small>吃辣</small>
					</blockquote>

				</div>
			</div>
		</div>
</body>
</html>