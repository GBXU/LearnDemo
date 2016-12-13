<%@page import="com.servlet.bean.ProjectBean"%>
<%@page import="com.servlet.bean.UserBean"%>
<%@page import="com.servlet.util.Dbutil"%>
<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<%@ page import="java.io.*,java.util.*,java.sql.*"%>
<%@ page import="javax.servlet.http.*,javax.servlet.*" %>
<%
	UserBean user = (UserBean)session.getAttribute("user");
	String userName = null;	
	if(user==null){
		userName = "登录";
	}else{
		userName = user.getName();
	}
%>
<%
	List<ProjectBean> projectList = new ArrayList<ProjectBean>();
try {
            Connection con=(Connection) Dbutil.getConnection();  
            Statement stmt=(Statement) con.createStatement();//句柄
            String prosSql="SELECT projectid,projectname,status FROM project";//单引号坑死我了
	        ResultSet prosRs=stmt.executeQuery(prosSql);  
	        while(prosRs.next()) {
	    		ProjectBean pro= new ProjectBean();
	    		pro.setmProjectId(prosRs.getInt(1));
	    		pro.setmProjectname(prosRs.getString(2));
	    		pro.setmStatus(prosRs.getInt(3));
	    		projectList.add(pro);
	        }
        }  
        catch(Exception ex) {  
            ex.printStackTrace();  
        }  
        finally {  
        	Dbutil.Close();  
        }
%>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<head>
	<title>AllProjects</title>
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
						<li class="active">
							 <a href="allprojects.jsp">Home</a>
						</li>
						<% if(user==null){ %>
						<li>
							<a id="modal-326986" href="#modal-container-326986" role="button" class="btn" data-toggle="modal"><%= userName %></a>
							<div class="modal fade" id="modal-container-326986" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
							<div class="modal-dialog">
								<div class="modal-content">
									<div class="modal-header">
										<button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>
										<h4 class="modal-title" id="myModalLabel">
											登录
										</h4>
									</div>
									<div class="modal-body">
										<form role="form" action="Login" method="post" class="form-inline">
											<div class="form-group">
												 <label for="EM">Email address</label><input type="text" class="form-control" name="EM" />
											</div>
											<div class="form-group">
												 <label for="PW">Password</label><input type="password" class="form-control" name="PW" />
											</div>
											</br>
											<div class="modal-footer">
												<button type="button" class="btn btn-default" data-dismiss="modal">取消</button> 
												<button type="submit" class="btn btn-primary">登录</button>
											</div>
										</form>
									</div>
								</div>
							</div>
							</div>							
						</li>
						<li>
							<a id="modal-326986" href="#modal-container-326912" role="button" class="btn" data-toggle="modal">注册</a>
							<div class="modal fade" id="modal-container-326912" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
								<div class="modal-dialog">
									<div class="modal-content">
										<div class="modal-header">
											<button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>
											<h4 class="modal-title" id="myModalLabel">
												注册
											</h4>
										</div>
										<div class="modal-body">
											<form role="form" action="Register" method="post" class="form-inline">
												<div class="form-group">
													 <label for="exampleInputEmail1">Email*</label><input type="text" class="form-control" name="EM" />
												</div>
												</br>
												<div class="form-group">
													 <label for="exampleInputPassword1">Password*</label><input type="password" class="form-control" name="PW" />
												</div>
												</br>
												<div class="form-group">
													 <label for="exampleInputPassword1">姓名*</label><input type="text" class="form-control" name="NA" />
												</div>
												</br>
												<div class="form-group">
													 <label for="exampleInputAbility1">技能Ability*</label><input type="text" placeholder="至少输入一个Ability" class="form-control" name="AB1" />
												</div>
												<div class="form-group">
													 <label for="exampleInputAbility1">Ability2</label><input type="text" class="form-control" name="AB2" />
												</div>
												<div class="form-group">
													 <label for="exampleInputAbility1">Ability3</label><input type="text" class="form-control" name="AB3" />
												</div>
												</br>
												<div class="form-group">
													 <label for="exampleInputFavor1">感兴趣的Tab1*</label><input type="text" placeholder="至少输入一个标签" class="form-control" name="TA1" />
												</div>
												<div class="form-group">
													 <label for="exampleInputFavor1">Tab2</label><input type="text" class="form-control" name="TA2" />
												</div>
												<div class="form-group">
													 <label for="exampleInputFavor1">Tab3</label><input type="text" class="form-control" name="TA3" />
												</div>
												</br>
												<div class="modal-footer">
													 <button type="button" class="btn btn-default" data-dismiss="modal">取消</button> 
													 <a href="profile.html">
													 	<button type="submit" class="btn btn-primary">确定</button>
													 </a>
												</div>
											</form>
										</div>
									</div>
								</div>
							</div>
						</li>
						<% }else{ %>
						<li>
							<a href="profile.jsp"><%= userName %></a>
						</li>
						<% } %>
						<form class="navbar-form navbar-right" role="search">
							<div class="form-group">
								<input type="text" class="form-control" />
							</div> <button type="submit" class="btn btn-default">搜索</button>
						</form>
					</ul>
			<div class="container">
				<div class="row clearfix">
					<div class="col-md-12 column">
						<table class="table table-hover">
							<thead>
								<tr>
									<th>
										编号
									</th>
									<th>
										项目
									</th>
									<th>
										状态
									</th>
								</tr>
							</thead>
							<tbody>
								<%for(ProjectBean item:projectList){ %>
								<tr>
									<td>
										<%=item.getmProjectId() %>
									</td>
									<td>
										<a href="projectdetail.jsp?projectid=<%=item.getmProjectId()%>">
										<%=item.getmProjectname()%>
										</a>
									</td>
									<td>
										<%=item.getmStatus()%>
									</td>
								</tr>
								<% } %>

							</tbody>
						</table>
					</div>
				</div>
				<ul class="pagination">
					<li>
						 <a href="#">Prev</a>
					</li>
					<li>
						 <a href="#">1</a>
					</li>
					<li>
						 <a href="#">2</a>
					</li>
					<li>
						 <a href="#">3</a>
					</li>
					<li>
						 <a href="#">4</a>
					</li>
					<li>
						 <a href="#">5</a>
					</li>
					<li>
						 <a href="#">Next</a>
					</li>
				</ul>
		</div>
</body>
</html>