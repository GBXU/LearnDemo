package com.Servlet;

import java.io.IOException;
import javax.servlet.Filter;
import javax.servlet.FilterChain;
import javax.servlet.FilterConfig;
import javax.servlet.ServletException;
import javax.servlet.ServletRequest;
import javax.servlet.ServletResponse;
import javax.servlet.annotation.WebFilter;
import javax.servlet.annotation.WebInitParam;

/**
 * Servlet Filter implementation class MyFilter
 */
@WebFilter(
		urlPatterns = { "/*" }, 
		initParams = { 
				@WebInitParam(name = "name", value = "test")
		})
public class MyFilter implements Filter{
	private int hitCountSum;
    /**
     * @see Filter#Filter()
     */
    public MyFilter() {
        super();
        // TODO Auto-generated constructor stub
    }

	/**
	 * @see Filter#destroy()
	 */
	public void destroy() {
		/* 在 Filter 实例被 Web 容器从服务移除之前调用 */
	}

	/**
	 * @see Filter#doFilter(ServletRequest, ServletResponse, FilterChain)
	 */
	public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain) 
			throws IOException, ServletException {
		// place your code here
		hitCountSum++;
		System.out.println("网站访问统计："+ hitCountSum );
		// 输出站点名称
		System.out.println("站点网址：http://www.runoob.com");

		// 把请求传回过滤链
		// pass the request along the filter chain
		chain.doFilter(request, response);
	}

	/**
	 * @see Filter#init(FilterConfig)
	 */
	public void init(FilterConfig fConfig) throws ServletException {
		hitCountSum = 0;
		// 获取初始化参数
		String name = fConfig.getInitParameter("name"); 
		// 输出初始化参数
		System.out.println("网站名称: " + name); 
	}

}
