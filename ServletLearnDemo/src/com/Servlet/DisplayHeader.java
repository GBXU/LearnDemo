package com.Servlet;

import java.io.IOException;
import java.io.PrintWriter;
import java.net.URLDecoder;
import java.util.Enumeration;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.Cookie;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

/**
 * Servlet implementation class DisplayHeader
 */
@WebServlet("/DisplayHeader")
public class DisplayHeader extends HttpServlet {
	private static final long serialVersionUID = 1L;
       
    /**
     * @see HttpServlet#HttpServlet()
     */
    public DisplayHeader() {
        super();
        // TODO Auto-generated constructor stub
    }

	/**
	 * @see HttpServlet#doGet(HttpServletRequest request, HttpServletResponse response)
	 */
	protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		// TODO Auto-generated method stub
		// 设置响应内容类型
				response.setContentType("text/html;charset=UTF-8");

				PrintWriter out = response.getWriter();
				String title = "HTTP Header 请求实例 - 菜鸟教程实例";
				String docType =
					"<!DOCTYPE html> \n";
					out.println(docType +
					"<html>\n" +
					"<head><meta charset=\"utf-8\"><title>" + title + "</title></head>\n"+
					"<body bgcolor=\"#f0f0f0\">\n" +
					"<h1 align=\"center\">" + title + "</h1>\n" +
					"<table width=\"100%\" border=\"1\" align=\"center\">\n" +
					"<tr bgcolor=\"#949494\">\n" +
					"<th>Header 名称</th><th>Header 值</th>\n"+
					"</tr>\n");

				Enumeration headerNames = request.getHeaderNames();

				while(headerNames.hasMoreElements()) {
					String paramName = (String)headerNames.nextElement();
					out.print("<tr><td>" + paramName + "</td>\n");
					String paramValue = request.getHeader(paramName);
					out.println("<td> " + paramValue + "</td></tr>\n");
				}
				out.println("</table>\n");
				
				Cookie cookie = null;
		    	Cookie[] cookies = null;
		    	cookies = request.getCookies();
				if( cookies != null ){
		            out.println("<h2>Cookie 名称和值</h2>");
		            for (int i = 0; i < cookies.length; i++){
		               cookie = cookies[i];
		               if((cookie.getName( )).compareTo("name") == 0 ){
		                    //cookie.setMaxAge(0);
		                    //response.addCookie(cookie);
		                    //out.print("已删除的 cookie：" + cookie.getName( ) + "<br/>");
		               }
		               out.print("名称：" + cookie.getName( ) + "，");
		               out.print("值：" +  URLDecoder.decode(cookie.getValue(), "utf-8") +" <br/>");
		            }
		         }else{
		             out.println(
		               "<h2 class=\"tutheader\">No Cookie founds</h2>");
		         }
				out.println("</body>");
				out.println("</html>");

	}

	/**
	 * @see HttpServlet#doPost(HttpServletRequest request, HttpServletResponse response)
	 */
	protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		// TODO Auto-generated method stub
		doGet(request, response);
	}

}
