package com.servlet.main;

import java.io.IOException;
import java.io.PrintWriter;
import java.sql.ResultSet;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;

import com.mysql.jdbc.Connection;
import com.mysql.jdbc.Statement;
import com.servlet.bean.UserBean;
import com.servlet.util.Dbutil;

/**
 * Servlet implementation class Login
 */
@WebServlet("/Login")
public class Login extends HttpServlet {
	private static final long serialVersionUID = 1L;
       
    /**
     * @see HttpServlet#HttpServlet()
     */
    public Login() {
        super();
    }

	/**
	 * @see HttpServlet#doGet(HttpServletRequest request, HttpServletResponse response)
	 */
	protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		response.getWriter().append("Served at: ").append(request.getContextPath());
	}
	/**
	 * @see HttpServlet#doPost(HttpServletRequest request, HttpServletResponse response)
	 */
	protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		HttpSession session = request.getSession(true);
		String EM = request.getParameter("EM"); 
        String PW= request.getParameter("PW");  

        response.setContentType("text/html; charset=UTF-8");  
        try {  
            Connection con=(Connection) Dbutil.getConnection();  
            Statement stmt=(Statement) con.createStatement();
            String loginSql="SELECT userId,name,email FROM user WHERE email="+ "'" + EM+ "'"+ " AND password="+ "'" +PW+ "'";//�����ſ�������
	        ResultSet loginRs=stmt.executeQuery(loginSql);  
	        if(loginRs.next()) {  
	    		UserBean user = new UserBean();
	    		user.setUserId(loginRs.getInt(1));
	    		user.setName(loginRs.getString(2));
	    		user.setEmail(loginRs.getString(3));
	    		session.setAttribute("user",user);
	        }
	        
        }  
        catch(Exception ex) {  
            ex.printStackTrace();  
        }  
        finally {  
        	Dbutil.Close();  
        }
        getServletContext().getRequestDispatcher("/allprojects.jsp").forward(request, response);
        //response.sendRedirect("allprojects.jsp");
	}

}
