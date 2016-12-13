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
	ProjectBean project = new ProjectBean();
	List<UserBean> applicant = new ArrayList<UserBean>();
try {  
            Connection con=(Connection) Dbutil.getConnection();  
            
        	Statement isleaderstmt=(Statement) con.createStatement();//句柄
            String isleaderSql="SELECT projectid,projectname FROM project where projectid='"+projectid+"' and leaderid='"+user.getUserId()+"' ";
	        ResultSet isleaderRs=isleaderstmt.executeQuery(isleaderSql); 
	        if(isleaderRs.next()) {
	        	project.setmProjectId(isleaderRs.getInt(1));
	        	project.setmProjectname(isleaderRs.getString(2));
	        }else{
	        	getServletContext().getRequestDispatcher("/allprojects.jsp").forward(request, response);
	        }

        	Statement applicationstmt=(Statement) con.createStatement();//句柄
            String applicationSql="select name,userid from user where userid in (SELECT userid FROM application where projectid='"+projectid+"')";
	        ResultSet applicationRs=applicationstmt.executeQuery(applicationSql); 
	        while(applicationRs.next()) {
	        	UserBean tmpuser=new UserBean();
	        	tmpuser.setName(applicationRs.getString(1));
	        	tmpuser.setUserId(applicationRs.getInt(2));
	        	applicant.add(tmpuser);
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
	<title>Profile</title>
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
					<li >
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
			</div>
		</div>
	</div>

	<div class="container">
		<div class="row clearfix">
			<div class="col-md-12 column">
				<table class="table table-hover">
					<thead>
						<tr>
							<th>
								项目
							</th>
							<th>
								申请人
							</th>
							<th>
								处理
							</th>
						</tr>
					</thead>
					<tbody>
						<tr class="warning">
										<%for(UserBean item:applicant){ %>
										<tr>
											<td>
												<%=project.getmProjectname() %>
											</td>
											<td>
												<a href="information.jsp?userid=<%=item.getUserId() %>">
												<%=item.getName() %>
												</a>
											</td>
											<td>
												<form role="form" action="Accept" method="post">
													<input type="hidden" value=<%=project.getmProjectId() %> name="projectid" >
													<button type="submit" class="btn btn-primary btn-default">同意</button>
												</form>												
											</td>
										</tr>
										<% } %>
						</tr>
					</tbody>
				</table>
			</div>
		</div>
	</div>
</body>
</html>