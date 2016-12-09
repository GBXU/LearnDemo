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
		/* �� Filter ʵ���� Web �����ӷ����Ƴ�֮ǰ���� */
	}

	/**
	 * @see Filter#doFilter(ServletRequest, ServletResponse, FilterChain)
	 */
	public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain) 
			throws IOException, ServletException {
		// place your code here
		hitCountSum++;
		System.out.println("��վ����ͳ�ƣ�"+ hitCountSum );
		// ���վ������
		System.out.println("վ����ַ��http://www.runoob.com");

		// �����󴫻ع�����
		// pass the request along the filter chain
		chain.doFilter(request, response);
	}

	/**
	 * @see Filter#init(FilterConfig)
	 */
	public void init(FilterConfig fConfig) throws ServletException {
		hitCountSum = 0;
		// ��ȡ��ʼ������
		String name = fConfig.getInitParameter("name"); 
		// �����ʼ������
		System.out.println("��վ����: " + name); 
	}

}
