<%@page import="com.servlet.bean.ProjectBean"%>
<%@page import="com.servlet.bean.UserBean"%>
<%@page import="com.servlet.util.Dbutil"%>
<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<%@ page import="java.io.*,java.util.*,java.sql.*"%>
<%
	UserBean user = (UserBean)session.getAttribute("user");
	if(user==null||request.getParameter("userid")==null){
		getServletContext().getRequestDispatcher("/allprojects.jsp").forward(request, response);
	}
%>
<%
	UserBean friend = new UserBean();
	friend.setUserId(Integer.parseInt(request.getParameter("userid")));
	if(user.getUserId()==friend.getUserId()){
		getServletContext().getRequestDispatcher("/profile.jsp").forward(request, response);
	}
	List<String> abilities=new ArrayList<String>();
	List<String> tabs=new ArrayList<String>();
	List<ProjectBean> projectin = new ArrayList<ProjectBean>();
try {  
            Connection con=(Connection) Dbutil.getConnection();  
        	
            Statement userstmt=(Statement) con.createStatement();//能力
            String userSql="SELECT userId,name,email FROM user where userid='"+friend.getUserId()+"'";
	        ResultSet userRs=userstmt.executeQuery(userSql);  
	        while(userRs.next()) {
	        	friend.setUserId(userRs.getInt(1));
	        	friend.setName(userRs.getString(2));
	        	friend.setEmail(userRs.getString(3));
	        }
            
        	Statement abilitiesstmt=(Statement) con.createStatement();//能力
            String abilitiesSql="SELECT ability FROM userability where userid='"+friend.getUserId()+"'";
	        ResultSet abilitiesRs=abilitiesstmt.executeQuery(abilitiesSql);  
	        while(abilitiesRs.next()) {
	        	abilities.add(abilitiesRs.getString(1));
	        }
			
        	Statement tabsstmt=(Statement) con.createStatement();//兴趣
            String tabsSql="SELECT tab FROM usertab where userid='"+friend.getUserId()+"'";
	        ResultSet tabsRs=tabsstmt.executeQuery(tabsSql);  
	        while(tabsRs.next()) {
	        	tabs.add(tabsRs.getString(1));
	        }
			
        	Statement projectinstmt=(Statement) con.createStatement();//句柄
            String projectinSql="select projectid,projectname,status from project where projectid in (SELECT projectid FROM member where userid='"+friend.getUserId()+"')";
	        ResultSet projectinRs=projectinstmt.executeQuery(projectinSql); 
	        while(projectinRs.next()) {
	        	ProjectBean tmp=new ProjectBean();
	        	tmp.setmProjectId(projectinRs.getInt(1));
	        	tmp.setmProjectname(projectinRs.getString(2));
	        	tmp.setmStatus(projectinRs.getInt(3));
	        	projectin.add(tmp);
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
	<title>FriendProfile</title>
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
				<dl>
					<h1>
						<%=friend.getName() %>
					</h1>
					</br>
					<dt>
						能力
					</dt>
					<dd>
						<% for(String ability:abilities){ %>
						<span class="label label-default">
							<%=ability%>
						</span>
						<%} %>
					</dd>
					</br>
					<dt>
						兴趣
					</dt>
					<dd>
						<% for(String tab:tabs){ %>
						<span class="label label-default">
							<%=tab%>
						</span>
						<%} %>
					</dd>
					</br>
					<dt>
						e-mail:
					</dt>
					<dd>
						<a href="mailto:
						<%=friend.getEmail() %>
						?subject=来自项目组队网站"><%=friend.getEmail()%></a>
					</dd>
					</br>
					<dt>
						参与项目
					</dt>
					<dd>
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
								<%for(ProjectBean item:projectin){ %>
								<tr>
									<td>
										<%=item.getmProjectId() %>
									</td>
									<td>
										<a href="projectdetail.jsp?projectid=<%=item.getmProjectId() %>">
										<%=item.getmProjectname() %>
										</a>
									</td>
									<td>
										<%=item.getmStatus()%>
									</td>
								</tr>
								<% } %>
							</tbody>
						</table>
					</dd>
					
				</dl>
			</div>
		</div>
	</div>
</body>
</html>