package com.Servlet;

import java.io.IOException;
import java.io.PrintWriter;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Enumeration;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;

/**
 * Servlet implementation class CheckBox
 */
@WebServlet("/CheckBox")
public class CheckBox extends HttpServlet {
	private static final long serialVersionUID = 1L;
       
    /**
     * @see HttpServlet#HttpServlet()
     */
    public CheckBox() {
        super();
        // TODO Auto-generated constructor stub
    }

	/**
	 * @see HttpServlet#doGet(HttpServletRequest request, HttpServletResponse response)
	 */
	protected void doGet(HttpServletRequest request, HttpServletResponse response) 
			throws ServletException, IOException {
		// 如果不存在 session 会话，则创建一个 session 对象
		HttpSession session = request.getSession(true);
		// 获取 session 创建时间
		Date createTime = new Date(session.getCreationTime());
		// 获取该网页的最后一次访问时间
		Date lastAccessTime = new Date(session.getLastAccessedTime());
		 
		//设置日期输出的格式  
		SimpleDateFormat df=new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");  
		
		String title = "Servlet Session 实例 - 菜鸟教程";
		Integer visitCount = new Integer(0);
		String visitCountKey = new String("visitCount");
		String userIDKey = new String("userID");
		String userID = new String("Runoob");
		
		// 检查网页上是否有新的访问者
		if (session.isNew()){
			title = "Servlet Session 实例 - 菜鸟教程";
		 	session.setAttribute(userIDKey, userID);
		} else {
		 	visitCount = (Integer)session.getAttribute(visitCountKey);
		 	visitCount = visitCount + 1;
		 	userID = (String)session.getAttribute(userIDKey);
		}
		session.setAttribute(visitCountKey,  visitCount);
		
		// 设置响应内容类型
		response.setContentType("text/html;charset=UTF-8");

		PrintWriter out = response.getWriter();
		String docType =
				"<!doctype html public \"-//w3c//dtd html 4.0 " +
				"transitional//en\">\n";
				out.println(docType +
				"<html>\n" +
				"<head><meta charset=\"utf-8\"><title>" + "读取复选框数据" + "</title></head>\n" +
				"<body bgcolor=\"#f0f0f0\">\n" +
				"<h1 align=\"center\">" + "读取复选框数据" + "</h1>\n" +
				"<table width=\"100%\" border=\"1\" align=\"center\">\n" +
				"<tr bgcolor=\"#949494\">\n" +
				"<th>参数名称</th><th>参数值</th>\n"+
				"</tr>\n");

			Enumeration paramNames = request.getParameterNames();

			while(paramNames.hasMoreElements()) {
				String paramName = (String)paramNames.nextElement();
				out.print("<tr><td>" + paramName + "</td>\n");
				String[] paramValues =
				request.getParameterValues(paramName);
				// 读取单个值的数据
				if (paramValues.length == 1) {
					String paramValue = paramValues[0];
					if (paramValue.length() == 0)
						out.println("<td><i>没有值</i></td>");
					else
						out.println("<td>" + paramValue + "</td>");
				} else {
					// 读取多个值的数据
					out.println("<td><ul>");
					for(int i=0; i < paramValues.length; i++) {
					out.println("<li>" + paramValues[i]);
				}
					out.println("</ul></td>");
				}
				out.print("</tr>");
			}
			out.println("\n</table>\n");
			
			out.println(
			         "<h2 align=\"center\">Session 信息</h2>\n" +
			        "<table border=\"1\" align=\"center\">\n" +
			        "<tr bgcolor=\"#949494\">\n" +
			        "  <th>Session 信息</th><th>值</th></tr>\n" +
			        "<tr>\n" +
			        "  <td>id</td>\n" +
			        "  <td>" + session.getId() + "</td></tr>\n" +
			        "<tr>\n" +
			        "  <td>创建时间</td>\n" +
			        "  <td>" +  df.format(createTime) + 
			        "  </td></tr>\n" +
			        "<tr>\n" +
			        "  <td>最后访问时间</td>\n" +
			        "  <td>" + df.format(lastAccessTime) + 
			        "  </td></tr>\n" +
			        "<tr>\n" +
			        "  <td>用户 ID</td>\n" +
			        "  <td>" + userID + 
			        "  </td></tr>\n" +
			        "<tr>\n" +
			        "  <td>访问统计：</td>\n" +
			        "  <td>" + visitCount + "</td></tr>\n" +
			        "</table>\n"); 
			out.println("</body></html>");
	}

	/**
	 * @see HttpServlet#doPost(HttpServletRequest request, HttpServletResponse response)
	 */
	protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		// TODO Auto-generated method stub
		doGet(request, response);
	}

}
