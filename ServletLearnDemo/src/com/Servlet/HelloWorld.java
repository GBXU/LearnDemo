package com.Servlet;

import java.io.IOException;
import java.io.PrintWriter;
import java.net.URLEncoder;
import java.util.Locale;

import javax.servlet.ServletConfig;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.Cookie;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

/**
 * Servlet implementation class HelloWorld
 */
@WebServlet("/HelloWorld")
public class HelloWorld extends HttpServlet {
	private static final long serialVersionUID = 1L;
	private int hitCount; 
	public void init(ServletConfig config) throws ServletException {
		super.init(config);
		//初始化，例如打开数据库，点击率
		// 重置点击计数器
		hitCount = 0;
	}
    /**
     * @see HttpServlet#HttpServlet()
     */
    public HelloWorld() {
        super();
        // TODO Auto-generated constructor stub
    }

	/**
	 * @see HttpServlet#doGet(HttpServletRequest request, HttpServletResponse response)
	 */
	protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		// 获取客户端的区域设置
		Locale locale = request.getLocale();
		String language = locale.getLanguage();
		String country = locale.getCountry();
		// 增加 hitCount 
		hitCount++;
		//记录登录信息，写入cookie
		Cookie nameCookie = new Cookie("name",URLEncoder.encode(request.getParameter("name"), "UTF-8")); // 中文转码
		nameCookie.setMaxAge(60*60);//60*60 seconds
		response.addCookie(nameCookie);
		
		// 设置状态码
		//response.sendRedirect("http://baidu.com");
		//response.sendError(407, "test:response code test" );
		
		// 设置 HTTP 响应报头
		//http://www.runoob.com/servlet/servlet-server-response.html
		response.setContentType("text/html;charset=UTF-8");
		response.setIntHeader("Refresh", 5);
		//状态码
		// 处理中文
		String name =new String(request.getParameter("name").getBytes("ISO8859-1"),"UTF-8");
		// 实际的逻辑是在这里
		PrintWriter out = response.getWriter();
		String docType = "<!DOCTYPE html> \n";
		String title = "使用 GET 方法读取表单数据";
		out.println(docType +
			    "<html>\n" +
			    "<head><title>" + title + "</title></head>\n" +
			    "<body bgcolor=\"#f0f0f0\">\n" +
			    "<h1 align=\"center\">" + title + " : "+language + "from "+country + "</h1>\n" +
			    "<h2 align=\"center\">" + "自动刷新：点击量" + hitCount + "</h2>\n" +
			    "<ul>\n" +
			    "  <li><b>站点名</b>："
			    + name + "\n" +
			    "  <li><b>网址</b>："
			    + request.getParameter("url") + "\n" +
			    "</ul>\n" +
			    "</body></html>");
		//out.println("<h1>" + "hello" + "</h1>");
		//response.getWriter().append("Served at: ").append(request.getContextPath());
	}

	/**
	 * @see HttpServlet#doPost(HttpServletRequest request, HttpServletResponse response)
	 */
	protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		// TODO Auto-generated method stub
		doGet(request, response);
	}
	public void destroy() {

	}
}
