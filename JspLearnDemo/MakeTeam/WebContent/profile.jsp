<%@page import="com.servlet.bean.ProjectBean"%>
<%@page import="com.servlet.bean.UserBean"%>
<%@page import="com.servlet.util.Dbutil"%>
<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<%@ page import="java.io.*,java.util.*,java.sql.*"%>
<%
	UserBean user = (UserBean)session.getAttribute("user");
	if(user==null){
		getServletContext().getRequestDispatcher("/allprojects.jsp").forward(request, response);
	}
%>
<%
	List<String> abilities=new ArrayList<String>();
	List<String> tabs=new ArrayList<String>();
	List<ProjectBean> projectin = new ArrayList<ProjectBean>();
	List<ProjectBean> projectlead = new ArrayList<ProjectBean>();
try {  
            Connection con=(Connection) Dbutil.getConnection();  
	        
        	Statement abilitiesstmt=(Statement) con.createStatement();//句柄
            String abilitiesSql="SELECT ability FROM userability where userid='"+user.getUserId()+"'";
	        ResultSet abilitiesRs=abilitiesstmt.executeQuery(abilitiesSql);  
	        while(abilitiesRs.next()) {
	        	abilities.add(abilitiesRs.getString(1));
	        }
			
        	Statement tabsstmt=(Statement) con.createStatement();//句柄
            String tabsSql="SELECT tab FROM projecttab where projectid='"+user.getUserId()+"'";
	        ResultSet tabsRs=tabsstmt.executeQuery(tabsSql);  
	        while(tabsRs.next()) {
	        	tabs.add(tabsRs.getString(1));
	        }
			
        	Statement projectinstmt=(Statement) con.createStatement();//句柄
            String projectinSql="select projectid,projectname,status from project where projectid in (SELECT projectid FROM member where userid='"+user.getUserId()+"')";
	        ResultSet projectinRs=projectinstmt.executeQuery(projectinSql); 
	        while(projectinRs.next()) {
	        	ProjectBean tmp=new ProjectBean();
	        	tmp.setmProjectId(projectinRs.getInt(1));
	        	tmp.setmProjectname(projectinRs.getString(2));
	        	tmp.setmStatus(projectinRs.getInt(3));
	        	projectin.add(tmp);
	        }
	        
        	Statement projectleadstmt=(Statement) con.createStatement();//句柄
            String projectleadSql="select projectid,projectname,status,(select count(*) from application where application.projectid = project.projectid)as num from project where projectid in (SELECT projectid FROM project where leaderid='"+user.getUserId()+"')";
	        ResultSet projectleadRs=projectleadstmt.executeQuery(projectleadSql); 
	        while(projectleadRs.next()) {
	        	ProjectBean tmp=new ProjectBean();
	        	tmp.setmProjectId(projectleadRs.getInt(1));
	        	tmp.setmProjectname(projectleadRs.getString(2));
	        	tmp.setmStatus(projectleadRs.getInt(3));
	        	tmp.setapplicationnum(projectleadRs.getInt(4));
	        	projectlead.add(tmp);
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
	<link href="css/bootstrap.min.css" rel="stylesheet">
	<link href="v3/layoutit.css" rel="stylesheet">
	<!--[if lt IE 9]>
		<script src="http://apps.bdimg.com/libs/html5shiv/3.7/html5shiv.min.js"></script>
		<![endif]-->

	<script type="text/javascript" src="http://cdn.staticfile.org/jquery/2.0.0/jquery.min.js"></script>
	<script type="text/javascript" src="http://cdn.staticfile.org/jqueryui/1.10.2/jquery-ui.min.js"></script>
	<script type="text/javascript" src="http://cdn.staticfile.org/jqueryui-touch-punch/0.2.2/jquery.ui.touch-punch.min.js"></script>
	<script type="text/javascript" src="v3/jquery.htmlClean.js"></script>

	<script type="text/javascript" src="js/bootstrap.min.js"></script>
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
					<li class="active">
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
						<%=user.getEmail() %>
						?subject=来自项目组队网站"><%=user.getEmail()%></a>
					</dd>
				</dl>
				<div class="panel-group" id="panel-517614">
					<div class="panel panel-default">
						<div class="panel-heading">
							 <a class="panel-title" data-toggle="collapse" data-parent="#panel-517614" href="#panel-element-152355">已参加项目</a>
						</div>
						<div id="panel-element-152355" class="panel-collapse in">
							<div class="panel-body">
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
												<a href="projectdetail.jsp?projectid=<%=item.getmProjectId()%>">
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
							</div>
						</div>
					</div>
					<div class="panel panel-default">
						<div class="panel-heading">
							 <a class="panel-title collapsed" data-toggle="collapse" data-parent="#panel-517614" href="#panel-element-sa">您管理的项目</a>
						</div>
						<div id="panel-element-sa" class="panel-collapse collapse">
							<div class="panel-body">
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
											<th>
												新的申请
											</th>
										</tr>
									</thead>
									<tbody>
										<%for(ProjectBean item:projectlead){ %>
										<tr>
											<td>
												<%=item.getmProjectId() %>
											</td>
											<td>
												<a href="projectdetail.jsp?projectid=<%=item.getmProjectId()%>">
												<%=item.getmProjectname() %>
												</a>
											</td>
											<td>
												<%=item.getmStatus()%>
											</td>
											<td>
												<a href="manageapplication.jsp?projectid=<%=item.getmProjectId()%>">
												<%=item.getapplicationnum() %>
												</a>
											</td>
										</tr>
										<% } %>
									</tbody>
								</table>
							
								<a id="modal-326986" href="#modal-container-326986" role="button" class="btn" data-toggle="modal">添加项目</a>
								<div class="modal fade" id="modal-container-326986" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
									<div class="modal-dialog">
										<div class="modal-content">
											<div class="modal-header">
												<button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>
												<h4 class="modal-title" id="myModalLabel">
													项目信息
												</h4>
											</div>
											<div class="modal-body">
												<form role="form" action="Publish" method="post" class="form-inline">
													<div class="form-group">
														 <label for="projectname">项目名*</label><input type="text" class="form-control" id="projectname" autofocus name="NA"/>
													</div>
													<br>
													<div class="form-group">
														 <label for="projecttab">标签*</label><input type="text" class="form-control" id="projecttab" placeholder="至少输入一个标签" name="TA1"/>
													</div>
													<div class="form-group">
														 <label for="projecttab">标签</label><input type="text" class="form-control" id="projecttab" name="TA2"/>
													</div>
													<div class="form-group">
														 <label for="projecttab">标签</label><input type="text" class="form-control" id="projecttab" name="TA3" />
													</div>
													<br>
													<div class="form-group">
														 <label for="projectdetail">详情*</label>
														 <textarea  class="form-control" id="projectdetail" rows="10" cols="30" name="DE">
														 </textarea>
													</div>
													<br>
													<div class="form-group">
														 <label for="projectneed">寻找队友的方向*</label><input placeholder="至少输入一个标签" type="text" class="form-control" id="projectneed" name="AB1"/>
													</div>
													<div class="form-group">
														 <label for="projectneed">方向</label><input  type="text" class="form-control" id="projectneed" name="AB2"/>
													</div>
													<div class="form-group">
														 <label for="projectneed">方向</label><input type="text" class="form-control" id="projectneed" name="AB3"/>
													</div>
													</br>
															
													<div class="modal-footer">
														 <button type="button" class="btn btn-default" data-dismiss="modal">取消</button> 
														 <button type="submit" class="btn btn-primary">添加</button>
													</div>
												</form>
											</div>
										</div>
									</div>
								</div>

							</div>
						</div>
					</div>

				</div>
			</div>
		</div>
	</div>
</body>
</html>